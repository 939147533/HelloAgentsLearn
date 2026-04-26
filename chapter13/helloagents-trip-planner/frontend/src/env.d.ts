/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_AMAP_WEB_JS_KEY: string
  // 如果还有其他 VITE_ 开头的环境变量，也可以在这里补充
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}