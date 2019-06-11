<template>
  <div id="app" :class="{'dark': isDark}">
    <router-view/>
  </div>
</template>

<script>
import { store } from '@/store'
import { mapState } from 'vuex';

export default {
  data() {
    return {
      socket: ''
    }
  },
  methods: {
  },
  computed: mapState([
      'isDark'
  ])


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

.dark > .wrapper > .settings > .back-btn {
  color: rgba(255, 255, 255, 0.90);
}

.dark > .wrapper > .settings > .back-btn:hover {
  background-color: #616161;
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

.dark > .wrapper > .settings > .modal > .modal-content > .premium a {
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

.dark > .wrapper > .chat > .contacts > .scroll > li.selected {
  background-color: #5c6bc0 !important;
}

.dark > .wrapper > .chat > .contacts > .scroll > li.mergeTo {
  background-color: #3949ab !important;
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

.dark > .wrapper > .chat > ::-webkit-scrollbar-thumb {
  background: #424242; 
  border-radius: 10px;
}

.dark > .wrapper > .chat > .col > .msg_cont_area > ::-webkit-scrollbar-thumb {
  background: #424242; 
  border-radius: 10px;
}

/* Handle on hover */
.dark > .wrapper > .chat > ::-webkit-scrollbar-thumb:hover {
  background: #616161; 
}

.dark > .wrapper > .chat > .col > .msg_cont_area > ::-webkit-scrollbar-thumb:hover {
  background: #616161; 
}

.dark > .wrapper > .settings > .modal {
  background-color: #272727;
  color: rgba(255, 255, 255, 0.90);
}

.dark > .wrapper > .settings > .modal i {
  color: #bdbdbd;
}

.dark > .wrapper > .settings > .modal-overlay {
 background: #1c1c1c !important;
}

.dark > .wrapper> .chat > .contacts > .scroll > li > .icon span {
  background-color: #ff9100;
}

.dark > .wrapper> .chat > .conv > .messages > .msg-container .notMe > .message span {
  background-color: #43a047;
}

.dark > .wrapper> .chat > .conv > .messages > .msg-container .me > .message span {
  background-color: #1e88e5;
}

#toast-container {
  position: fixed;
  top: 50px;
  height: fit-content;
}



</style>
