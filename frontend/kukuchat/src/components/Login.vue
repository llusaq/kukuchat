<template>
    <div class="valign-wrapper row login-box">
        <div class="col card hoverable s12 m6 pull-m3 l4 pull-l4">
            <form>
                <div class="card-content">
                    <span class="card-title center-align">Log In</span>
                    <div class="row">
                        <div class="input-field col s12">
                            <label for="login">Login</label>
                            <input type="text" class="validate" name="login" id="login" />
                        </div>
                        <div class="input-field col s12">
                            <label for="password">Password </label>
                            <input type="password" class="validate" name="password" id="password" />
                        </div>
                    </div>
                </div>
                <div class="card-action right-align">
                    <button type="button" class="btn blue waves-effect waves-light">Forgot password? </button>
                    <button type="button" class="btn green waves-effect waves-light">Login </button>
                </div>
            </form>
        </div>
    </div>
</template>

<script>
export default {
  name: 'Login'
}
</script>

<style scoped>



.active {
    color: #3498db !important;
}

input:focus {
    border-bottom: 1px solid #3498db !important;
    box-shadow: 0 1px 0 0 #3498db !important;
}

.login-box {
  height: 100%;
  margin: auto;
}

.blue {
    margin-right: 20px;
}


@media only screen and (max-width: 600px) {
  .card {
      box-shadow: none;
  }
}

</style>
