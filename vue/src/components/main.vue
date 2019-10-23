<template>
  <div>
    <nav class="navbar navbar-inverse navbar-fixed-top header">
      <a class="navbar-brand">Playlist Merger</a>
      <form class="form-inline">
        <input class="form-control mr-sm-2" type="search" placeholder="Search" aria-label="Search" />
        <button class="btn btn-outline-success my-2 my-sm-0" type="submit">Search</button>
      </form>
    </nav>
    <div class="container-fluid">
      <div class="row">
        <!--<div class="col-sm-4 col-md-3 col-lg-2 sidenav">
          <ul id="playlists">
            <li
              v-for="playlist in playlists"
              v-bind:key="playlist.id"
              :style="listItemStyle(playlist.id)"
              @click="openPlayList(playlist)"
            >{{playlist.name}}</li>
          </ul>
        </div>-->
        <template>
          <v-card class="mx-auto" max-width="500" tile width="300">
            <v-list rounded>
              <v-subheader>Playlists</v-subheader>
              <v-list-item-group
                multiple
                v-model="selected"
                active-class="pink--text"
                style="text-align: left"
              >
                <v-list-item
                  v-for="playlist in playlists"
                  v-bind:key="playlist.id"
                  @click="openPlayList(playlist)"
                >
                  <template v-slot:default="{ active, toggle }">
                    <v-list-item-content>
                      <v-list-item-title v-text="playlist.name"></v-list-item-title>
                    </v-list-item-content>
                  </template>
                </v-list-item>
              </v-list-item-group>
            </v-list>
          </v-card>
        </template>
        <div class="col">
          <section>
            <div class="container">
              <!--<template>
                <v-row justify="center">
                  <v-expansion-panels popout>
                    <v-expansion-panel>
                      <v-expansion-panel-header>Item</v-expansion-panel-header>
                      <v-expansion-panel-content>
                        
                      </v-expansion-panel-content>
                    </v-expansion-panel>
                  </v-expansion-panels>
                </v-row>
              </template>-->
              <template>
                <div class="text-center">
                  <v-menu offset-y>
                    <template v-slot:activator="{ on }">
                      <v-btn color="primary" dark v-on="on">Dropdown</v-btn>
                    </template>
                    <v-list>
                      <v-list-item v-for="(item, index) in items" :key="index">
                        <v-list-item-title>{{ item.title }}</v-list-item-title>
                      </v-list-item>
                    </v-list>
                  </v-menu>
                </div>
              </template>
              <div class="table-responsive">
                <table class="table">
                  <thead>
                    <tr style="text-align: left;">
                      <th
                        v-for="playlist in playlistSongsSelected"
                        v-bind:key="playlist.playlistID"
                      >{{playlist.playlistName}}</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td
                        v-for="(playlist, index) in playlistSongsSelected"
                        v-bind:key="playlist.playlistID"
                      >
                        <ul class="songsLists">
                          <li
                            v-for="songs in playlistSongsSelected[index].songs"
                            v-bind:key="songs.song"
                          >{{songs.song}}</li>
                        </ul>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </section>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Prop, Vue } from "vue-property-decorator";
import Component from "vue-class-component";
import SpotifyWebApi from "spotify-web-api-js";
import router from "../router";

const spotify = new SpotifyWebApi();

interface playlist {
  name: string;
  id: string;
}

interface playlistSongs {
  playlistName: string;
  playlistID: number;
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
  private playlists: playlist[] = [];
  private playlistSongsSelected: playlistSongs[] = [];
  private selected: any = [0, 1, 2, 3, 4];
  created() {
    spotify.getUserPlaylists().then(
      response => {
        console.log(response);
        console.log(response.items[0]);
        response.items.forEach(playlist => {
          let playlist1: playlist = { name: playlist.name, id: playlist.id };
          this.playlists.push(playlist1);
          this.openPlayList(playlist1);
        });
      },
      function(err) {
        console.log(err.responseXML);
        if (err.responseXML === null) {
          router.push("/login");
        }
      }
    );
  }
  GetStuff() {
    spotify.getMe().then(response => {
      console.log(response);
    });
  }

  openPlayList(aplayList: playlist) {
    console.log(aplayList);
    spotify.getPlaylist(aplayList.id).then(response => {
      console.log(response);
      this.ParsePlaylist(response);
    });
  }

  ParsePlaylist(playlist: any) {
    let playlistIndex: number = this.playlistSongsSelected
      .map(x => x.playlistID)
      .indexOf(playlist.id);
    if (
      this.playlistSongsSelected.map(x => x.playlistID).includes(playlist.id)
    ) {
      this.playlistSongsSelected.splice(playlistIndex, 1);
    } else {
      let playlistItems1: playlistItem[] = [];
      playlist.tracks.items.forEach(item => {
        let artistsTemp: string = "";
        let artists: string = "";
        item.track.artists.forEach(artist => {
          artistsTemp = artistsTemp + artist.name + ", ";
        });
        if (artistsTemp.length > 0) {
          artists = artistsTemp.substring(0, artistsTemp.length - 2);
        }
        let playlistItem1: playlistItem = {
          song: item.track.name,
          artist: artists
        };
        playlistItems1.push(playlistItem1);
      });
      let playlistSongs1: playlistSongs = {
        playlistName: playlist.name,
        playlistID: playlist.id,
        songs: playlistItems1
      };
      console.log(playlistSongs1);
      this.playlistSongsSelected.push(playlistSongs1);

      console.log(this.playlistSongsSelected);
    }
  }

  listItemStyle(playlistId: number) {
    if (
      this.playlistSongsSelected.map(x => x.playlistID).includes(playlistId)
    ) {
      return "color: white;";
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
/* The navigation menu links */
.sidenav li {
  padding-top: 15px;
  text-decoration: none;
  font-size: 25px;
  display: block;
  color: #818181;
  text-align: left;
  list-style-type: none;
  cursor: pointer;
  word-wrap: break-word;
}

.sidenav v-list-item-content {
  padding-top: 15px;
  text-decoration: none;
  font-size: 25px;
  display: block;
  color: #818181;
  text-align: left;
  list-style-type: none;
  cursor: pointer;
  word-wrap: break-word;
}

.sidenav ul {
  padding-inline-start: 10px;
}

/* When you mouse over the navigation links, change their color */
.sidenav li:hover {
  color: #f1f1f1;
}

.sidenav li:active {
  color: #f1f1f1;
}

.header {
  background-color: #282828;
}

.table {
  margin: 0 auto;
  min-width: 60%;
  width: auto !important;
  max-width: 100%;
}

.table-responsive {
  display: block;
  width: 100%;
  overflow-x: auto;
}

.songsLists {
  list-style-type: none;
  text-align: left;
}

/* On smaller screens, where height is less than 450px, change the style of the sidebar (less padding and a smaller font size) */
@media screen and (max-height: 450px) {
  .sidenav {
    padding-top: 15px;
  }
  .sidenav a {
    font-size: 18px;
  }
}

@media (min-width: 544px) {
  .sidenav {
    bottom: 0;
    left: 0;
    z-index: 1000;
    display: block;
    padding: 0;
    padding-bottom: 0;
    overflow-x: hidden;
    overflow-y: hidden;
    background-color: #282828;
    border-top: 1px solid #181818;
  }
}
</style>