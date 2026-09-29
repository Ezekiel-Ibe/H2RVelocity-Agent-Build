/**
 * Runtime configuration for backend access.
 *
 * The frontend talks only to a governed backend-for-frontend (BFF). The BFF
 * owns Microsoft Fabric and Microsoft Foundry connections and credentials.
 * The frontend must never hold connection strings, tokens, or secrets.
 */

// Base URL for the governed backend. Empty means same-origin (dev/mock).
export const API_BASE_URL: string = import.meta.env.VITE_API_BASE_URL ?? "";

// Use the MSW mock worker unless explicitly disabled. Defaults to on in dev.
export const USE_MOCKS: boolean =
  import.meta.env.DEV && import.meta.env.VITE_USE_MOCKS !== "false";
