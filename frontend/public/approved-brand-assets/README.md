# Approved Brand Assets

Place the **approved KPMG logo files** here with these exact filenames so the app
picks them up automatically (referenced by `src/design-system/KpmgLogo.tsx`):

| Variant | Filename | Used where |
|---------|----------|------------|
| RGB (default, blue) | `kpmg-rgb.png` | Light surfaces / default |
| White | `kpmg-white.png` | Dark surfaces (the navy sidebar) |
| Black | `kpmg-black.png` | Mono / print contexts |

Notes:
- PNG with a transparent background is expected. SVG is fine too — if you supply
  SVGs, change the extensions in `KpmgLogo.tsx` (`.png` → `.svg`).
- Do not recreate or redraw the KPMG logo. Use only these approved supplied files.
- Until the files are present, the app renders a plain "KPMG" text fallback.

