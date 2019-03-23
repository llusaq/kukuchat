<template>
    <div class="wrapper">
        <Menu :current-chat="currentChat"></Menu>
        <div class="row chat">
            <Contacts></Contacts>
            <Conversation></Conversation>
        </div>
    </div>
    
</template>

<script>

import Contacts from '@/components/Contacts.vue'
import Menu from '@/components/Menu.vue'
import Conversation from '@/components/Conversation.vue'

export default {
    name: 'chat',
    data() {
        return {
            currentChat: 'empty'
        }
    },
    components: {
        Contacts,
        Menu,
        Conversation
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


