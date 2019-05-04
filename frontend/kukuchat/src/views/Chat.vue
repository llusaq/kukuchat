<template>
    <div class="wrapper" @keyup.esc="escape()">
        <Menu :current-chat="currentChat"></Menu>
        <div class="row chat">
            <Contacts v-if="currentChat == '' && width <= 600 && isChat"></Contacts>
            <Contacts v-else-if="width > 600 && isChat"></Contacts>
            <Conversation v-if="currentChat != '' && width <= 600"></Conversation>
            <Conversation v-else-if=" currentChat != '' && width > 600"></Conversation>
            <h5 v-if="!isChat">Add chat service to see something</h5>
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
        //  CreateMessage
    },

    data() {
        return {
            currentChat: '',
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
        if (store.getters.socket === undefined) {
            this.$router.push({name: 'home'})
            }
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
    display: table;
    margin: 200px auto 0 auto;
}

</style>


