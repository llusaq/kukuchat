<template>
    <div class="col l3 m4 s12 contacts" >
        <Preloader class="preloader" v-if="preloader"></Preloader>
            <div class="nav-wrapper">
                <div class="input-field">
                    <input id="search" type="search" v-model="search" autocomplete="off">
                    <label class="label-icon" for="search"><i class="material-icons">search</i></label>
                </div>
            </div>
            
        <ul class="scroll">
            <li v-for="contact in sortedList" :key="contact.id" @dblclick="select(contact)" @click="click(contact)" :class="{ clicked: selectedContact === contact, selected: mergeIds.includes(contact.id), mergeTo: mergeIds.indexOf(contact.id) === 0}" >
                <div class="icon">
				    <span>{{ contact.name.charAt(0) }}{{ contact.name.charAt(contact.name.indexOf(' ') + 1) }}</span>
                </div> 
                <div class="text">
                    <span class="user"> <b>{{ contact.name }}</b> </span>
                    <!-- <i v-if="contact.newMsg" class="material-icons lens">fiber_manual_record</i> -->
                    <span v-if="contact.newMsg" class="message"><b>{{ contact.last_msg }}</b></span>
                    <span v-else class="message">{{ contact.last_msg }}</span>
                        <img v-if="contact.msgProvider === 'facebook'" src="@/assets/messenger.png" alt="messanger">
                        <img v-if="contact.msgProvider === 'skype'" src="@/assets/skype.png" alt="skype">
                        <img v-if="contact.msgProvider === 'viber'" src="@/assets/viber.png" alt="viber">
                        <img v-if="contact.msgProvider === 'gmail'" src="@/assets/gmail.png" alt="gmail">
                        <img v-if="contact.msgProvider === 'telegram'" src="@/assets/telegram.png" alt="telegram">
                    
                </div>
                <div class="services">
                    <img v-if="contact.provider.includes('facebook')" src="@/assets/messenger.png" alt="messanger">
                    <img v-if="contact.provider.includes('skype')" src="@/assets/skype.png" alt="skype">
                    <img v-if="contact.provider.includes('viber')" src="@/assets/viber.png" alt="viber">
                    <img v-if="contact.provider.includes('gmail')" src="@/assets/gmail.png" alt="gmail">
                    <img v-if="contact.provider.includes('telegram')" src="@/assets/telegram.png" alt="telegram">
                </div>
                <div class="clear"></div>
		    </li>
        </ul>
        
        <div class="col l3 m4 s12 merge-form" v-if="isMerge">
            <a class="col l6 m6" @click="mergeContacts()">Merge</a>
            <a class="col l6 m6" @click="cancelMerge()">Cancel</a>
        </div>
    </div>
</template>

<script>

import { store } from '@/store'
import { mapState } from 'vuex';
import Preloader from './Preloader'

