<template>
    <div class="col card s12 m5 pull-m1 l4 pull-l1">
        <form @submit.prevent="pingServer">
            <div class="card-content">
                <span class="card-title center-align">Log In</span>
                <div class="row">
                    <div class="input-field col s12">
                        <label for="login">Login</label>
                        <input type="text" v-model="username" @keyup.enter="login()" @keyup="editLogin()" :class="validateLogin" name="login" id="login"/>
                    </div>
                    <div class="input-field col s12">
                        <label for="password">Password </label>
                        <input :type="passwordFieldType"  @keyup.enter="login()" @keyup="editPassword()" v-model="password" :class="validatePassword" name="password" id="password"/>
                        <i class="material-icons" @click="switchVisibility()">{{ passwordFieldText }}</i>
                    </div>
                    <div class="col s12">
                        <a @click="login()" class="btn green darken-2 waves-effect waves-light col s4">Log In </a>
                        <a @click="signup()" class="btn deep-orange darken-2 waves-effect waves-light col s4">Sign Up </a>
                        <a @click="restore()" class="restore">Forgot password?</a>
                    </div>
                </div>
            </div>
        </form>
    </div>
</template>

<script>

import {http} from '../plugins/axios'
import store from '../store'

export default {
    name: 'Login',
    data() {
        return {
        username: '',
        password: '',
        passwordFieldType: 'password',
        passwordFieldText: 'visibility_off',
        validateLogin: '',
        validatePassword: '',
        socket: ''
        }
    },
    methods: {
        signup() {
            this.$parent.dynamicComponent = 'signup';
        },
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
        login() {
             if (this.username === '') {
                this.validateLogin = 'invalid'
                M.toast({html: 'Login must not be empty', classes: 'red darken-2'})
            } 
            else if (this.password === '') {
                this.validatePassword = 'invalid'
                M.toast({html: 'Password must not be empty', classes: 'red darken-2'})
            }
            else { 
                let data = {
                    action: 'login',
                    username: this.username,
                    password: this.password,
                }

                this.socket.send(JSON.stringify(data));

                data = {
                    action: 'am_i_logged'
                }
                this.socket.send(JSON.stringify(data));

            }
        },
        connect() {
            this.socket = new WebSocket("ws://localhost:8000/ws/chat/");
            this.socket.onopen = () => {
                console.log("connected");   
                this.socket.onmessage = ({data}) => {
                    data = JSON.parse(data)
                    console.log(data)
                    if (data.is_logged) {
                        this.$router.push({name: 'chat'})
                    } 
                    if (data.status === 'error') {
                        M.toast({html: 'Logging failed. Invalid login or password', classes: 'red darken-2'})
                    }
                };
                let data = {
                    action: 'am_i_logged'
                }
                this.socket.send(JSON.stringify(data));
            };
        },
        disconnect() {
            this.socket.close();
        },
        sendMessage(data) {
            console.log('sent')
            this.socket.send(data)
        }
    },
    beforeMount() {
        this.connect();
    },
    mounted() {
       
    }
}
</script>

<style scoped>

.active {
    color: #1565c0  !important;
}

input:focus, .valid {
    border-bottom: 1px solid #1565c0 !important;
    box-shadow: 0 1px 0 0 #1565c0 !important;
}


a {
    color: #1565c0;
    cursor: pointer;
}

a:hover {
    text-decoration: underline;
}

.btn {
    text-transform: none;
    text-decoration: none !important;
    color: #f5f5f5;
    margin-right: 10px;
}

.main-img {
    width: 450px;
    height: 450px;
}

.restore {
    font-size: 12px;
    margin: 9px 0 0 0;
    display: inline-block
}

i {
    position: absolute;
    top: 15px;
    right: 20px;
    cursor: pointer;
    z-index: 9999;
}

</style>
