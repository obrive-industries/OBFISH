<template>
  <router-view />
</template>

<script setup>
// 使用 Vue Router 来管理页面
</script>

<style>
/* Obrive Design Tokens */
:root {
  --obrive-primary: #074139;
  --obrive-primary-dark: #052e28;
  --obrive-primary-light: #0d5c52;
  --obrive-accent: #a2f1df;
  --obrive-accent-light: #caede5;
  --obrive-accent-gradient: linear-gradient(135deg, #a2f1df 0%, #34d399 50%, #059669 100%);
  --obrive-bg: #A2F1DF;
  --obrive-surface: #FFFFFF;
  --obrive-border: rgba(7, 65, 57, 0.18);
  --obrive-border-focus: rgba(7, 65, 57, 0.35);
  --obrive-shadow: 0 4px 20px -2px rgba(7, 65, 57, 0.08);
}

/* 全局样式重置 */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  scrollbar-width: thin;
  scrollbar-color: rgba(7, 57, 51, 0.25) transparent;
}

body {
  background-color: #A2F1DF;
  color: #074139;
}

#app {
  font-family: 'Space Grotesk', 'Inter', system-ui, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #074139;
  background-color: var(--obrive-bg);
  min-height: 100vh;
}

/* Obrive Slim-line minimalist custom scrollbar everywhere */
::-webkit-scrollbar {
  width: 5px;
  height: 5px;
}

::-webkit-scrollbar-track {
  background: transparent;
}

::-webkit-scrollbar-thumb {
  background-color: rgba(7, 57, 51, 0.25);
  border-radius: 9999px;
  transition: background-color 0.2s ease;
}

::-webkit-scrollbar-thumb:hover {
  background-color: rgba(7, 57, 51, 0.5);
}

/* 全局按钮样式 */
button {
  font-family: inherit;
}
</style>
