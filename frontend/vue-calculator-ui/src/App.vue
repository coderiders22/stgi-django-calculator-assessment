<!-- src/App.vue -->
<template>
  <div id="app">
    <Navbar />
    <router-view />
  </div>
</template>

<script>
import Navbar from './components/Navbar.vue'   // ← path check karo

export default {
  components: {
    Navbar
  }
}
</script>