<template>
    <div class="col l9 m8">
        <div class="msg_cont_area">
            <p class="text-secondary nomessages" v-if="messages === ''">No messages yet!</p>
            <div class="messages">
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
        <!-- <div class="sendingsection">
            <div class="row">
                <form class="col s12" rows="4" cols="50">
                    <div class="row">
                        <div class="input-field col s12" rows="4" cols="50">
                            <textarea id="textarea1" class="materialize-textarea"></textarea>
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
        </div> -->
    </div>
</template>

<script>

import { store } from '@/store'
import moment from 'moment'

export default {
    name: 'conversation',
    data() {
        return {
            messages: [
                {
                    message: '',
                    timestamp: '',
                    name: ''
                }
            ]
        }
    },
    methods: {
        send() {
            var today = new Date();
            var d = today.getDay();
            var mo = today.getMonth();
            var ye = today.getYear();
            var h = today.getHours();
            var m = today.getMinutes();
            // this.messages.push({message:'my message',timestamp:"3:00",name:'me'});
            this.messages.push({
                message: document.getElementById("textarea1").value,
                timestamp: 'time: ' + h + ':' + m + ' date: ' + d + '.' + (mo + 1) + '.' + (1900 + ye),
                name: 'me'
            });
            document.getElementById("textarea1").value = " ";
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
    beforeMount() {
        store.getters.socket.onmessage = ({data}) => {
            data = JSON.parse(data)
            console.log(data)
            this.messages = ''
            if (data.action === 'get_messages' && data.status === 'ok')
                this.messages = data.messages.reverse();
        };
    },
    props: ['currentChat'],
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
        overflow: scroll;
        height: 100%;
    }
</style>
