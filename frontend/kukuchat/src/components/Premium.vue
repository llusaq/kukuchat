<template>
    <div id="premium" class="modal">
        <div class="modal-header">
            <h4>Premium account </h4>
            <a class="modal-close" ><i class="material-icons small left">clear</i></a>
        </div>
        <div class="modal-content">
            <h5>Advantages of a premium account</h5>
            <ul>
                <li>Use more than 2 chat services</li>
                <li>Karma +10</li>
            </ul>
        </div>
        <a class="premium-btn">Get Premium</a>
    </div>
</template>

<script>

export default {
    name: 'addAccount',
    components: {
    },
    data() {
        return {
           
        }
    },
    methods: {
        
    },
}
</script>

<style scoped>

.modal {
    background-image: url("../assets/colorful-background.jpg");
    height: 510px;
    background-size: 100%;
    cursor: default;
}

.modal-close {
    float: right;
}

i {
    position: absolute;
    top: 15px;
    right: 20px;
    cursor: pointer;
    z-index: 9999;
    color: rgba(255, 255, 255, 0.90);
}

.modal-header {
    padding: 10px 0;
}

.modal-header h4 {
    display: inline-block;
    color: rgba(255, 255, 255, 0.90);
}

.modal-content {
    text-align: left;
    color: rgba(255, 255, 255, 0.90);
    padding-top: 80px;
    padding-left: 100px;
}

ul li{
    list-style-type: disc;
    margin-left: 18px;
}

.premium-btn {
    padding: 20px;
    background: rgba(255, 255, 255, 0.90);
    color: rgba(0,0,0,0.80);
    font-weight: 650;
    margin-top: 80px;
    display: inline-block;
    cursor: pointer;
}

</style>
