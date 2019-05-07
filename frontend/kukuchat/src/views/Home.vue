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
import Restore from '@/components/Restore.vue'
import { store } from '@/store';
import { constants } from 'crypto';

export default {

    name: 'home',
    components: {
        Login,
        Signup,
        Info,
        Restore
    },
    data() {
        return {
            dynamicComponent: Login
        }
    },
    beforeMount() {
            store.getters.socket = new WebSocket("ws://localhost:8000/ws/chat/");
            store.getters.socket.onopen = () => {
               store.getters.socket.onmessage = ({data}) => {
                    data = JSON.parse(data);
                    console.log(data);
                    if (data.action === 'login' && data.status === 'ok') {
                        this.$router.push({name: 'chat'})
                    }

                    if (data.action === 'login' && data.status === 'error') {
                        M.toast({html: 'Logging failed. Invalid login or password', classes: 'red darken-2'})
                    }

                    if (data.action === 'login' && data.status === 'ok') {
                        this.$router.push({name: 'chat'})
                    }

                    if (data.action === 'am_i_logged' && data.is_logged) {
                        this.$router.push({name: 'chat'})
                    }
                };
                let data = {
                    action: 'am_i_logged'
                }
                store.getters.socket.send(JSON.stringify(data));
            };
    },
    mounted() {
        if (store.getters.socket.readyState !== 0) {
            let data = {
                action: 'am_i_logged'
            }
            store.getters.socket.send(JSON.stringify(data));
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

