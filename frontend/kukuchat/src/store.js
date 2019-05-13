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
            last_msg: '',
            time: '',
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
      let msg = {
        content: value.content,
        time: value.time,
        proveder: value.provider,
        me: false
      }
      console.log(typeof state.messages)
      //state.messages.push(msg);
    },
    changeAddAccountForm(state, value) {
      state.addAccountForm = value;
    },
    setProvider(state, [id, value]) {
      if (state.contacts[id] != null)
        state.contacts[id].provider = value;
    },
    setLastMsg(state, [id, value]) {
      if (value == null) {
        value = 'No messages yet!'
      }
      if (value === "") {
        value = '👍'
      }
      if (state.contacts[id] != null)
        state.contacts[id - 1].last_msg = value;
    },
    setTime(state, [id, value]) {
        state.contacts[id - 1].time = value;
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
  getters: {
    isDark: state => state.isDark,
    connection: state => state.socket,
    isChat: state => state.isChat
  }
})
