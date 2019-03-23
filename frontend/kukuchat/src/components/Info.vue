<template>
    <div class="col m5 l6 pull-l1 center-align left-side">
        <h5>CooCoo chat for everyone</h5>
        <p>Keep all your favorite communication chats in one service</p>
        <img class="main-img" src="../../public/image.png" alt="image">
    </div>
</template>

<style>
.main-img {
    width: 450px;
    height: 450px;
}

@media only screen and (max-width: 1000px) and (min-width: 600px) {
    .main-img {
        width: 250px;
        height: 250px;
    }
}

@media only screen and (max-width: 600px) {
    .card {
        box-shadow: none;
    }

    .left-side {
        display: none;
    }
}
</style>
