# Accessibility Standard

Target: **WCAG 2.2 AA**.

## Implemented

- Skip-to-content link (`src/app/App.tsx`).
- Semantic landmarks: `nav[aria-label="Primary"]`, `main`, `aside[aria-label="Agent chat"]`,
  and labelled `section` regions.
- Visible focus states via the global `:focus-visible` token ring.
- Accessible names on icon-only buttons (`aria-label`) and decorative icons hidden
  with `aria-hidden`.
- Active navigation item exposes `aria-current="page"`.
- Data tables use `th`/`scope` for row and column headers.
- Chat composer input has an associated label; streamed/agent responses announce
  via an `aria-live="polite"` region.
- Loading and error states use `role="status"` / `role="alert"`.
- Status is conveyed by text/label, not colour alone.
- Reduced-motion support via `prefers-reduced-motion`.

## Pending verification

- Automated axe checks (`tests/accessibility/`).
- Full keyboard walkthrough and screen-reader pass.
- Contrast audit of provisional brand tokens once official values are supplied.
