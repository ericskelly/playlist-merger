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
      <div class="row" style="height: 100vh;">
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
        <div class="col">
          <div>
            <b-dropdown id="dropdown-1" text="Merge" class="m-md-2">
              <b-dropdown-item @click="SortTop(5)">Top 5</b-dropdown-item>
              <b-dropdown-divider></b-dropdown-divider>
              <b-dropdown-item @click="SortTop(10)">Top 10</b-dropdown-item>
              <b-dropdown-item @click="SortTop(50)">Top 50</b-dropdown-item>
            </b-dropdown>
          </div>
          <section>
            <div class="container">
              <v-row dense>
                <v-col
                  v-for="(playlist, index) in playlistSongsSelected"
                  v-bind:key="playlist.playlistID"
                  :cols="3"
                >
                  <v-card class="mx-auto" tile>
                    <v-card-title>
                      <div style="display: flex; justify-content: space-between; width: 100%">
                        <div>{{playlistSongsSelected[index].playlistName}}</div>
                        <div>
                          <b-dropdown id="dropdown-1" offset="-120px" size="sm" text class>
                            <b-dropdown-header id="dropdown-header-label1">Merge Options</b-dropdown-header>
                            <b-dropdown-divider></b-dropdown-divider>
                            <b-dropdown-header id="dropdown-header-label1">Top Songs</b-dropdown-header>
                            <b-dropdown-item @click="SortTop(5)">Top 5</b-dropdown-item>

                            <b-dropdown-item @click="SortTop(10)">Top 10</b-dropdown-item>
                            <b-dropdown-item @click="SortTop(50)">Top 50</b-dropdown-item>
                            <b-dropdown-header id="dropdown-header-label2">Genre</b-dropdown-header>
                          </b-dropdown>
                        </div>
                      </div>
                    </v-card-title>
                    <v-list>
                      <v-list-item
                        two-line
                        v-for="songs in playlistSongsSelected[index].songs"
                        v-bind:key="songs.song"
                        v-bind:style="[songs.highlight ? {'color': '#008000'} : {'color': '#000000'}]"
                        style="text-align: left; max-height: 50px"
                      >
                        <v-list-item-content>
                          <v-list-item-title>{{songs.song}}</v-list-item-title>
                          <v-list-item-subtitle>{{songs.artist}}</v-list-item-subtitle>
                        </v-list-item-content>
                      </v-list-item>
                    </v-list>
                  </v-card>
                </v-col>
              </v-row>
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
  songId: string;
  song: string;
  artist: string;
  highlight: boolean;
}

@Component({
  components: {}
})
export default class main extends Vue {
  private playlists: playlist[] = [];
  private playlistSongsSelected: playlistSongs[] = [];
  private selected: number[] = [];
  private topSelectedSongsForMerge: playlistItem[] = [];
  created() {
    spotify.getUserPlaylists().then(
      response => {
        let playlistCount = 0;
        response.items.forEach(playlist => {
          let playlist1: playlist = { name: playlist.name, id: playlist.id };
          this.playlists.push(playlist1);
          this.openPlayList(playlist1);
          this.selected.push(playlistCount);
          playlistCount += 1;
        });
      },
      function (err) {
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
    if (this.playlistSongsSelected.map(x => x.playlistID).includes(playlist.id)) {
      this.playlistSongsSelected.splice(playlistIndex, 1);
    } else {
      let totalPlayListSongs: number = playlist.tracks.total;
      let playlistItems1: playlistItem[] = [];

      let numberCalls = Math.ceil(totalPlayListSongs / 100);
      let promiseArray = [];
      let offset = 0;
      for (let i = 0; i < numberCalls; ++i) {
        let promise = spotify.getPlaylistTracks(playlist.id, { 'limit': 100, 'offset': offset })
        promiseArray.push(promise);
        offset += 100;
      }

      Promise.all(promiseArray).then(setOfTracks => {
        setOfTracks.forEach(set => {
          set.items.forEach(item => {
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
              artist: artists,
              songId: item.track.id,
              highlight: false
            };
            playlistItems1.push(playlistItem1);
          });
        });
      });

      let playlistSongs1: playlistSongs = {
        playlistName: playlist.name,
        playlistID: playlist.id,
        songs: playlistItems1
      };
      this.playlistSongsSelected.push(playlistSongs1);

    }
  }

  SortTop(numberItems: number) {
    spotify.getMyTopTracks({ 'limit': numberItems }).then(topSongs => {
      let topSongsArray = topSongs.items.sort(function (a, b) { return b.popularity - a.popularity });

      console.log(topSongsArray);
      this.playlistSongsSelected.forEach(playlist => {
        playlist.songs.forEach(song => {
          if (topSongsArray.map(x => x.id).includes(song.songId) || topSongsArray.map(x => x.name).includes(song.song)) {
            //this.topSelectedSongsForMerge.push(song);
            song.highlight = true;
          }
        })
      })
    });
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

.selectedMerge {
  color: green;
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