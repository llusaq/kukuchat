<template>
    <div class="col l9 m8">
        <div class="msg_cont_area">
            <p class="text-secondary nomessages" v-if="messages === ''">No messages yet!</p>
            <div class="messages" id="messages">
                <div v-for="message in messages" :key="message.id" >
                    <div v-if="!message.me && messages.content !== '' && messages.content !== null" class="notMe">
                        <span class="author">{{currentChat.name}} </span>
                        <span class="time">{{ moment(message.time).format('YYYY-MM-DD  HH:mm')}}</span>
                        <div class="message" v-if="message.content !== ''">
                            <span>{{message.content}}</span>
                        </div>
                    </div>
                    <div v-else-if="messages.content !== '' && messages.content !== null" class="me">
                        <span class="author">Me </span>
                        <span class="time">{{moment(message.time).format('YYYY-MM-DD  HH:mm')}}</span>
                        <div class="message">
                            <span>{{message.content}}</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="sendingsection">
            <div class="row">
                <form class="col s12" rows="4" cols="50">
                    <div class="row">
                        <div class="input-field col s12" rows="4" cols="50">
                            <textarea v-model="message" id="textarea1" class="materialize-textarea"></textarea>
                            <label for="textarea1" rows="4" cols="50">Your message</label>
                        </div>
                    </div>
                </form>
            </div>
            <div class="sendbtnarea">
                <button @click="send()" class="btn waves-effect waves-light blue" type="submit" name="action">SEND
                    <i class="material-icons right">send</i>
                </button>
            </div>
        </div>
    </div>
</template>

<script>

import { store } from '@/store'
import moment from 'moment'
import { mapState } from 'vuex';

export default {
    name: 'conversation',
    data() {
        return {
            
            message: '',
        }
    },
    props: {
        currentChat: ''
    },
    computed: mapState([
        'messages'
    ]),
    methods: {
        send() {
            this.messages.push({
                content: document.getElementById("textarea1").value,
                time: moment().format(),
                provider: 'facebook',
                me: true
            });

            let data = {
                'action': 'send_message',
                'provider': 'facebook',
                'chat_id': this.currentChat.id,
                'content': this.message,
            }

            store.getters.socket.send(JSON.stringify(data));

            this.message = ''
        }
    },
    watch: {
        currentChat() {
            let data = {
                action: 'get_messages',
                chat_id: this.currentChat.id,
                count: 50
            }
            store.getters.socket.send(JSON.stringify(data));
        }
    },
    updated() {
        var container = this.$el.querySelector("#messages");
        container.scrollTop = container.scrollHeight;
    }
}
</script>


<style scoped>

    .author, .time {
        font-size: 12px;
        color: #9e9e9e; 
    }

    .message {
        margin: 0 0 10px 0;
        
    }

    .messages {
        overflow-y: scroll;
        height: 70vh;
        margin-left: 20px;
    }

    .message span {
        max-width: 70%;
        display: inline-block;
    }

    .notMe > .message > span {
        padding: 10px 10px;
        background-color: #a5d6a7;
        border-radius: 1.3em;
    }

    .me > .message > span {
        padding: 10px 10px;
        background-color: #90caf9;
        border-radius: 1.3em;
    }

    .notMe {
        text-align: left;
    }

    .me {
        text-align: right;
    }

    .col {
        padding: 0;
    }

</style>
