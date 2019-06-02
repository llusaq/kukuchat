<template>
    <div class="row settings">
        <a class="col l3 m4 s12 menu-el" :class="{opened: opened}" @click="settings()" v-if="currentChat == '' && width <= 600">
            <i class="material-icons left">{{ icon }}</i>
            CooCoo
        </a>
        <a class="col l3 m4 s12 menu-el" :class="{opened: opened}" @click="settings()" v-else-if="width > 600">
            <i class="material-icons left">{{ icon }}</i>
            CooCoo
        </a>
        <div class="col card l3 m4 s12" v-if="opened">
            <a class="settings-btn modal-trigger" href="#add-account" @click="settings()">Add account</a>
            <a class="settings-btn modal-trigger" href="#settings" @click="settings()">Settings</a>
            <a class="settings-btn" @click="logout()">Log out</a>
        </div>
        <div class="back-btn" @click="toContacts()" v-if="currentChat != '' && width <= 600">  
            <i class="material-icons">arrow_back</i>
        </div>
        <a class="col l9 m8 s12 menu-el" v-if="currentChat != '' && width <= 600">
           
            {{ currentChat.name }}
        </a>
        <a class="col l9 m8 s12 menu-el" v-else-if="width > 600">
            {{ currentChat.name }} 
        </a>
            <AddAccount></AddAccount>
            <Settings></Settings>
            <Premium></Premium>
    </div>
</template>

<script>
import { store } from '@/store'
import AddAccount from './AddAccount'
import Settings from './Settings'
import Premium from './Premium'

export default {
    name: 'dropdownmenu',
    components: {
      AddAccount,
      Settings,
      Premium
    },
    data() {
        return {
            icon: 'menu',
            style: 'white',
            opened: false,
            width: window.innerWidth,
        }
    },
    mounted() {
        $('#add-account').modal();
        $('#settings').modal();
        $('#premium').modal();
    },
    methods: {
        settings() {
            this.icon = this.icon === 'menu' ? 'clear' : 'menu';
            this.opened = !this.opened;
        },
        logout() {
            this.$router.push({name: 'home'})
            let data = {
                action: 'logout'
            }
            store.getters.socket.send(JSON.stringify(data));
            store.getters.socket.close();
            store.getters.socket = undefined;
        },
        toContacts() {
            this.$parent.currentChat = '';
        },
    },
    props: ['currentChat'],
}
</script>

<style scoped>

.clear {
    clear: both;
}

.settings {
    background-color: white;
    box-shadow: 0 4px 2px -2px rgba(0,0,0,0.12);
    text-align: center;
    color: rgba(0,0,0,0.87);
    cursor: pointer;
    height: 50px;
    position: relative;
}

i {
    transition: 0.5ms;
    transition-delay: 1s;
}

a {
    user-select: none;
    color: rgba(0,0,0,0.80);
}

.menu-el {
    padding: 15px;
    height: 55px;
}

.menu-el:hover {
    background-color: #e0e0e0;
}

.row {
    height: auto;
    margin-bottom: 0;
}

.card {
    position: absolute;
    top: 55px;
    box-shadow: 0px 4px 2px -2px rgba(0,0,0,0.12);
    background-color: white;
    z-index: 999;
    margin: 0;
    padding: 0;
}

.settings-btn {
    width: 100%;
    height: 30px;
    display: inline-table;
    padding: 10px 0;
    line-height: 28px;
}

.settings-btn:hover {
    background-color: #eeeeee;
}

.opened {
    background-color: #e0e0e0;
}

.back-btn {
    height: 100%;
    position: absolute;
    left: 0px;
    top: 0px;
    cursor: pointer;
    padding: 15px;
    color: rgba(255, 255, 255, 0.90);
}

.back-btn:hover {
    background-color: #616161;
}

</style>


