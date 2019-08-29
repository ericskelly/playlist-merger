<template>
  <div class="hello">
     <button v-on:click="getStuff()">get user details</button>
     <SpotifyLogin>  </SpotifyLogin>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';
import SpotifyWebApi from 'spotify-web-api-js'
import SpotifyLogin from './components/spotifyLogin.vue';
import router from '../router';

const spotify = new SpotifyWebApi();

@Component({
    components: {}
})
export default class main extends Vue {

    private fromLogin: string = '';

    onLoginSend(value: string){
        this.fromLogin = value;
    }

    getStuff(){
        spotify.getMe().then((response) => {
        console.log(response)
        })
    }

}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>