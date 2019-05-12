import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export const store = new Vuex.Store({
  state: {
    isDark: false,
    socket: '',
    isChat: false,
    messenger: false,
    skype: false,
    viber: false,
    gmail: false,
    telegram: false,
    usernameField: false,
    usernameHelp: '',
    passwordField: false,
    passwordHelp: '',
    preloader: false,
    addAccountForm: true,
    contacts: [
        {
            id: '',
            name: '',
            provider: '',
            lastMsg: '',
        }
    ],
    messages: [
        {
            content: '',
            time: '',
            provider: '',
            me: false
        }
    ],
  },
  mutations: {
    changeTheme(state) {
      state.isDark = !state.isDark;
    },
    connect: (state, connection ) => {
      state.socket = connection
    },
    setChat (state) {
      state.isChat = true;
    },
    setMessenger (state) {
      state.messenger = true;
    },
    setSkype(state) {
      state.skype = true;
    },
    setUsernameField(state) {
      state.usernameField = true;
    },
    setUsernameHelp(state, vaule) {
      state.usernameHelp = vaule;
    },
    setPasswordField(state) {
      state.passwordField = true;
    },
    setPasswordHelp(state, value) {
      state.passwordHelp = value;
    },
    setPreloader(state, value) {
      state.preloader = value;
    },
    setContacts(state, value) {
      state.contacts = value;
    },
    setMessages(state, value) {
      state.messages = value;
    },
    pushMessage(state, value) {
      state.messages.push(value);
    },
    changeAddAccountForm(state, value) {
      state.addAccountForm = value;
    },
    set(state) {
      state.skype = true;
    },
    set(state) {
      state.skype = true;
    },
    set(state) {
      state.skype = true;
    },
    set(state) {
      state.skype = true;
    },
    set(state) {
      state.skype = true;
    },
    set(state) {
      state.skype = true;
    },
    set(state) {
      state.skype = true;
    },
    set(state) {
      state.skype = true;
    },
    set(state) {
      state.skype = true;
    },
    set(state) {
      state.skype = true;
    },
    



  },
  actions: {

  },
  getters: {
    isDark: state => state.isDark,
    connection: state => state.socket,
    isChat: state => state.isChat
  }
})
