<template>
    <div class="row settings">
        <a class="col l3 m4 s12 menu-el" :class="{opened: opened}" @click="settings()">
            <i class="material-icons left">{{ icon }}</i>
            CooCoo
        </a>
        <div class="col card l3 m4" v-if="opened">
            <a class="settings-btn modal-trigger" href="#add-account" @click="settings()">Add account</a>
            <a class="settings-btn">Log out</a>
        </div>
        <a class="col l9 m8 s12 menu-el" v-if="">
            {{ currentChat }}
        </a>
        <div id="add-account" class="modal">
             <div class="modal-header">
                <h4>Add account</h4>
                <a class="modal-close"><i class="material-icons small left">clear</i></a>
            </div>
            <div class="modal-content">
                <div class="row">
                    <div class="col l2 m2">
                        <img src="@/assets/messenger.png" alt="messenger">
                        <span> <b>Messenger</b> </span>
                    </div>
                    <div class="col l2 m2">
                        <img src="@/assets/skype.png" alt="skype">
                        <span> <b>Skype</b> </span>
                    </div>
                    <div class="col l2 m2">
                        <img src="@/assets/viber.png" alt="viber">
                        <span> <b>Viber</b> </span>
                    </div>
                    <div class="col l2 m2">
                        <img src="@/assets/gmail.png" alt="gmail">
                        <span> <b>Gmail</b> </span>
                    </div>
                    <div class="col l2 m2">
                        <img src="@/assets/telegram.png" alt="telegram">
                        <span> <b>Telegram</b> </span>
                    </div>
                </div>
               
                <div class="clear"></div>
            </div>
           
        </div>
        
    </div>
</template>

<script>
export default {
    name: 'dropdownmenu',
    data() {
        return {
            icon: 'menu',
            style: 'white',
            opened: false,
            showModal: false,
            
        }
    },
    mounted() {
        $('#add-account').modal();
    },
    methods: {
        settings() {
            this.icon = this.icon === 'menu' ? 'clear' : 'menu';
            this.opened = !this.opened;
        },
    },
    props: ['currentChat'],
}
</script>

<style scoped>

.clear {
    clear: both;
}

.settings {
    background-color: white;
    box-shadow: 0 4px 2px -2px rgba(0,0,0,0.12);
    text-align: center;
    color: rgba(0,0,0,0.87);
    cursor: pointer;
    height: 50px;
    position: relative;
}

i {
    transition: 0.5ms;
    transition-delay: 1s;
}

a {
    user-select: none;
    color: rgba(0,0,0,0.80);
}

.menu-el {
    padding: 15px;
    height: 55px;
}

.menu-el:hover {
    background-color: #e0e0e0;
}

.row {
    height: auto;
    margin-bottom: 0;
}

.card {
    position: absolute;
    top: 55px;
    box-shadow: 0px 4px 2px -2px rgba(0,0,0,0.12);
    background-color: white;
    z-index: 999;
    margin: 0;
    padding: 0;
}

.settings-btn {
    width: 100%;
    height: 30px;
    display: inline-table;
    padding: 10px 0;
    line-height: 28px;
}

.settings-btn:hover {
    background-color: #eeeeee;
}

.opened {
    background-color: #e0e0e0;
}

.modal-header {
    padding: 10px 0;
}

.modal-header h4 {
    display: inline-block;
}

.modal {
    overflow: hidden;
    cursor: default;
}

.modal-close {
    float: right;
}

.modal-content .col {
    margin: 20px 1.6%;
    position: relative;
    height: 150px;
    transition: all 0.2s ease;
    display: table;
    cursor: pointer;
}

.modal-content .col:hover img {
    max-width: 130%;
    height: auto;
    margin-left: -15%;
    margin-top: -15%;
}

.modal-content .col span {
    position: absolute;
    left: 50%;
    bottom: 0;
    transform: translate(-50%, -50%);
}

.col img {
    max-width: 100%;
    height:auto;
    transition: all 0.2s;
}

.modal-content {
    padding: 20px;
}



</style>


