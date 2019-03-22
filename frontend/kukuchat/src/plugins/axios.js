"use strict";

import Vue from 'vue';
import axios from "axios";

// Full config:  https://github.com/axios/axios#request-config
// axios.defaults.baseURL = 'http://127.0.0.1:8000/';
// axios.defaults.headers.common['Authorization'] = AUTH_TOKEN;
// axios.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';

let config = {
   baseURL: 'http://127.0.0.1:8000/',
  // timeout: 60 * 1000, // Timeout
  withCredentials: false, // Check cross-site Access-Control
};

export const http = axios.create(config);

http.interceptors.request.use(
  function(config) {
    // Do something before request is sent
    return config;
  },
  function(error) {
    // Do something with request error
    return Promise.reject(error);
  }
);

// Add a response interceptor
http.interceptors.response.use(
  function(response) {
    // Do something with response data
    return response;
  },
  function(error) {
    // Do something with response error
    return Promise.reject(error);
  }
);

Plugin.install = function(Vue, options) {
  Vue.axios = http;
  window.axios = http;
  Object.defineProperties(Vue.prototype, {
    axios: {
      get() {
        return http;
      }
    },
    $axios: {
      get() {
        return http;
      }
    },
  });
};

Vue.use(Plugin)

export default Plugin;
