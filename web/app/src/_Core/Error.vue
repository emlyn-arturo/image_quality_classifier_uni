<template>
    <div v-if="message" class="tsno-error">
        <p><strong>Ein Fehler ist aufgetreten!</strong></p>
        {{message}}
    </div>
</template>


<script>
    export default {
        props: ['message']
    }
</script>


<style scoped lang="sass" rel="stylesheet/sass">
    .tsno-error
        color: white
        background: #C62828
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.25)
        border-radius: 4px
        padding: 20px
        text-align: center

        p
            width: auto
            margin: auto
            text-align: center

</style>
