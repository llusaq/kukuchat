<template>
    <div id="add-account" class="modal">
        <div class="modal-header">
            <h4>Add {{ choosenAccount }} account </h4>
            <span class="close-form" @click="close()" v-if="choosenAccount !== ''"><i class="material-icons small left">clear</i></span>
            <a class="modal-close" v-if="choosenAccount === ''"><i class="material-icons small left">clear</i></a>
        </div>
        <div class="modal-content">
            <div class="row" v-if="choosenAccount === ''">
                <div v-if="!messenger" class="col l2 m2" @click="massengerLogin()">
                    <img src="@/assets/messenger.png" alt="messenger">
                    <p> <b>Messenger</b> </p>
                </div>
                <div v-if="!skype" class="col l2 m2" @click="accountLogin('Skype')">
                    <img src="@/assets/skype.png" alt="skype">
                    <p> <b>Skype</b> </p>
                </div>
                <div v-if="!viber" class="col l2 m2" @click="accountLogin('Viber')">
                    <img src="@/assets/viber.png" alt="viber">
                    <p> <b>Viber</b> </p>
                </div>
                <div v-if="!gmail" class="col l2 m2" @click="accountLogin('Gmail')">
                    <img src="@/assets/gmail.png" alt="gmail">
                    <p> <b>Gmail</b> </p>
                </div>
                <div v-if="!telegram" class="col l2 m2" @click="accountLogin('Telegram')">
                    <img src="@/assets/telegram.png" alt="telegram">
                    <p> <b>Telegram</b> </p>
                </div>
            </div>
            <div class="row" v-if="choosenAccount !== ''">
                 <div class="input-field col s12" v-if="usernameField">
                        <label for="login">{{ usernameHelp }}</label>
                        <input type="text" v-model="username" @keyup.enter="login()" @keyup="editLogin()" :class="validateLogin" name="login" id="login"/>
                </div>
                <div class="input-field col s12" v-if="passwordField">
                    <label for="password">{{ passwordHelp }} </label>
                    <input :type="passwordFieldType"  @keyup.enter="login()" @keyup="editPassword()" v-model="password" :class="validatePassword" name="password" id="password"/>
                    <i class="material-icons" @click="switchVisibility()">{{ passwordFieldText }}</i>
                </div>
                <div class="col s4 logbtn">
                    <a @click="login()" class="btn green darken-2 waves-effect waves-light col s12">Log In </a>
                </div>
            </div>
        </div>
        <Preloader v-if="preload"></Preloader>
    </div>
</template>

<script>

import { store } from '@/store'
import Preloader from './Preloader'
import { close } from 'fs';
import { mapState } from 'vuex';

export default {
    name: 'addAccount',
    components: {
      Preloader  
    },
    data() {
        return {
            choosenAccount: '',
            username: '',
            password: '',
            passwordFieldType: 'password',
            passwordFieldText: 'visibility_off',
            validateLogin: '',
            validatePassword: '',
            usernameField: false,
            usernameHelp: '',
            passwordField: false,
            passwordHelp: '',
            preload: false,
            messenger: false,
            skype: false,
            viber: false,
            gmail: false,
            telegram: false,
        }
    },
    computed: mapState([
        'isChat'
    ]),
    methods: {
        editLogin() {
            this.validateLogin = 'valid'
        },
        editPassword() {
            this.validatePassword = 'valid'
        },
        switchVisibility() {
            this.passwordFieldType = this.passwordFieldType === 'password' ? 'text' : 'password'
            this.passwordFieldText= this.passwordFieldText === 'visibility' ? 'visibility_off' : 'visibility'
        },
        close() {
            this.choosenAccount = ''
        },
        massengerLogin() {
            this.choosenAccount = 'Messenger';
            let data = {
                    action: 'provider_facebook_get_required_credentials'
                }
            store.getters.socket.send(JSON.stringify(data));
            store.getters.socket.onmessage = ({data}) => {
                data = JSON.parse(data)
                if (data.password) {
                    this.passwordField = true;
                    this.passwordHelp = data.password.help;
                }
                if (data.username) {
                    this.usernameField = true;
                    this.usernameHelp = data.username.help;
                }
            };
        },
        login() {
            this.preload = true
            let data = {
                action: 'provider_facebook_login',
                username: this.username,
                password: this.password,
            }
            store.getters.socket.send(JSON.stringify(data));
            store.getters.socket.onmessage = ({data}) => {
                data = JSON.parse(data)
                console.log(data)
                if (data.status === 'error') {
                    M.toast({html: 'Logging failed. Invalid login or password', classes: 'red darken-2'})
                    this.preload = false;
                }
                if (data.status === 'ok') {
                    this.preload = false;
                    this.close();
                    M.toast({html: 'Messenger added', classes: 'green darken-2'})
                    this.messenger = true;
                    store.commit('setChat');
                }
            };
        }

    }
}
</script>

<style scoped>

.row {
    min-height: 200px;
}

a, span {
    user-select: none;
    color: rgba(0,0,0,0.80);
    cursor: pointer;
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
}

.close-form {
    float: right;
}

i {
    position: absolute;
    top: 15px;
    right: 20px;
    cursor: pointer;
    z-index: 9999;
}

.active {
    color: #1565c0  !important;
}

input:focus, .valid {
    border-bottom: 1px solid #1565c0 !important;
    box-shadow: 0 1px 0 0 #1565c0 !important;
}

.logbtn {
    float: right;
    margin: 0 !important;
}

.logbtn a {
    color: #f5f5f5;
    margin: 0 !important;
}


</style>
