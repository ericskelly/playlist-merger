<template>
  <div>
    <link href="https://fonts.googleapis.com/css?family=Material+Icons" rel="stylesheet" />
    <link
      href="https://cdn.jsdelivr.net/npm/@mdi/font@4.x/css/materialdesignicons.min.css"
      rel="stylesheet"
    />
    <nav class="navbar navbar-inverse navbar-fixed-top header">
      <a class="navbar-brand" style="color: #1DB954">Spotify Playlist Merger</a>
      <form class="form-inline">
        <input class="form-control mr-sm-2" type="search" placeholder="Search" aria-label="Search" />
        <button class="btn btn-outline-success my-2 my-sm-0" type="submit">Search</button>
      </form>
    </nav>
    <div class="container-fluid">
      <div class="row">
        <v-card dark class="mx-auto" max-width="500" tile width="300" style="min-height: 100vh;">
          <v-list rounded style="background-color">
            <v-subheader>Playlists</v-subheader>
            <v-list-item-group multiple v-model="selected" style="text-align: left">
              <v-list-item
                v-for="playlist in playlists"
                v-bind:key="playlist.id"
                @click="OpenPlayList(playlist)"
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
        <div class="col" style="background-color: #353535">
          <section>
            <div class="container" v-if="playlistsLoaded">
              <div style="border: 1px solid #1DB954">
                <v-row>
                  <v-col v-if="topSelectedSongsForMerge.length > 0" :justify="start">
                    <v-btn @click="ShowOrHide()">Merged Playlist</v-btn>
                  </v-col>
                  <v-col :justify="start">
                    <v-btn @click="ShowOrHideSongs()">Display Songs</v-btn>
                  </v-col>
                  <v-col>
                    <b-dropdown id="dropdown-1" text="Merge" class="m-md-2">
                      <b-dropdown-item @click="SortTop(5)">Top 5</b-dropdown-item>
                      <b-dropdown-divider></b-dropdown-divider>
                      <b-dropdown-item @click="SortTop(10)">Top 10</b-dropdown-item>
                      <b-dropdown-item @click="SortTop(50)">Top 50</b-dropdown-item>
                    </b-dropdown>
                  </v-col>
                  <v-col></v-col>
                </v-row>
              </div>
              <v-row v-if="columns != -1">
                <v-col :cols="3" v-if="topSelectedSongsForMerge.length > 0">
                  <v-card
                    style="border: 1px solid #1DB954"
                    shaped
                    class="mx-auto"
                    tile
                    dark
                    v-if="showMerged"
                  >
                    <v-card-title>
                      <div style="display: flex; justify-content: space-between; width: 100%">
                        <v-chip outlined>Merged Playlist</v-chip>
                        <div data-app>
                          <!--<v-btn color="primary" dark @click="dialog = true"></v-btn>-->

                          <v-icon color="primary" dark v-on="on" @click="dialog = true">create</v-icon>

                          <v-dialog v-model="dialog" max-width="500">
                            <v-card>
                              <v-card-title class="headline">Create Playlist</v-card-title>
                              <v-card-text>
                                <v-container fluid>
                                  <v-row>
                                    <v-col cols="12">
                                      <v-text-field id="nameField" label="Playlist Name*" required></v-text-field>
                                    </v-col>
                                    <v-col cols="12">
                                      <v-text-field id="descriptionField" label="Description"></v-text-field>
                                    </v-col>
                                    <v-col>
                                      <v-checkbox
                                        v-model="newPlaylistPublic"
                                        label="Public Playlist?"
                                      ></v-checkbox>
                                    </v-col>
                                    <v-col>
                                      <v-checkbox
                                        v-model="newPlaylistCollaborative"
                                        label="Collaborative Playlist?"
                                      ></v-checkbox>
                                    </v-col>
                                  </v-row>
                                </v-container>
                                <small>*indicates required field</small>
                              </v-card-text>
                              <v-card-actions>
                                <v-spacer></v-spacer>

                                <v-btn color="green darken-1" text @click="dialog = false">Cancel</v-btn>

                                <v-btn
                                  color="green darken-1"
                                  text
                                  @click="CreateMergedPlaylist()"
                                >Create</v-btn>
                              </v-card-actions>
                            </v-card>
                          </v-dialog>
                        </div>
                      </div>
                    </v-card-title>
                    <v-divider></v-divider>
                    <v-list class="scrollStyle" max-height="500px">
                      <v-list-item
                        two-line
                        v-for="songs in topSelectedSongsForMerge"
                        v-bind:key="songs.song"
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
                <v-col
                  v-for="(playlist, index) in playlistSongsSelected"
                  v-bind:key="playlist.playlistID"
                  v-bind:cols="3"
                >
                  <v-card class="mx-auto" tile dark>
                    <v-card-title>
                      <div style="display: flex; justify-content: space-between; width: 100%">
                        <v-chip outlined>{{playlistSongsSelected[index].playlistName}}</v-chip>
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
                    <v-divider></v-divider>
                    <v-list class="scrollStyle" max-height="500px" v-if="showSongs">
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
  numberSongs: number;
}

