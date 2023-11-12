<script setup>

import { RouterLink, RouterView } from 'vue-router'

console.clear();
console.log("%cLoaded!!!", "color: #22ff22; font-size: 24px");
</script>

<template>

  <div class="wrapper">
    <RouterView />
  </div>

</template>

<style scoped>
.web-title {
  font-size: 22px;
  font-weight: bolder;
  padding-bottom: 12px;
  color: var(--color-heading)
}

.sidebar-link {
  font-weight: bold;
}

.sidebar-separator {
  margin-top: 10px;
  margin-left: 8px;
  margin-bottom: 10px;
}

.top-nav {
  display: flex;
  width: 100%;
  flex-direction: column;
}

a {
  width: 100%;
}
.wrapper {
  flex-grow: 1;
  flex-shrink: 0;
  min-height: 100vh;
}

@media (min-width: 1024px) {
  .sidebar {
    min-width: 240px;
    padding: 16px;
    height: 100%;
  }
}
</style>
