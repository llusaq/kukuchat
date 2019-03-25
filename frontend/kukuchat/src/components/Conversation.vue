<template>
    <div class="col l9 m8">
        <div class="topinfoboard">
            <div class="user_info">
                <div class="whowith">Chat with Andro</div>
            </div>
            <div class="messagecount">78 Messages</div>
        </div>
        <div class="messageboard">
            <div class="card">
                <div class="holder">

                    <div class="msg_card_body">

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


                    </div>
                </div>
            </div>
        </div>

        <div class="textinputboard">
            <textarea name="" class=" type_msg" placeholder="Type your message..."></textarea>
            <div class="sendbtnarea">
                <button class="btn waves-effect waves-light" type="submit" name="action">SEND
                    <i class="material-icons right">send</i>
                </button>
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        name: 'conversation',
        date() {
            return {}
        }
    }
</script>

<style scoped>
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
        color: rgba(255, 255, 255, 0.5);
        font-size: 10px;
    }

    .msg_card_body {
        overflow-y: auto;
        height: 400px;

    }

    .card {
        height: 400px;
        border-radius: 15px !important;
        background-color: rgba(0, 0, 0, 0.4) !important;

    }


    .msg_cont_area {

        margin: 15px;
    }

    msg_cont_send_area {

        margin: 15px;
        float: right;
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
        color: rgba(255, 255, 255, 0.5);
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
        background: linear-gradient(black, grey);;


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
</style>


