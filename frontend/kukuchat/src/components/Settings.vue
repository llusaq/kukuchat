<template>
    <div id="settings" class="modal">
        <div class="modal-header">
            <h4>Settings</h4>
            <a class="modal-close"><i class="material-icons small left">clear</i></a>
        </div>
        <div class="modal-content">
            <div class="row" >
                <h6>Theme</h6>
                <div class="switch">
                    <label >
                        Light
                    <input @click="changeTheme()" type="checkbox">
                    <span class="lever"></span>
                        Dark
                    </label>
                </div>
            </div>
            <div class="row premium">
                <a @click="getPremium()">Get premium</a>
            </div>
        </div>
    </div>
</template>

<script>

import { store } from '@/store'
import { mapState } from 'vuex';
import { constants } from 'crypto';


export default {
    name: 'settings',
    data() {
        return {
        }
    },
    methods: {
        changeTheme() {
            store.commit('changeTheme');
        },
        getPremium() {
            $('#premium').modal('open');
        }
    },
    computed: mapState([
        'isDark'
    ]),
    
}
</script>


<style scoped>

.switch label .lever:after{
    background-color: white;
}

.row {
    min-height: 50px;
}

a, span {
    user-select: none;
    color: rgba(0,0,0,0.80);
    cursor: pointer;
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

.col img {
    max-width: 100%;
    height:auto;
    transition: all 0.2s;
}

.modal-content {
    padding: 0px;
}

.close-form {
    float: right;
}

i {
    position: absolute;
    top: 15px;
    right: 20px;
    cursor: pointer;
    z-index: 9999;
}

.active {
    color: #1565c0  !important;
}

input:focus, .valid {
    border-bottom: 1px solid #1565c0 !important;
    box-shadow: 0 1px 0 0 #1565c0 !important;
}

.logbtn {
    float: right;
    margin: 0 !important;
}

.logbtn a {
    color: #f5f5f5;
    margin: 0 !important;
}

.switch label .lever {
    background-color: #1565c0;
}

.switch label input[type=checkbox]:checked+.lever {
    background-color: #1565c0;
}

.switch label input[type=checkbox]:checked+.lever:after {
    background-color: white
}

.premium a {
    margin: 10px;
    display: inline-block;
    padding: 10px;
    border: 1px solid;
}


</style>
