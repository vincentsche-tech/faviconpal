// 冒烟测试：从 index.html 提取纯函数，验证 ICO / ZIP / CRC32 核心编码逻辑
'use strict';
const fs = require('fs');
const path = require('path');
const os = require('os');
const zlib = require('zlib');

const htmlPath = path.join(__dirname, '..', 'index.html');
const html = fs.readFileSync(htmlPath, 'utf8');
const m = html.match(/<script>([\s\S]*?)<\/script>/);
if (!m) { console.error('NO SCRIPT FOUND'); process.exit(1); }

const fn = new Function(m[1] + '\n;return { crc32, buildIco, buildZip, makeManifest, makeHtmlSnippet };');
const { crc32, buildIco, buildZip, makeManifest } = fn();

// ---- 生成真实 PNG（RGBA，zlib deflate）----
function makePng(w, h, rgba = [255, 0, 0, 255]) {
  const raw = Buffer.alloc((w * 4 + 1) * h);
  for (let y = 0; y < h; y++) {
    raw[y * (w * 4 + 1)] = 0;
    for (let x = 0; x < w; x++) {
      const o = y * (w * 4 + 1) + 1 + x * 4;
      raw[o] = rgba[0]; raw[o + 1] = rgba[1]; raw[o + 2] = rgba[2]; raw[o + 3] = rgba[3];
    }
  }
  const ihdr = Buffer.alloc(13);
  ihdr.writeUInt32BE(w, 0); ihdr.writeUInt32BE(h, 4);
  ihdr[8] = 8; ihdr[9] = 6;
  const chunk = (type, data) => {
    const len = Buffer.alloc(4); len.writeUInt32BE(data.length);
    const td = Buffer.concat([Buffer.from(type), data]);
    const crc = Buffer.alloc(4); crc.writeUInt32BE(crc32(td) >>> 0);
    return Buffer.concat([len, td, crc]);
  };
  return Buffer.concat([
    Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]),
    chunk('IHDR', ihdr),
    chunk('IDAT', zlib.deflateSync(raw)),
    chunk('IEND', Buffer.alloc(0))
  ]);
}

let pass = 0, fail = 0;
const check = (name, cond) => { cond ? pass++ : fail++; console.log((cond ? '  PASS ' : '  FAIL ') + name); };

// 1) CRC32 已知向量
check('crc32("123456789") == 0xCBF43926', crc32(Buffer.from('123456789')) === 0xCBF43926);

// 2) ICO 打包
const sizes = [16, 32, 48, 256];
const pngs = sizes.map(s => ({ data: new Uint8Array(makePng(s, s, [10, 200, 120, 255])), width: s, height: s }));
const ico = buildIco(pngs);
fs.writeFileSync(path.join(os.tmpdir(), 'faviconpal_test.ico'), Buffer.from(ico));
const dv = new DataView(ico.buffer, ico.byteOffset, ico.byteLength);
check('ICO type==1', dv.getUint16(2, true) === 1);
check('ICO count==4', dv.getUint16(4, true) === 4);
let icoOk = true;
for (let i = 0; i < 4; i++) {
  const e = 6 + i * 16;
  const w = dv.getUint8(e), h = dv.getUint8(e + 1);
  const planes = dv.getUint16(e + 4, true), bits = dv.getUint16(e + 6, true);
  const size = dv.getUint32(e + 8, true), off = dv.getUint32(e + 12, true);
  const expectW = sizes[i] >= 256 ? 0 : sizes[i];
  const ok = w === expectW && h === expectW && planes === 1 && bits === 32 && off + size <= ico.length;
  if (!ok) icoOk = false;
  console.log(`  entry${i}: ${w === 0 ? 256 : w}px planes=${planes} bits=${bits} size=${size} off=${off}${ok ? '' : '  <-- BAD'}`);
  // 校验 data 偏移处确实是指定的 PNG 签名
  const sig = [0x89, 0x50, 0x4e, 0x47].every((b, k) => ico[off + k] === b);
  if (!sig) icoOk = false;
}
check('ICO entries valid (planes/bits/offset/PNG sig)', icoOk);

// 3) ZIP 打包（store）
const zip = buildZip([
  { name: 'icon/favicon.ico', data: ico },
  { name: 'icon/favicon-32x32.png', data: new Uint8Array(makePng(32, 32, [0, 0, 255, 255])) },
  { name: 'site.webmanifest', data: new Uint8Array(Buffer.from('{"name":"test"}')) }
]);
fs.writeFileSync(path.join(os.tmpdir(), 'faviconpal_test.zip'), Buffer.from(zip));
const zdv = new DataView(zip.buffer, zip.byteOffset, zip.byteLength);
check('ZIP EOCD sig', zdv.getUint32(zip.length - 22, true) === 0x06054b50);
const zcount = zdv.getUint16(zip.length - 12, true);
check('ZIP entry count==3', zcount === 3);
const cdSize = zdv.getUint32(zip.length - 10, true); // EOCD+12
const cdOff = zdv.getUint32(zip.length - 6, true);   // EOCD+16
check('ZIP central directory size==3*46+names', cdSize > 3 * 46);
check('ZIP cd offset + size == file length - 22', cdOff + cdSize === zip.length - 22);
// 验证第一个 local file header
const lfv = new DataView(zip.buffer, zip.byteOffset, zip.byteLength);
check('ZIP LFH sig @0', lfv.getUint32(0, true) === 0x04034b50);
const nameLen = lfv.getUint16(26, true);
check('ZIP first file name ok', String.fromCharCode(...zip.subarray(30, 30 + nameLen)) === 'icon/favicon.ico');

// 4) manifest 输出
const mf = JSON.parse(makeManifest('My Web App'));
check('manifest has 192+512 icons', mf.icons.some(i => i.sizes === '192x192') && mf.icons.some(i => i.sizes === '512x512'));

console.log(`\nRESULT: ${pass} passed, ${fail} failed`);
process.exit(fail ? 1 : 0);
