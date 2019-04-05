<template>
    <div class="wrapper" @keyup.esc="escape()">
        <Menu :current-chat="currentChat"></Menu>
        <div class="row chat">
            <Contacts v-if="currentChat == '' && width <= 600"></Contacts>
            <Contacts v-else-if="width > 600"></Contacts>
            <Conversation v-if="currentChat != '' && width <= 600"></Conversation>
            <Conversation v-else-if=" currentChat != '' && width > 600"></Conversation>
        </div>
    </div>

</template>

<script>

import Contacts from '@/components/Contacts.vue'
import Menu from '@/components/Menu.vue'
import Conversation from '@/components/Conversation.vue'

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
            messages: []
        }
    },


    created: function () {
        window.addEventListener('keyup', this.onkey)
        //  let ref = baza.collection('messages').orderBy('timestamp');

        //  ref.onSnapshot(snapshot)
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

</style>


