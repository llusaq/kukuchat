<template>
    <div class="col l9 m8 conv">
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
                            <img v-if="message.provider === 'facebook'" src="@/assets/messenger.png" alt="messanger">
                            <img v-if="message.provider === 'skype'" src="@/assets/skype.png" alt="skype">
                            <img v-if="message.provider === 'viber'" src="@/assets/viber.png" alt="viber">
                            <img v-if="message.provider === 'gmail'" src="@/assets/gmail.png" alt="gmail">
                            <img v-if="message.provider === 'telegram'" src="@/assets/telegram.png" alt="telegram">
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
                            <img v-if="message.provider === 'facebook'" src="@/assets/messenger.png" alt="messanger">
                            <img v-if="message.provider === 'skype'" src="@/assets/skype.png" alt="skype">
                            <img v-if="message.provider === 'viber'" src="@/assets/viber.png" alt="viber">
                            <img v-if="message.provider === 'gmail'" src="@/assets/gmail.png" alt="gmail">
                            <img v-if="message.provider === 'telegram'" src="@/assets/telegram.png" alt="telegram">
                            <span>{{message.content }}</span>
                        </div>
                        <div class="message" v-else>
                            <span>👍</span>
                        </div>
                    </div>
                </div>
            </div>
        <div class="sendingsection">
            <textarea v-model="message" rows="4" class="message-box" placeholder="Write a message..." @keyup.enter="send()"></textarea>
            <a @click="send()" class="send-btn">Send</a>

            <div v-show="anotherSendServices" class="another-send-service">
                <img v-if="currentChat.provider.includes('facebook') && sendService !== 'facebook'" @click="chooseAnotherService('facebook')" src="@/assets/messenger.png" alt="messanger">
                <img v-if="currentChat.provider.includes('skype') && sendService !== 'skype'" @click="chooseAnotherService('skype')" src="@/assets/skype.png" alt="skype">
                <img v-if="currentChat.provider.includes('skype') && sendService !== 'skype'" @click="chooseAnotherService('skype')" src="@/assets/skype.png" alt="skype">
                <img v-if="currentChat.provider.includes('viber') && sendService !== 'viber'" @click="chooseAnotherService('viber')" src="@/assets/viber.png" alt="viber">
                <img v-if="currentChat.provider.includes('gmail') && sendService !== 'gmail'" @click="chooseAnotherService('gmail')" src="@/assets/gmail.png" alt="gmail">
                <img v-if="currentChat.provider.includes('telegram') && sendService !== 'telegram'" @click="chooseAnotherService('telegram')" src="@/assets/telegram.png" alt="telegram">
            </div> 
            <div class="send-service">
                <img v-if="currentChat.provider.includes('facebook') && sendService === 'facebook'" @click="showAvailableServices()" src="@/assets/messenger.png" alt="messanger">
                <img v-if="currentChat.provider.includes('skype') && sendService === 'skype'" @click="showAvailableServices()" src="@/assets/skype.png" alt="skype">
                <img v-if="currentChat.provider.includes('viber') && sendService === 'viber'" @click="showAvailableServices()" src="@/assets/viber.png" alt="viber">
                <img v-if="currentChat.provider.includes('gmail') && sendService === 'gmail'" @click="showAvailableServices()" src="@/assets/gmail.png" alt="gmail">
                <img v-if="currentChat.provider.includes('telegram') && sendService === 'telegram'" @click="showAvailableServices()" src="@/assets/telegram.png" alt="telegram">
            </div> 
            <div class="clear"></div>
        </div>
    </div>
</template>

<script>

import { store } from '@/store'
import moment from 'moment'
import { mapState } from 'vuex';
import Preloader from './Preloader'
import { truncate } from 'fs';

export default {
    name: 'conversation',
    components: {
        Preloader
    },
    data() {
        return {
            message: '',
            hover: true,
            sendService: this.currentChat.msgProvider,
            anotherSendServices: false
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
            this.currentChat.last_msg = this.message;
            this.currentChat.msgProvider = this.sendService;
            let data;
            if (this.sendService === 'facebook') {
                data = {
                    'action': 'send_message',
                    'provider': 'facebook',
                    'chat_id': this.currentChat.id,
                    'content': this.message,
                }
            }
            
            if (this.sendService === 'skype') {
                data = {
                    'action': 'send_message',
                    'provider': 'skype',
                    'chat_id': this.currentChat.id,
                    'content': this.message,
                }
            }

            store.getters.socket.send(JSON.stringify(data));

            this.message = ''
        },
        showAvailableServices() {
            this.anotherSendServices = this.anotherSendServices ? false : true;
        },
        chooseAnotherService(service) {
            this.anotherSendServices = false;
            this.sendService = service;
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
        height: 75%;
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
    border: none;
}

.message-box {
    border: none;
    border-bottom: 2px solid #64b5f6;
    resize: none;
    width: calc(100% - 100px);
    float: left;
    height: 100%;
    font-weight: 400;
    letter-spacing: 1px;
    cursor: text;
}

textarea:focus, textarea:active, textarea:focus:active {
    border: none;
    border-bottom: 2px solid #2196f3;
    box-shadow: none !important;
    outline: 0;
}

.sendingsection {
    width: 100%;
    height: 17vh;
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

.clear {
    clear: both;
}

.conv {
    height: 100vh;

}

.message img {
    width: 20px;
    height: auto;
    margin: 0 3px -4px 0;
}

.send-service img {
    width: 50px;
    height: auto;
    margin-top: 25px;
    cursor: pointer;
}

.another-send-service {
    width: 50px;
    position: absolute;
    right: 35px;
    bottom: 120px;
    transition: all 0.2s;
}

.another-send-service img {
    width: 50px;
    height: auto;
    cursor: pointer;
    transition: all 0.2s;
}

.another-send-service img:hover {
    width: 70px;
    height: auto;
    margin-left: -10px;
}

@media only screen and (max-width: 600px) {
    .send-service img {
        margin-top: 0px;
    }
    .another-send-service {
        bottom: 60px;
    }
}

</style>
