<template>
    <div class="row settings">
    <a class="col l3 m4 menu-el"  :style="{backgroundColor: style}" @click="settings()">
        <i class="material-icons left">{{ icon }}</i>
        CooCoo
    </a>
    <div class="col card l3 m4" v-if="opened">
        <div class="card-content">
            <div class="row">
                <a class="btn">Add account</a>
            </div>
        </div>
    </div>
    <a class="col l9 m8 menu-el">
        {{ currentChat }}
    </a>
    </div>
</template>

<script>
export default {
    name: 'dropdownmenu',
    data() {
        return {
            icon: 'menu',
            style: 'white',
            opened: false
        }
    },
    methods: {
        settings() {
            this.icon = this.icon === 'menu' ? 'clear' : 'menu';
            this.style = this.style === 'white' ? '#dcdcdc' : 'white';
            this.opened = !this.opened;
        }
    },
    props: ['currentChat'],
}
</script>

<style scoped>
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
    background-color: #dcdcdc !important;
}

.row {
    height: auto;
    margin-bottom: 0;
}

.card {
    position: absolute;
    top: 47px;
    box-shadow: 0px 4px 2px -2px rgba(0,0,0,0.12);
    background-color: #fafafa;
}

</style>


