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
| `/jpg-to-ico` | JPG to ICO | ✅ live |
| `/svg-to-ico` | SVG to ICO | ✅ live |
| `/avif-to-ico` | AVIF to ICO | 🔜 planned |
| `/png-to-ico` | PNG to ICO | 🔜 planned |

## Changelog

- **v1.5** – Add GA4 conversion event tracking: `convert_success`, `convert_failed`, `download_zip`, `download_ico`, `copy_code`, `copy_manifest` on all live pages. Test script now targets the engine script block by `crc32` marker (GA4 inline script is ignored).
- **v1.4** – Add Google Analytics 4 (`G-QMF2LHLL2B`) to all live pages for traffic measurement.
- **v1.3** – Add SVG to ICO page + SVG width/height guard.
- **v1.2** – Add JPG to ICO page + navigation fixes.
- **v1.1** – Brand favicon set, sitemap, canonical aligned to `www.faviconpal.com`.
- **v1.0** – WebP to ICO MVP.

## Testing

```bash
node test/test_core.cjs
```

Smoke tests extract the pure functions from `index.html` and verify CRC32 vectors, ICO header/directory structure, PNG signatures and ZIP layout (cross-validated with Python `zipfile`).

## Deploy

Zero config on Vercel: import this repo, Framework Preset = **Other**, Root Directory = repo root. Deployments trigger on every push to `main`.
