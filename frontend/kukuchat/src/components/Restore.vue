<template>
    <div class="col card s12 m5 pull-m1 l4 pull-l1">
        <form>
            <div class="card-content">
                <span class="card-title center-align">Reset Password</span>
                <div class="row">

                    <div class="input-field col s12">
                        <label for="email">Email </label>
                        <input type="email" v-model="email" @keyup="editEmail()" :class="validateEmail" name="email"
                               id="email"/>
                    </div>
                    <div class="col s12">
                        <a @click="restore()" class="btn green darken-2 waves-effect waves-light col s4">Reset now </a>
                        <a @click="back()" class="btn deep-orange darken-2 waves-effect waves-light col s4">Go
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
            back() {
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

            restore() {
                if (this.email === '') {
                    this.validateEmail = 'invalid'
                    M.toast({html: 'Email must not be empty', classes: 'red darken-2'})
                } else if (!this.validEmail(this.email)) {
                    this.validateEmail = 'invalid'
                    M.toast({html: 'Email is not correct', classes: 'red darken-2'})
                } else {
                    let data = {
                        username: this.username,
                        password: this.password,
                        email: this.email
                    }


                }
            },
        }
    }
</script>

<style scoped>

    .active {
        color: #1565c0 !important;
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
