<template>
    <div class="valign-wrapper row login-box">
        <Info></Info>
        <component :is="dynamicComponent"></component>
    </div>
</template>

<script>
import Login from '@/components/Login.vue'
import Signup from '@/components/Signup.vue'
import Info from '@/components/Info.vue'

export default {
    name: 'home',
    components: {
        Login,
        Signup,
        Info
    },
    data() {
        return {
            dynamicComponent: Login
        }
    }
}
</script>

<style>

.login-box {
  height: 100%;
  margin: auto;
}

</style>

