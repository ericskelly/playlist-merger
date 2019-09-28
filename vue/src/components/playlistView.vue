<template>
    <div>
        
    </div>
</template>

<script lang="ts">
    import { Prop, Vue } from 'vue-property-decorator';
    import Component from 'vue-class-component';
    import main from '../components/main/main.vue';
    import SpotifyWebApi from 'spotify-web-api-js'
    import router from '../router';

    const spotify = new SpotifyWebApi();

</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>