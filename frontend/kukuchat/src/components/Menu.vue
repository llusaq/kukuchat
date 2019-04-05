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
            <a class="settings-btn" @click="logout()">Log out</a>
        </div>
         <div class="back-btn" @click="toContacts()" v-if="currentChat != '' && width <= 600">  
                <i class="material-icons">arrow_back</i>
            </div>
        <a class="col l9 m8 s12 menu-el" v-if="currentChat != '' && width <= 600">
           
            {{ currentChat }}
        </a>
        <a class="col l9 m8 s12 menu-el" v-else-if="width > 600">
            {{ currentChat }} 
        </a>
        <div id="add-account" class="modal">
             <div class="modal-header">
                <h4>Add account</h4>
                <a class="modal-close"><i class="material-icons small left">clear</i></a>
            </div>
            <div class="modal-content">
                <div class="row">
                    <div class="col l2 m2">
                        <img src="@/assets/messenger.png" alt="messenger">
                        <p> <b>Messenger</b> </p>
                    </div>
                    <div class="col l2 m2">
                        <img src="@/assets/skype.png" alt="skype">
                        <p> <b>Skype</b> </p>
                    </div>
                    <div class="col l2 m2">
                        <img src="@/assets/viber.png" alt="viber">
                        <p> <b>Viber</b> </p>
                    </div>
                    <div class="col l2 m2">
                        <img src="@/assets/gmail.png" alt="gmail">
                        <p> <b>Gmail</b> </p>
                    </div>
                    <div class="col l2 m2">
                        <img src="@/assets/telegram.png" alt="telegram">
                        <p> <b>Telegram</b> </p>
                    </div>
                </div>
               
                <div class="clear"></div>
            </div>
           
        </div>
        
    </div>
</template>

<script>
import { store } from '@/store'

export default {
    name: 'dropdownmenu',
    data() {
        return {
            icon: 'menu',
            style: 'white',
            opened: false,
            showModal: false,
            width: window.innerWidth,
        }
    },
    mounted() {
        $('#add-account').modal();
    },
    methods: {
        settings() {
            this.icon = this.icon === 'menu' ? 'clear' : 'menu';
            this.opened = !this.opened;
        },
        logout() {
             let data = {
                 action: 'logout'
                 }
            store.getters.socket.send(JSON.stringify(data));
            store.getters.socket.close();
            store.getters.socket = undefined;
            this.$router.push({name: 'home'})
        },
        toContacts() {
            this.$parent.currentChat = '';
        }
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

.modal-header {
    padding: 10px 0;
}

.modal-header h4 {
    display: inline-block;
}

.modal {
    overflow: hidden;
    cursor: default;
}

.modal-close {
    float: right;
}

.modal-content .col {
    margin: 20px 1.6%;
    position: relative;
    transition: all 0.2s ease;
    display: table;
    cursor: pointer;
}

.modal-content .col:hover img {
    max-width: 130%;
    height: auto;
    margin-left: -15%;
    margin-top: -15%;
}

.col img {
    max-width: 100%;
    height:auto;
    transition: all 0.2s;
}

.modal-content {
    padding: 20px;
    height: 230px;
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


