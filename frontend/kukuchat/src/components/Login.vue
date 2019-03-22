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
                            <input type="text" class="validate" name="login" id="login" required="" aria-required="true"/>
                        </div>
                        <div class="input-field col s12">
                            <label for="password">Password </label>
                            <input type="password" class="validate" name="password" id="password" required="" aria-required="true"/>
                        </div>
                        <div class="col s12">
                            <button class="btn green darken-2 waves-effect waves-light col s3">Log In </button>
                            <a @click="signup()" class="btn deep-orange darken-2 waves-effect waves-light col s3">Sign Up </a>
                            <a @click="restore()" class="restore">Forgot password?</a>
                        </div>
                    </div>
                </div>
            </form>
        </div>
    </div>
</template>

<script>
export default {
  name: 'Login',
  methods: {
      signup() {
          this.$parent.dynamicComponent = 'signup';
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
  min-width: 365px;
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
