<template>
        <div class="col card s12 m5 pull-m1 l4 pull-l1">
            <form >
                <div class="card-content">
                    <span class="card-title center-align">Sign Up</span>
                    <div class="row">


                        <div class="input-field col s12">
                            <label for="email">Email </label>
                            <input type="email" v-model="email" @keyup="editEmail()" :class="validateEmail" name="email"
                                   id="email"/>
                        </div>

                        <div class="input-field col s12">
                            <label for="login">Login</label>
                            <input type="text" @keyup="editLogin()" v-model="username" :class="validateLogin" name="login" id="login"/>
                        </div>
                        <div class="input-field col s12">
                            <label for="password">Password </label>
                            <input type="password" @keyup="editPassword()" v-model="password" :class="validatePassword" name="password" id="password"/>

                        </div>
                        <div class="input-field col s12">
                            <label for="password2">Confirm password </label>
                            <input type="password" @keyup="editPassword2()" v-model="password2" :class="validatePassword2" name="password2" id="password2"/>
                        </div>

                        <div class="col s12">

                            <a @click="signup()" class="btn green darken-2 waves-effect waves-light col s4">Sign Up </a>

                            <a @click="login()" class="btn deep-orange darken-2 waves-effect waves-light col s4">Go
                                back </a>
                        </div>
                    </div>
                </div>
            </form>
        </div>
</template>

<script>

import {http} from '../plugins/axios'

export default {
    name: 'Signup',
    data() {
        return {
            username: '',
            password: '',
            password2: '',
            email: '',
            validateLogin: '',
            validatePassword: '',
            validatePassword2: '',
            validateEmail: ''
        }
    },
    methods: {
        login() {
            this.$parent.dynamicComponent = 'login';
        },
        editLogin() {
            this.validateLogin = 'valid'
        },
        editPassword() {
            this.validatePassword = 'valid'
        },
        editPassword2() {
            this.validatePassword2 = 'valid'
        },
        editEmail() {
            this.validateEmail = 'valid'
        },
        validEmail(email) {
            var re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
            return re.test(email);
        },
        signup() {
            if (this.username === '') {
                this.validateLogin = 'invalid'
                M.toast({html: 'Login must not be empty', classes: 'red darken-2'})
            }
            else if (this.password === '') {
                this.validatePassword = 'invalid'
                M.toast({html: 'Password must not be empty', classes: 'red darken-2'})
            }
            else if (this.password2 === '') {
                this.validatePassword2 = 'invalid'
                M.toast({html: 'Accept password must not be empty', classes: 'red darken-2'})
            }
            else if (this.password != this.password2) {
                this.validatePassword2 = 'invalid'
                M.toast({html: 'Passwords doesn`t match', classes: 'red darken-2'})
            }
            else if (this.email === '') {
                this.validateEmail = 'invalid'
                M.toast({html: 'Email must not be empty', classes: 'red darken-2'})
            }
            else if (!this.validEmail(this.email)) {
                this.validateEmail = 'invalid'
                M.toast({html: 'Email is not correct', classes: 'red darken-2'})
            } else {
                let data = {
                    username: this.username,
                    password: this.password,
                    email: this.email
                }

                http.post('/api/register/', data)
                    .then(res => {
                        M.toast({html: 'Registration successful', classes: 'green darken-2'})
                        this.$parent.dynamicComponent = 'login';
                    })
                    .catch(err => {
                        M.toast({html: 'Registration failed', classes: 'red darken-2'})
                        console.log(err)
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
    display: inline-block;
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
