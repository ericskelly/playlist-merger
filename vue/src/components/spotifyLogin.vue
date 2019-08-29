<template>
  <div class="hello">
    <p>{{msg}}</P>
     <a href='http://127.0.0.1:5000/login'>
        <button>Login with spotify</button>
     </a> 
     <button v-on:click="getStuff()">get user details</button>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';
import axios from 'axios';
import SpotifyWebApi from 'spotify-web-api-js'
import router from '../router';

const spotify = new SpotifyWebApi();

@Component
export default class SpotifyLogin extends Vue {
  @Prop() private msg: string = "testing";
  private params: any;
  created() {
    this.params = this.getHashParams();
    if (this.params.access_token){
      spotify.setAccessToken(this.params.access_token);
      router.push('about');
      console.log(this.params.access_token)
    }
  }
  
  emitToMain (access_token:any){
    this.$emit('onLoginSend', access_token);
  }

  getHashParams(){
    var hashParams = {} as any;
    var e, r = /([^&;=]+)=?([^&;]*)/g,
        q = window.location.hash.substring(1);
    while ( e = r.exec(q)) {
      hashParams[e[1]] = decodeURIComponent(e[2]);
    }
    return hashParams;
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