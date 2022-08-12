<template>
    <div id="app">
        <router-view class="main"></router-view>
    </div>
</template>


<script>
    export default {
        name: "home"
    }
</script>


<style lang="sass" rel="stylesheet/sass">
    body
        margin: 0
        padding: 0
        color: #555

        *
            box-sizing: border-box

        .circle-promoted
            width: 46vmin
            height: 46vmin
            margin: 10vmin auto
            position: relative
            border: 0 solid white
            border-radius: 100%
            box-shadow: 0 6px 18px rgba(0, 0, 0, 0.35)
            background-size: cover
            background-repeat: no-repeat
            background-position: center

            &:after
                content: ""
                position: absolute
                left: -2vmin
                top: -2vmin
                right: -2vmin
                bottom: -2vmin
                border: 2vmin solid transparent
                border-radius: 100%
                pointer-events: none
                z-index: -1

        p
            width: 50vmin
            margin: 10vmin auto
            text-align: center

        h1, h2, h3, h4, h5
            font-family: "Sansation", "Verdana", sans-serif
            text-align: center

        h2
            font-size: 250%
</style>
<style scoped lang="sass" rel="stylesheet/sass">

</style>
