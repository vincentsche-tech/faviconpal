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
| `/jpg-to-ico/` | JPG to ICO | ✅ live |
| `/svg-to-ico/` | SVG to ICO | ✅ live |
| `/avif-to-ico/` | AVIF to ICO | ✅ live |
| `/contact/` | Contact page | ✅ live |
| `/privacy/` | Privacy policy | ✅ live |
| `/png-to-ico/` | PNG to ICO | 🔜 planned |
| `/mp4-to-webp/` | MP4 to WebP | 🔜 planned |
| `/webp-compressor/` | WebP Compressor | 🔜 planned |

## Changelog

- **v1.6.2** – Fix SEO foundation: add missing `/contact/` and `/privacy/` pages (were linked in footer but returned 404), add `robots.txt`, update `sitemap.xml` to include all 6 live URLs, normalize all internal links to trailing-slash form.
- **v1.6** – Add AVIF to ICO page (page 4 of the favicon matrix) + unified tool-matrix block on all four pages (live tools get LIVE badge & link, planned tools show SOON in gray, no more dead links). AVIF page copy layer: honest browser-compatibility section (Chrome/Edge 85+, Firefox 93+, Safari 16+), AVIF-is-already-lossy FAQ, "is AVIF good for favicons" FAQ.
- **v1.5.1** – Fix `i is not defined` runtime bug in `renderResults()` on all three pages (map callback was missing index parameter; caused conversion result rendering to fail).
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
