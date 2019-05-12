<template>
    <div class="col l3 m4 s12 contacts" >
            <div class="nav-wrapper">
                <div class="input-field">
                    <input id="search" type="search" v-model="search" autocomplete="off">
                    <label class="label-icon" for="search"><i class="material-icons">search</i></label>
                </div>
            </div>
        <ul class="scroll">
            <li v-for="contact in sortedList" :key="contact.id" @click="select(contact)" :class="{ clicked: selectedContact === contact }">
                <div class="icon">
				    <span>{{ contact.name.charAt(0) }}{{ contact.name.charAt(contact.name.indexOf(' ') + 1) }}</span>
                </div>
                <div class="info">
                    <span class="user"> <b>{{ contact.name }}</b> </span><br>
				    <span class="message">{{ contact.last_msg }}</span>
                </div>
                <div class="clear"></div>
		    </li>
        </ul>
    </div>
</template>

<script>

import { store } from '@/store'
import { mapState } from 'vuex';

export default {
    name: 'contacts',
    data() {
        return {
            randcolor: '',
            clicked: '',
            search: '',
        }
    },
    methods: {
        select(name) {
            this.$parent.currentChat = name;
            this.clicked = name;
            this.search = '';
        },
    },
    beforeMount() {
            let data = {
                action: 'provider_facebook_get_chats',
            }
            store.getters.socket.send(JSON.stringify(data));

        data = {
            action: 'provider_skype_get_chats',
        }
        store.getters.socket.send(JSON.stringify(data));


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
        ...mapState(['contacts']),
        sortedList() {
            this.filteredList.sort( ( a, b) => {
                return new Date(a.date) - new Date(b.date);
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
    width: calc(100% - 70px);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
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

.info {
    float: left;
    display: contents;

}

.clicked {
    background-color: #dcdcdc;
}

.clear {
    clear: both;
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

</style>


