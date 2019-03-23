<template>
  <div id="app" :class="{'dark': isDark}">
    <router-view/>
  </div>
</template>

<script>
export default {
  data() {
    return {
      isDark: false
    }
  }
}
</script>

<style>

html,body {
  height:100%;
  background-color: #fafafa;
  min-width: 365px;
}

#app {
  height: 100%;
  overflow: hidden;
}

.dark {
  background-color: #121212;
  color: rgba(255, 255, 255, 0.90);
  
}

.dark  input {
  color: rgba(255, 255, 255, 0.70);
}

.dark > .login-box > .card {
  background-color: #272727;
}

#toast-container {
  position: fixed;
  top: 50px;
}

</style>
