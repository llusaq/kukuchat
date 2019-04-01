import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export const store = new Vuex.Store({
  state: {
    isDark: false,
    socket: ''
  },
  mutations: {
    changeTheme (state) {
      state.isDark = !state.isDark
    },
    connect: (state, connection ) => {
      state.socket = connection
    }
  },
  actions: {

  },
  getters: {
    isDark: state => state.isDark,
    connection: state => state.socket
  }
})
