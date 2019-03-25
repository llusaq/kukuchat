<template>
  <div id="app" :class="{'dark': isDark}">
    <router-view/>
  </div>
</template>

<script>
export default {
  data() {
    return {
      isDark: false,
      socket: ''
    }
  },
  methods: {
  }

}
</script>

<style>

html,body {
  height:100%;
  background-color: #fafafa;
  min-width: 365px;
}

#app {
  height: 100%;
  overflow: hidden;
  user-select: none;
}

.dark {
  background-color: #121212;
  color: rgba(255, 255, 255, 0.90);
}

.dark  input {
  color: rgba(255, 255, 255, 0.70);
}

.dark > .login-box > .card {
  background-color: #272727;
}

.dark > .wrapper > .settings > .opened {
  background-color: #333333 !important;
}

.dark > .wrapper > .settings > .col {
  background-color: #272727;
  color: rgba(255, 255, 255, 0.90);
}

.dark > .wrapper > .settings > .col a {
  color: rgba(255, 255, 255, 0.90);
}

.dark > .wrapper > .settings > .col > .settings-btn:hover {
  background-color: #333333;
}

.dark > .wrapper > .settings > .menu-el {
  background-color: #272727;
  color: rgba(255, 255, 255, 0.90);
}

.dark > .wrapper > .settings > .menu-el:hover {
  background-color: #333333;
}

.dark > .wrapper > .chat > .contacts {
  background-color: #1c1c1c;
}

.dark > .wrapper > .chat > .contacts span {
  color: rgba(255, 255, 255, 0.85);
}

.dark > .wrapper > .chat > .contacts > .scroll > li > .info > span:last-child {
  color: rgba(255, 255, 255, 0.65);
}

.dark > .wrapper > .chat > .contacts li:hover {
  background-color: #333333;
}

.dark > .wrapper > .chat > .contacts input {
  background-color: #121212;
  border: 1px solid #333333 !important;
  color: rgba(255, 255, 255, 0.90);
}

.dark > .wrapper > .chat > .contacts > .nav-wrapper > .input-field > .active i {
    color: rgba(255, 255, 255, 0.90) !important;
}

.dark > .wrapper > .chat > .contacts input:focus+label {
  color: #bdbdbd;
}

.dark > .wrapper > .chat > .contacts > .scroll > .clicked {
    background-color: #333333 !important;
}

.dark > .wrapper > .chat > .contacts ::-webkit-scrollbar-thumb {
  background: #424242; 
  border-radius: 10px;
}

/* Handle on hover */
.dark > .wrapper > .chat > .contacts ::-webkit-scrollbar-thumb:hover {
  background: #616161; 
}

.dark > .wrapper > .settings > .modal {
  background-color: #272727;
  color: rgba(255, 255, 255, 0.90);
}

.dark > .wrapper > .settings > .modal i {
  color: #bdbdbd;
}

#toast-container {
  position: fixed;
  top: 50px;
  height: fit-content;
}

</style>
