import { useState } from "react";

/**
 * Renders the APPROVED KPMG brand asset. Supplied files live in
 * public/approved-brand-assets/ (rgb / white / black). Do not recreate the KPMG
 * logo. Falls back to a text mark only if the asset is missing (dev safety).
 */
type Variant = "rgb" | "white" | "black";

const srcByVariant: Record<Variant, string> = {
  rgb: "/approved-brand-assets/KPMG_NoCP_RGB.png",
  white: "/approved-brand-assets/KPMG_NoCP_White.png",
  black: "/approved-brand-assets/KPMG_NoCP_Black.png",
};

const fallbackColor: Record<Variant, string> = {
  rgb: "#00338d",
  white: "#ffffff",
  black: "#0f1b3d",
};

export function KpmgLogo({
  variant = "rgb",
  height = 28,
  title = "KPMG",
}: {
  variant?: Variant;
  height?: number;
  title?: string;
}) {
  const [failed, setFailed] = useState(false);

  if (failed) {
    return (
      <span
        role="img"
        aria-label={title}
        style={{
          fontWeight: 700,
          fontSize: height * 0.6,
          letterSpacing: 1,
          color: fallbackColor[variant],
        }}
      >
        KPMG
      </span>
    );
  }

  return (
    <img
      src={srcByVariant[variant]}
      alt={title}
      height={height}
      onError={() => setFailed(true)}
      style={{ height, width: "auto", display: "block" }}
    />
  );
}
