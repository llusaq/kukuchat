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
    }

  },
  actions: {

  },
  getters: {
    isDark: state => state.isDark,
    connection: state => state.socket,
    isChat: state => state.isChat
  }
})