interface playlistItem {
  songId: string;
  song: string;
  artist: string;
  highlight: boolean;
  uri: string;
}

@Component({
  components: {}
})
export default class main extends Vue {
  private playlists: playlist[] = [];
  private playlistSongsSelected: playlistSongs[] = [];
  private selected: number[] = [];
  private topSelectedSongsForMerge: playlistItem[] = [];
  private playlistCount: number = 0;
  private showMerged: boolean = true;
  private playlistsLoaded: boolean = false;
  private showSongs: boolean = true;
  private userID: string = '';
  private dialog: boolean = false;
  private newPlaylistPublic: boolean = true;
  private newPlaylistCollaborative: boolean = false;
  created() {
    spotify.getMe().then(user => {
      this.userID = user.id;
    })
    this.LoadPlaylists();
  }

  LoadPlaylists() {
    this.playlists = [];
    this.selected = [];
    this.playlistSongsSelected = [];
    this.playlistsLoaded = false;
    this.playlistCount = 0;
    spotify.getUserPlaylists().then(
      response => {
        response.items.forEach(playlist => {
          let playlist1: playlist = { name: playlist.name, id: playlist.id };
          this.playlists.push(playlist1);
          //this.OpenPlayList(playlist1);
          this.selected.push(this.playlistCount);
          this.playlistCount += 1;
        });
      },
      function (err) {
        console.log(err.responseXML);
        if (err.responseXML === null) {
          router.push("/login");
        }
      }
    ).then(() => this.OpenPlayLists());
  }

  OpenPlayLists() {
    let promiseArray: any = [];
    this.playlists.forEach(playlist => {
      let promise = spotify.getPlaylist(playlist.id);
      promiseArray.push(promise);
    });
    Promise.all(promiseArray).then(playlists => {
      playlists.forEach(playlist => {
        this.ParsePlaylist(playlist);
      })
    }).then(() => this.playlistsLoaded = true);
  }

  OpenPlayList(aplayList: playlist) {
    spotify.getPlaylist(aplayList.id).then(response => {
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

      let numberSongs = 0;
      Promise.all(promiseArray).then(setOfTracks => {
        setOfTracks.forEach(set => {
          console.log(set);
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
              uri: item.track.uri,
              highlight: false
            };
            playlistItems1.push(playlistItem1);
            numberSongs += 1;
          });
        });
      });

      let playlistSongs1: playlistSongs = {
        playlistName: playlist.name,
        playlistID: playlist.id,
        songs: playlistItems1,
        numberSongs: numberSongs
      };
      this.playlistSongsSelected.push(playlistSongs1);
      console.log(playlist.name);
    }
  }

  SortTop(numberItems: number) {
    // TODO: think there is a bug in here duplicating songs - for top 10 click etc
    this.topSelectedSongsForMerge = [];
    spotify.getMyTopTracks({ 'limit': numberItems }).then(topSongs => {
      let topSongsArray = topSongs.items.sort(function (a, b) { return b.popularity - a.popularity });

      this.playlistSongsSelected.forEach(playlist => {
        playlist.songs.forEach(song => {
          if (topSongsArray.map(x => x.id).includes(song.songId) || topSongsArray.map(x => x.name).includes(song.song)) {
            if (!this.topSelectedSongsForMerge.map(x => x.songId).includes(song.songId)) {
              this.topSelectedSongsForMerge.push(song);
              song.highlight = true;
            }
          }
        })
      })
    });
  }

  CreateMergedPlaylist() {
    this.dialog = false;
    let newPlaylistName = (<HTMLInputElement>document.getElementById("nameField")).value;
    let newPlaylistDescription = (<HTMLInputElement>document.getElementById("descriptionField")).value;
    spotify.createPlaylist(this.userID, { 'name': newPlaylistName, 'description': newPlaylistDescription, 'public': this.newPlaylistPublic, 'collaborative': this.newPlaylistCollaborative }).then(createResponse => {
      console.log(createResponse);
      let newPlaylistId = createResponse.id;
      let songsToAdd = this.topSelectedSongsForMerge.map(x => x.uri);
      spotify.addTracksToPlaylist(newPlaylistId, songsToAdd).then(addSongsResponse => {
        console.log(addSongsResponse);
        this.LoadPlaylists();
      });
    });
  }

  SortIndividualTop(numberItems: number, playlist: playlistSongs) {

  }

  SortGenre(playlist: playlistSongs) {

  }

  ShowOrHide() {
    if (this.showMerged === true) {
      this.showMerged = false;
    } else {
      this.showMerged = true;
    }
  }

  ShowOrHideSongs() {
    if (this.showSongs == true) {
      this.showSongs = false;
    } else {
      this.showSongs = true;
    }
  }

}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
/* The navigation menu links */
.scrollStyle {
  overflow-y: scroll;
  scrollbar-width: none; /* Firefox */
  -ms-overflow-style: none; /* Internet Explorer 10+ */
}
.scrollStyle::-webkit-scrollbar {
  /* WebKit */
  width: 0;
  height: 0;
}

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