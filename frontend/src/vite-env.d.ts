/// <reference types="vite/client" />

interface ImportMetaEnv {
  /** Base URL of the governed backend-for-frontend. Empty = same-origin. */
  readonly VITE_API_BASE_URL?: string;
  /** Set to "false" to disable the MSW mock worker in development. */
  readonly VITE_USE_MOCKS?: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}

declare module "*.module.css" {
  const classes: { readonly [key: string]: string };
  export default classes;
}