export default {
    name: 'contacts',
    components: {
        Preloader,
    },
    data() {
        return {
            randcolor: '',
            clicked: '',
            search: '',
            mergeIds: [],
            isMerge: false,
        }
    },
    methods: {
        click(contact) {
            this.$parent.currentChat = contact;
            this.clicked = contact;
            //this.search = '';
            store.commit('clearMessages');
            store.commit('setPreloader', true);
            store.commit('setNewMsg', [contact.id, false]);
            let data = {
                action: 'get_messages',
                chat_ids: [contact.id],
                count: 200
            }
            store.getters.socket.send(JSON.stringify(data));
        },
        select(contact) {
            if (this.mergeIds.includes(contact.id)) {
                console.log('is')
                let index = this.mergeIds.indexOf(contact.id);
                if (index > -1) {
                    this.mergeIds.splice(index, 1);
                }
            } else {
                this.mergeIds.push(contact.id);
                this.isMerge = true;
            }
            if (this.mergeIds.length === 0) {
                this.isMerge = false;
            }
        },
        cancelMerge() {
            this.mergeIds = [];
            this.isMerge = false;
        },
        mergeContacts() {
            let data = {
                action: 'merge_chats',
                chat_ids: this.mergeIds
            }
            store.getters.socket.send(JSON.stringify(data));
            M.toast({html: 'Contacts merged successfully', classes: 'green darken-2'})
            /*for (let i = 1; i < this.mergeIds.length; i++) {
                store.commit('removeContact', this.mergeIds[i]);
                store.commit('addProvider', this.mergeIds[i], this.mergeIds[0]);
            }*/
            this.cancelMerge();
            store.commit('clearContacts');
            this.$parent.currentChat = '';
            let query = {
                action: 'get_chats' 
            }
            store.getters.socket.send(JSON.stringify(query));
        }
    },
    beforeMount() {
        
    },
    computed: {
        selectedContact() {
            return this.$parent.currentChat === '' ? '' : this.$parent.currentChat;
        },
        filteredList() {
            if (this.contacts !== undefined)
            if (this.search !== '') {
                return this.contacts.filter(contact => {
                    if (contact.name !== undefined) {
                        return contact.name.toLowerCase().includes(this.search.toLowerCase())
                    }
                })
            }
            return this.contacts;
        },
        ...mapState([
            'contacts',
            'messenger',
            'skype',
            'viber',
            'gmail',
            'telegram',
            'preloader'
        ]),

        sortedList() {
            this.filteredList.sort( ( a, b) => {
                return new Date(b.time) - new Date(a.time);
            });
                return this.filteredList;
        }
    }
}
</script>

<style scoped>
.contacts {
    height: 100%;
    float: left;
    padding: 0;
    background-color: #f5f5f5;
    text-align: left;
}

.contacts {
    height: calc(100% - 35px);
    overflow: scroll;
}

ul {
    margin: 0;
}

li {
    padding: 15px;
    cursor: pointer;
}

li:hover {
    background-color: #e0e0e0 ;
}

span {
    display: inline-block;
    color: rgba(0,0,0,0.80);
}

.circle {
    height: 30px;
    width: 30px;
}


.user, .message {
    margin-top: 5px;
    width: 100%;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.message {
    width: calc(100% - 25px);
    float: right;
}

.icon {
    float: left;
    margin-right: 10px;
}

.icon span {
    width: 50px;
    height: 50px;
    border-radius: 50%;
    text-align: center;
    padding-top: 5px;
    color: white;
    font-size: 24px;
    margin: 5px;
}


.clicked {
    background-color: #dcdcdc;
}

.selected {
    background-color: #9fa8da !important;
}

.mergeTo {
    background-color: #7986cb !important;
}

.clear {
    clear: both;
}

.nav-wrapper {
    width: 90%;
    margin: 0 auto;
    border-radius: 20px;
}

.nav-wrapper input {
    border: 1px solid #dcdcdc !important;
    background-color: white;
    height: 40px !important;
    border-radius: 10px;
}

.label-icon {
    margin-top: 10px;
}

.active i {
    color: #64b5f6 !important;
}

.icon span {
    background-color: #ffab40;
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

.lens {
    color: red;
}

.merge-form {
    position: fixed;
    bottom: 0;
    text-align: center;
    height: 55px;
    background-color: #d32f2f    ;
}

.merge-form a{
    color: rgba(255, 255, 255, 0.90);
    cursor: pointer;
    transition: all 0.1s ease;
    padding: 17px 0;
}

.merge-form a:hover {
    font-size: 20px;
    padding: 12px 0;
}

.services {
    width: 65px;
    float: right;
    margin-top: 8px;
    margin-right: -20px;
}

.services img {
    width: 20px;
    height: auto;
    margin: 0 3px;
}

.text {
    float: left;
    width: calc(100% - 115px);
}

.text img {
    width: 20px;
    height: auto;
    margin-top: 7px;
}

.preloader {
    position: absolute;
    left: 150px;
    top: 150px;
}

</style>


