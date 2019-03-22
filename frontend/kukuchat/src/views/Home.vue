<template>
    <component :is="dynamicComponent"></component>
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
