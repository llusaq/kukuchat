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

    props: ['name'],
    components: {
        Contacts,
        Menu,
        Conversation,
    },

    data() {
        return {
            currentChat: '',
            currentChatId: '',
            width: window.innerWidth,
            messages: [],
        }
    },
    computed: mapState([
            'isChat'
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
        store.getters.socket.onmessage = ({data}) => {
            data = JSON.parse(data)
            console.log(data)

            if (data.action === 'provider_facebook_am_i_logged' && data.is_logged) {
                store.commit('setMessenger');
                store.commit('setChat');
            }

            if (data.action === 'am_i_logged' && !data.is_logged) {
                this.$router.push({name: 'home'})
            }
        };
        let data = {
            action: 'am_i_logged'
        }
        store.getters.socket.send(JSON.stringify(data));
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


