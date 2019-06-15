<template>
    <p>{{ greeting }} World!</p>
</template>

<script>
export default {
    name: 'Hello',
    data() {
        return {
            greeting: "Hello"
        }
    }
}

</script>

<style scoped>
p {
    text-align: center;
}
</style>
