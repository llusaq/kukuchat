<template>
    <div class="col l9 m8">
        <div class="topinfoboard">
            <div class="user_info">
                <div class="whowith">Chat with Andro</div>
                <div class="messagecount">78 Messages</div>
            </div>


        </div>
        <div class="messageboard">
            <div class="card">
                <div class="holder">

                    <div class="msg_card_body">
                        <div class="msg_cont_area">

                            <p class="text-secondary nomessages" v-if="messages.length==0">
                                [No messages yet!]
                            </p>

                            <div class="messages">


                                <div v-for="message in messages" :key="message.id">

                                    <div v-if="message.name === 'me'">
                                        <span class="text-info">[{{message.name}}]</span>


                                        <div class="msg_cont_area">
                                            <div class="msg_cotainer">
                                                <span>{{message.message}}</span>

                                                <span class="msg_time">{{message.timestamp}}</span>
                                            </div>
                                        </div>
                                    </div>

                                    <div v-else>

                                        <span class="text-info">[{{message.name}}]</span>

                                        <div class="msg_cont_send_area">
                                            <div class="msg_cotainer_send">

                                                <span>{{message.message}}</span>

                                                <span class="msg_time_send">{{message.timestamp}}</span>
                                            </div>
                                        </div>


                                    </div>


                                </div>

                            </div>

                            <div class="card-action">
                                <CreateMessage :name="name"/>
                            </div>

                        </div>

                    </div>
                </div>
            </div>


            <!--
            <div class="msg_cont_area">
                <div class="msg_cotainer">
                    Hi, how are you Andro?
                    <span class="msg_time">8:40 AM, Today</span>

                </div>
            </div>
            <div class="msg_cont_send_area">
                <div class="msg_cotainer_send">
                    Hi Andro i am good tnx how about you?
                    <span class="msg_time_send">8:55 AM, Today</span>
                </div>
            </div>

            <div class="msg_cont_area">
                <div class="msg_cotainer">
                    Hi, how are you Andro?
                    <span class="msg_time">8:40 AM, Today</span>

                </div>
            </div>
            <div class="msg_cont_send_area">
                <div class="msg_cotainer_send">
                    Hi Andro i am good tnx how about you?
                    <span class="msg_time_send">8:55 AM, Today</span>
                </div>
            </div>

            <div class="msg_cont_area">
                <div class="msg_cotainer">
                    Hi, how are you Andro?
                    <span class="msg_time">8:40 AM, Today</span>

                </div>
            </div>
            <div class="msg_cont_send_area">
                <div class="msg_cotainer_send">
                    Hi Andro i am good tnx how about you?
                    <span class="msg_time_send">8:55 AM, Today</span>
                </div>
            </div>

            <div class="msg_cont_area">
                <div class="msg_cotainer">
                    Hi, how are you Andro?
                    <span class="msg_time">8:40 AM, Today</span>

                </div>
            </div>
            <div class="msg_cont_send_area">
                <div class="msg_cotainer_send">
                    Hi Andro i am good tnx how about you?
                    <span class="msg_time_send">8:55 AM, Today</span>
                </div>
            </div>
            <div class="msg_cont_area">
                <div class="msg_cotainer">
                    Hi, how are you Andro?
                    <span class="msg_time">8:40 AM, Today</span>

                </div>
            </div>
            <div class="msg_cont_send_area">
                <div class="msg_cotainer_send">
                    Hi Andro i am good tnx how about you?
                    <span class="msg_time_send">8:55 AM, Today</span>
                </div>
            </div>


            -->


            <!-- <textarea name="" class=" type_msg" placeholder="Type your message..."></textarea>
             <div class="sendbtnarea">
                 <button class="btn waves-effect waves-light" type="submit" name="action">SEND
                     <i class="material-icons right">send</i>
                 </button>
             </div>

             -->

            <div class="sendingsection">

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

                    <div class="w3-dropdown-hover">
                        <button class="w3-button">Hover Over Me!</button>
                        <div class="w3-dropdown-content w3-bar-block w3-border">
                            <a href="#" class="w3-bar-item w3-button">Link 1</a>
                            <a href="#" class="w3-bar-item w3-button">Link 2</a>
                            <a href="#" class="w3-bar-item w3-button">Link 3</a>
                        </div>
                    </div>


                    <button @click="send()" class="btn waves-effect waves-light blue" type="submit" name="action">SEND
                        <i class="material-icons right">send</i>
                    </button>
                </div>

            </div>


        </div>
    </div>


