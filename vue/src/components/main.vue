<template>
    <div>
        <nav class="navbar navbar-light bg-light justify-content-between">
            <a class="navbar-brand">Navbar</a>
            <form class="form-inline">
                <input class="form-control mr-sm-2" type="search" placeholder="Search" aria-label="Search">
                <button class="btn btn-outline-success my-2 my-sm-0" type="submit">Search</button>
            </form>
        </nav>
        <div class="sidenav">
            <ul id="playlists">
                <li v-for="playlist in playlists" v-bind:key="playlist.id" @click="openPlayList(playlist)">
                {{playlist.name}}
                </li>
                <li>omgthisissolongomgomgomgomgomg</li>
            </ul>
        </div>
    </div>
</template>

<script lang="ts">
    import { Prop, Vue } from 'vue-property-decorator';
    import Component from 'vue-class-component';
    import SpotifyWebApi from 'spotify-web-api-js'
    import router from '../router';

    const spotify = new SpotifyWebApi();

    interface playlist{
        name: string;
        id: string;
    }

    interface playlistSongs {
        playlistName: string;
        songs: playlistItem[];
    }

    interface playlistItem {
        song: string;
        artist: string;
    }

    @Component({
        components: {}
    })
    export default class main extends Vue {

        
        private playlists:playlist[] = [];
        created(){           
            spotify.getUserPlaylists().then((response) =>{
                console.log(response);
                console.log(response.items[0])
                response.items.forEach(playlist => {
                    let playlist1: playlist = {name: playlist.name, id: playlist.id}
                    this.playlists.push(playlist1);
                });
            }, function(err){
                console.log(err.responseXML);
                if (err.responseXML === null){
                    router.push("/login")
                }
            })
            
        }
        getStuff(){
            spotify.getMe().then((response) => {
                console.log(response);
            })
        }

        openPlayList(aplayList:playlist){
            console.log(aplayList);
            spotify.getPlaylist(aplayList.id).then((response)=> {
                console.log(response)
            })
        }
    }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.sidenav {
  height: 100%; /* Full-height: remove this if you want "auto" height */
  width: 250px; /* Set the width of the sidebar */
  position: fixed; /* Fixed Sidebar (stay in place on scroll) */
  z-index: 1; /* Stay on top */
  top: 0; /* Stay at the top */
  left: 0;
  background-color: #111; /* Black */
  padding-top: 20px;
  
}

/* The navigation menu links */
.sidenav li{
  padding-top: 15px;
  text-decoration: none;
  font-size: 25px;
  color: #818181;
  display: block;
  text-align: left;
  list-style-type: none;
  cursor: pointer;
  word-wrap:break-word;
}

.sidenav ul{
    padding-inline-start: 10px;
}

/* When you mouse over the navigation links, change their color */
.sidenav li:hover {
  color: #f1f1f1;
}

/* Style page content */
.main {
  margin-left: 250px; /* Same as the width of the sidebar */
  padding: 0px 10px;
}

/* On smaller screens, where height is less than 450px, change the style of the sidebar (less padding and a smaller font size) */
@media screen and (max-height: 450px) {
  .sidenav {padding-top: 15px;}
  .sidenav a {font-size: 18px;}
}
</style>