<template>
    <div class="valign-wrapper row login-box">
        <div class="col m5 l6 pull-l1 center-align left-side">
            <h5>CooCoo chat for everyone</h5>
            <p>Keep all your favorite communication chats in one service</p>
            <img class="main-img" src="../../public/image.png" alt="image">
        </div>
        <div class="col card s12 m5 pull-m1 l4 pull-l1">
            <form>
                <div class="card-content">
                    <span class="card-title center-align">Log In</span>
                    <div class="row">
                        <div class="input-field col s12">
                            <label for="login">Login</label>
                            <input type="text" v-model="username" @keyup="editLogin()" :class="validateLogin" name="login" id="login"/>
                        </div>
                        <div class="input-field col s12">
                            <label for="password">Password </label>
                            <input :type="passwordFieldType" @keyup="editPassword()" v-model="password" :class="validatePassword" name="password" id="password"/>
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
    </div>
</template>

<script>

import {http} from '../plugins/axios'

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
                    username: this.username,
                    password: this.password,
                }

                http.post('/api/login/', data)
                .then(res => {
                    M.toast({html: 'Logging successful', classes: 'green darken-2'})
                })
                .catch(err => {
                    M.toast({html: 'Logging failed', classes: 'red darken-2'})
                });
            }
        }
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

.login-box {
  height: 100%;
  margin: auto;
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

@media only screen and (max-width: 600px) {
    .card {
        box-shadow: none;
    }

    .left-side {
        display: none;
    }
}

@media only screen and (max-width: 1000px) and (min-width: 600px) {
    .main-img {
        width: 250px;
        height: 250px;
    }
}

</style>