</template>

<script>
    document.addEventListener('DOMContentLoaded', function () {
        var elems = document.querySelectorAll('.dropdown-trigger');
        var instances = M.Dropdown.init(elems, options);
    });

    export default {


        name: 'conversation',


        data() {


            return {


                messages: [
                    {message: 'Hello!', timestamp: 'time: 2:34 date: 2.4.2019', name: 'me'},
                    {message: 'Foo', timestamp: 'time: 2:35 date: 2.4.2019', name: 'Andro'},
                    {message: 'Bar', timestamp: 'time: 2:36 date: 2.4.2019', name: 'me'},
                    {message: 'Hello!', timestamp: 'time: 2:37 date: 2.4.2019', name: 'Andro'},
                    {message: 'Foo', timestamp: 'time: 2:38 date: 2.4.2019', name: 'me'},
                    {message: 'Bar', timestamp: 'time: 2:39 date: 2.4.2019', name: 'Andro'},
                    {message: 'Blabla', timestamp: 'time: 2:44 date: 2.4.2019', name: 'Andro'},


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

        }


    }
</script>

<style scoped>


    .dropdown {


        float: left;
        margin-bottom: 5px;
    }

    .dropbtn:hover, .dropbtn:focus {
        background-color: #2980B9;
    }

    .dropdown-content a {
        color: black;
        padding: 12px 16px;
        text-decoration: none;
        display: block;
    }

    .col {
        height: 100%;
    }

    body, html {
        height: 100%;
        margin: 0;
        background: #7F7FD5;
        background: -webkit-linear-gradient(to right, #91EAE4, #86A8E7, #7F7FD5);
        background: linear-gradient(to right, #91EAE4, #86A8E7, #7F7FD5);
    }

    .msg_time {
        position: absolute;
        left: 0;
        bottom: -15px;
        color: grey;
        font-size: 10px;
    }

    .msg_card_body {
        overflow-y: auto;
        height: 400px;

    }

    .card {
        height: 400px;
        border-radius: 15px !important;


    }


    .msg_cont_area {

        margin: 15px;
    }

    msg_cont_send_area {

        margin: 15px;
        float: right;
        margin-bottom: 5px;
    }

    .msg_cotainer {
        margin-top: auto;
        margin-bottom: auto;
        margin-left: 10px;
        border-radius: 25px;
        background-color: #82ccdd;
        padding: 10px;
        position: relative;

    }

    .msg_cotainer_send {
        margin-top: auto;
        margin-bottom: auto;
        margin-right: 10px;
        margin-left: 10px;

        border-radius: 25px;
        background-color: #78e08f;
        padding: 10px;
        position: relative;
    }

    .msg_time_send {
        position: absolute;
        right: 0;
        bottom: -15px;
        color: grey;
        font-size: 10px;
    }

    .textinputboard {
        height: 100px;
        border-radius: 15px !important;
        background: linear-gradient(white, grey);;
    }

    .topinfoboard {
        margin-top: 10px;

        height: auto;
        border-radius: 15px !important;
        background: grey;;


    }

    .type_msg:focus {
        box-shadow: none !important;
        outline: 0px !important;
    }


    .send_btn {
        border-radius: 0 15px 15px 0 !important;
        background-color: rgba(0, 0, 0, 0.3) !important;
        border: 0 !important;
        color: white !important;
        cursor: pointer;
    }

    .sendbtnarea {
        float: right;
        margin-right: 10px;
    }

    .user_info {
        margin-top: auto;
        margin-bottom: auto;
        margin-left: 15px;
        color: white;
        text-align: center;
    }

    .whowith {
        font-size: large;
    }

    .messagecount {
        font-size: small;
        color: white;
        margin-left: 10px;
    }

    .sendingsection {
        margin-top: 10px;
        height: 100px;
        border-radius: 15px !important;


    }


    .materialize-textarea {
        max-height: 100px;
        overflow: scroll;
    }


</style>


