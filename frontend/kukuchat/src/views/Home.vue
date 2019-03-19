<template>
  <keep-alive>
    <component :is="dynamicComponent"></component>
  </keep-alive>
</template>

<script>
import Login from '@/components/Login.vue'
import Signup from '@/components/Signup.vue'

export default {
  name: 'home',

  components: {
    Login,
    Signup
  },
  
  data() {
    return {
       dynamicComponent: Login
    }
  }
}
</script>
