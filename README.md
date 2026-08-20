# FaviconPal

Free in-browser favicon & ICO conversion tools. Convert WebP (and more) to ICO and a complete favicon set — 16px to 256px, Apple Touch Icon, Android icons, `manifest.json` and ready-to-paste HTML code.

**100% client-side.** Files never leave your device. No upload, no signup, no watermark.

Live at: https://faviconpal.com

## Tech

- Zero-dependency, single-file HTML (`index.html`)
- Hand-written encoders: CRC32, PNG-inside-ICO packaging, store-mode ZIP (with central directory + EOCD)
- Batch upload via drag & drop / file picker / clipboard paste
- Three output modes: full favicon set, single size, multi-size ICO

## Site map

| Path | Page | Status |
|---|---|---|
| `/` | WebP to ICO converter (homepage) | ✅ live |
| `/jpg-to-ico` | JPG to ICO | 🔜 planned |
| `/svg-to-ico` | SVG to ICO | 🔜 planned |
| `/avif-to-ico` | AVIF to ICO | 🔜 planned |
| `/png-to-ico` | PNG to ICO | 🔜 planned |

## Testing

```bash
node test/test_core.cjs
```

Smoke tests extract the pure functions from `index.html` and verify CRC32 vectors, ICO header/directory structure, PNG signatures and ZIP layout (cross-validated with Python `zipfile`).

## Deploy

Zero config on Vercel: import this repo, Framework Preset = **Other**, Root Directory = repo root. Deployments trigger on every push to `main`.
