<template>
    <div class="col l3 m4 contacts">
            <div class="nav-wrapper">
                <div class="input-field">
                    <input id="search" type="search" v-model="search" autocomplete="off">
                    <label class="label-icon" for="search"><i class="material-icons">search</i></label>
                </div>
            </div>
        <ul class="scroll">
            <li v-for="contact in filteredList" @click="select(contact)" :class="{ clicked: clicked === contact }">
                <div class="icon">
				    <span :style="{backgroundColor: randomColor()}">AV</span>
                </div>
                <div class="info">
                    <span class="user"> <b>{{ contact }}</b> </span><br>
				    <span class="message">last message</span>
                </div>
                <div class="clear"></div>
		    </li>
        </ul>
    </div>
</template>

<script>
export default {
    name: 'contacts',
    data() {
        return {
            contacts: [
                'Andro Vsmopasdasdasjd',
                'Andro Vsmop2',
                'Andro Vsmop3',
                'Andro Vsmop4',
                'Andro Vsmop4',
                'Andro Vsmop4',
                'Andro Vsmop4',
                'Andro Vsmop4',
                'Andro Vsmop5',
            ],
            randcolor: '',
            clicked: 1,
            search: ''
        }
    },
    methods: {
         randomColor() {
            const h = Math.floor(Math.random() * 360),
            s = Math.floor(Math.random() * 70 + 30) + '%',
            l = Math.floor(Math.random() * 60 + 20) + '%';
            return `hsl(${h},${s},${l})`;
            console.log(`hsl(${h},${s},${l})`);
        },
        select(name) {
            this.$parent.currentChat = name;
            this.clicked = name;
            this.search = '';
        }
    },
    computed: {
        filteredList() {
            return this.contacts.filter(contact => {
                return contact.toLowerCase().includes(this.search.toLowerCase())
            })
        }
    }
}
</script>

<style scoped>
.contacts {
    height: calc(100% - 40px);
    float: left;
    padding: 0;
    border-right: 1px solid #f5f5f5;
    background-color: #f5f5f5;
}

.scroll {
    height: calc(100% - 40px);
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
    background-color: #dcdcdc;
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
  box-shadow: inset 0 0 5px #f5f5f5; 
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
    background-color: white;
    width: 90%;
    margin: 0 auto;
}

.nav-wrapper input {
    border: 1px solid #dcdcdc !important;
    height: 40px !important;
}

.label-icon {
    margin-top: 10px;
}

</style>


