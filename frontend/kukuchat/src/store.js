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
    contacts: []/*[{
          id: '',
          name: '',
          provider: '',
          last_msg: '',
          time: '',
          newMsg: false,
    }]*/,
    messages: [
        {
            content: '',
            time: '',
            provider: '',
            me: false,
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
      state.contacts = state.contacts.concat(value);
    },
    clearContacts(state) {
      state.contacts = [];
    },
    removeContact(state, id) {
      let index = state.contacts.indexOf(id);
      if (index != -1) {
        state.contacts.splice(index, 1);
      }
    },
    setMessages(state, value) {
      state.messages = value;
    },
    clearMessages(state) {
      state.messages = [];
    },
    pushMessage(state, value) {
      state.messages.push(value);
    },
    changeAddAccountForm(state, value) {
      state.addAccountForm = value;
    },
    setProvider(state, [id, value]) {
      let result = state.contacts.find( contact => contact.id === id );
      if (result != null)
        result.provider = value;
    },
    setLastMsg(state, [id, value]) {
      let result = state.contacts.find( contact => contact.id === id );
      if (value == null) {
        result.last_msg = 'No messages yet!'
      }
      if (value === "") {
        result.last_msg = '👍'
      }
      else
        result.last_msg = value;
    },
    setTime(state, [id, value]) {
      let result = state.contacts.find( contact => contact.id === id );
      if (result != null)
        result.time = value;
    },
    setNewMsg(state, [id, value]) {
      let result = state.contacts.find( contact => contact.id === id );
      if (result != null)
      result.newMsg = value;
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
