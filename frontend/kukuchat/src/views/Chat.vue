<template>
    <div class="wrapper">
        <Menu :current-chat="currentChat"></Menu>
        <div class="row chat">
            <Contacts v-if="currentChat == '' && width <= 600 && isChat"></Contacts>
            <Contacts v-else-if="width > 600 && isChat"></Contacts>
            <Conversation :current-chat="currentChat" v-if="currentChat != '' && width <= 600"></Conversation>
            <Conversation :current-chat="currentChat" v-else-if=" currentChat != '' && width > 600"></Conversation>
            <h5 v-if="!isChat">Add chat service to see something</h5>
            <h5 v-if="currentChat == '' && isChat">Choose contact to start conversation</h5>
        </div>
    </div>
</template>

<script>

import Contacts from '@/components/Contacts.vue'
import Menu from '@/components/Menu.vue'
import Conversation from '@/components/Conversation.vue'
import { store } from '@/store'
import { mapState } from 'vuex';

export default {
    name: 'chat',

    components: {
        Contacts,
        Menu,
        Conversation,
    },
    data() {
        return {
            currentChat: '',
            width: window.innerWidth,
        }
    },
    computed: mapState([
        'isChat',
        'contacts'
    ]),
    created: function () {
        window.addEventListener('keyup', this.onkey)
    },
    beforeDestroy: function () {
        window.removeEventListener('keyup', this.onkey)
    },
    methods: {
        onkey(event) {
            if (event.keyCode == 27) {
                this.currentChat = '';
            }
        }
    },
    beforeMount() {
        if (store.getters.socket === undefined) {
            this.$router.push({name: 'home'})
        }
        else {
            store.getters.socket.onmessage = ({data}) => {
                data = JSON.parse(data)
                console.log(data)

                if (data.action === 'provider_facebook_am_i_logged' && data.is_logged) {
                    store.commit('setMessenger');
                    store.commit('setChat');
                    /*let data = {
                        action: 'get_chats',
                    }
                    store.getters.socket.send(JSON.stringify(data));*/
                }

                if (data.action === 'provider_skype_am_i_logged' && data.is_logged) {
                    store.commit('setSkype');
                    store.commit('setChat');
                    /*let data = {
                        action: 'get_chats',
                    }
                    store.getters.socket.send(JSON.stringify(data));*/
                }

                if (data.action === 'am_i_logged' && !data.is_logged) {
                    this.$router.push({name: 'home'})
                }

                if ((data.action === 'provider_facebook_get_required_credentials' && data.password) ||
                    (data.action === 'provider_skype_get_required_credentials' && data.password)) {
                    store.commit('setPasswordField');
                    store.commit('setPasswordHelp', data.password.help);
                }

                if ((data.action === 'provider_facebook_get_required_credentials' && data.username) ||
                    (data.action === 'provider_skype_get_required_credentials' && data.username)) {
                    store.commit('setUsernameField');
                    store.commit('setUsernameHelp', data.username.help);
                }

                if (data.action === 'provider_facebook_login' && data.status === 'ok') {
                    store.commit('setPreloader', false);
                    store.commit('changeAddAccountForm', false);
                    M.toast({html: 'Messenger added', classes: 'green darken-2'})
                    store.commit('setMessenger');
                    store.commit('setChat');
                    let data = {
                        action: 'get_chats',
                    }
                    store.getters.socket.send(JSON.stringify(data));
                }

                if (data.action === 'provider_facebook_login' && data.status === 'error') {
                    store.commit('setPreloader', false);
                    M.toast({html: 'Logging failed. Invalid login or password', classes: 'red darken-2'})

                }

                if (data.action === 'provider_skype_login' && data.status === 'ok') {
                    store.commit('setPreloader', false);
                    store.commit('changeAddAccountForm', false);
                    M.toast({html: 'Skype added', classes: 'green darken-2'})
                    store.commit('setSkype');
                    store.commit('setChat');
                    let data = {
                        action: 'get_chats',
                    }
                    store.getters.socket.send(JSON.stringify(data));
                }

                if (data.action === 'provider_skype_login' && data.status === 'error') {
                    store.commit('setPreloader', false);
                    M.toast({html: 'Logging failed. Invalid login or password', classes: 'red darken-2'})
                }

                if (data.action === 'get_chats') {
                    let ids = [];
                    for (let contact of data.chats) {
                        ids.push(contact.id);
                    }
                    let data2 = {
                        action: 'schedule',
                        provider: 'facebook',
                        method: 'get_messages',
                        chat_ids: ids,
                        count: 2
                    }

                    store.getters.socket.send(JSON.stringify(data2));
                    store.commit('setContacts', data.chats);
                }

                if (data.action === 'get_messages' && data.chats[0] != null && data.chats[0].messages.length === 2) {
                    store.commit('setProvider', [data.chats[0].id, data.chats[0].messages[0].provider]);
                    store.commit('setLastMsg', [data.chats[0].id, data.chats[0].messages[0].content]);
                    store.commit('setTime', [data.chats[0].id, data.chats[0].messages[0].time]);
                    store.commit('setPreloader', false);
                } 

                if (data.action === 'get_messages' && data.chats[0] != null && data.chats[0].messages.length === 1) {
                    store.commit('setProvider', [data.chats[0].id, data.chats[0].messages[0].provider]);
                    store.commit('setLastMsg', [data.chats[0].id, data.chats[0].messages[0].content]);
                    store.commit('setTime', [data.chats[0].id, data.chats[0].messages[0].time]);
                    store.commit('setPreloader', false);
                }

                if (data.action === 'get_messages' && data.chats[0] != null && data.chats[0].messages.length !== 1) {
                    store.commit('setMessages', data.chats[0].messages.reverse());
                    store.commit('setPreloader', false);
                    store.commit('setNewMsg', [data.chats[0].id, false]);
                }

                if (data.action === 'new_message') {
                    if (data.chat_id === this.currentChat.id)
                        store.commit('pushMessage', data);
                    store.commit('setProvider', [data.chat_id, data.provider]);
                    store.commit('setLastMsg', [data.chat_id, data.content]);
                    store.commit('setTime', [data.chat_id, data.time]);
                    store.commit('setNewMsg', [data.chat_id, true]);
                }

                if (data.action === 'send_message') {
                    data.me = true;
                    store.commit('pushMessage', data);
                }

                // if (data.action === 'provider_skype_get_chats') {
                //     store.commit('setContacts', data.chats);
                // }
               
            }
            let query = {
                action: 'am_i_logged'
            }
            store.getters.socket.send(JSON.stringify(query));

            query = {
                action: 'provider_facebook_am_i_logged' 
            }
            store.getters.socket.send(JSON.stringify(query));

            query = {
                action: 'provider_skype_am_i_logged' 
            }
            store.getters.socket.send(JSON.stringify(query)); 
            
            query = {
                action: 'get_chats' 
            }
            store.getters.socket.send(JSON.stringify(query));
        }
    },
    mounted() {
    }
}

</script>

<style scoped>

.row, .wrapper {
    height: 100%;
}

.wrapper > .row {
    height: auto;
}

.wrapper > .chat {
    height: 100%;
}

h5 {
    display: inline-block;
    margin: 200px auto 0 auto;
}

.chat {
    text-align: center;
}



</style>


