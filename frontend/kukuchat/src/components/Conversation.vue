<template>
    <div class="col l9 m8">
        <div class="msg_cont_area">
            <Preloader v-if="preloader"></Preloader>
            <p class="text-secondary nomessages" v-if="messages === ''">No messages yet!</p>
            <div class="messages" id="messages">
                <div v-for="message in messages" :key="message.id" class="msg-container">
                    <div v-if="!message.me && messages.content !== null" class="notMe">
                        <span class="author">{{currentChat.name}} </span>
                        <div class="tooltip">
                            <span class="time">{{ moment(message.time).format('HH:mm')}}</span>
                            <span class="tooltiptext time">{{ moment(message.time).format('YYYY:MM:DD  HH:mm')}}</span>
                        </div>
                        <div class="message" v-if="message.content !== ''">
                            <span>{{message.content}}</span>
                        </div>
                        <div class="message" v-else>
                            <span>👍</span>
                        </div>
                    </div>
                    <div v-else-if="messages.content !== null" class="me">
                        <span class="author">Me </span>
                        <div class="tooltip">
                            <span class="time">{{ moment(message.time).format('HH:mm')}}</span>
                            <span class="tooltiptext time">{{ moment(message.time).format('YYYY:MM:DD  HH:mm')}}</span>
                        </div>
                        <div class="message" v-if="message.content !== ''">
                            <span>{{message.content}}</span>
                        </div>
                        <div class="message" v-else>
                            <span>👍</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="sendingsection">
            <textarea v-model="message" rows="20" id="textarea" class="message"></textarea>
            <a @click="send()" class="send-btn">Send</a>
        </div>
    </div>
</template>

<script>

import { store } from '@/store'
import moment from 'moment'
import { mapState } from 'vuex';
import Preloader from './Preloader'

export default {
    name: 'conversation',
    components: {
        Preloader
    },
    data() {
        return {
            message: '',
            hover: true
        }
    },
    props: {
        currentChat: ''
    },
    computed: mapState([
        'messages',
        'preloader'
    ]),
    methods: {
        send() {
            /*let data = {
                content: document.getElementById("textarea1").value,
                time: moment().format(),
                provider: 'facebook',
                me: true
            }

            store.commit('pushMessage', data);*/

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
        margin-bottom: 5px;
    }

    .messages {
        overflow-y: scroll;
        height: 70vh;
        margin-left: 20px;
        padding-right: 10px;
    }

    .message span {
        max-width: 70%;
        display: inline-block;
    }

    .notMe > .message > span {
        padding: 3px 10px;
        background-color: #a5d6a7;
        border-radius: 0.8em;
    }

    .me > .message > span {
        padding: 3px 10px;
        background-color: #90caf9;
        border-radius: 0.8em;
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

    .preloader-wrapper {
        position: absolute;
        top: 40%;
    }

    .hide {
        display: none;
    }

    /* Tooltip container */
    .tooltip {
        position: relative;
        display: inline-block;
    }

    /* Tooltip text */
    .notMe > .tooltip .tooltiptext {
        visibility: hidden;
        position: absolute;
        width: 120px;
        background-color: #9e9e9e;
        color: #fff;
        text-align: center;
        padding: 5px 0;
        border-radius: 6px;
        margin-left: 10px;
        z-index: 1;
        opacity: 0;
        transition: opacity 0.3s;
    }

    .me > .tooltip .tooltiptext {
        visibility: hidden;
        position: absolute;
        width: 120px;
        background-color: #9e9e9e;
        color: #fff;
        text-align: center;
        padding: 5px 0;
        border-radius: 6px;
        z-index: 1;
        opacity: 0;
        transition: opacity 0.3s;
        top: -2px;
        bottom: auto;
        right: 128%;
    }

    /* Tooltip arrow */
    .notMe > .tooltip .tooltiptext::after {
        content: "";
        position: absolute;
        top: 50%;
        right: 100%;
        margin-top: -5px;
        border-width: 5px;
        border-style: solid;
        border-color: transparent #9e9e9e transparent transparent;
    }

    .me > .tooltip .tooltiptext::after {
       content: "";
        position: absolute;
        top: 50%;
        left: 100%;
        margin-top: -5px;
        border-width: 5px;
        border-style: solid;
        border-color: transparent transparent transparent #9e9e9e;
    }

    /* Show the tooltip text when you mouse over the tooltip container */
    .tooltip:hover .tooltiptext {
        visibility: visible;
        opacity: 1;
    }

    /* width */
::-webkit-scrollbar {
  width: 5px;
}

/* Track */
::-webkit-scrollbar-track {
  border-radius: 10px;
}

/* Handle */
::-webkit-scrollbar-thumb {
    background: #64b5f6;
  border-radius: 10px;
}

/* Handle on hover */
::-webkit-scrollbar-thumb:hover {
    background: #1e88e5;
}

.active {
    color: #1565c0  !important;
}

textarea:focus, .valid {
    border-bottom: 1px solid #1565c0 !important;
    box-shadow: 0 1px 0 0 #1565c0 !important;
}

textarea {
    color: red;
}

.sendingsection {
    width: 100%;
    padding: 10px;
}

.input-field {
    width: calc(100% - 100px) !important;
}

.send-btn {
    display: inline-block;
    margin: 10px;
    text-transform: uppercase;
    font-weight: 500;
    cursor: pointer;
}


</style>
