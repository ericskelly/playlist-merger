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
              <div style="border: 1px solid #1DB954; height: 100px">
                <!--<v-row>
                  <v-col v-if="selectedSongsForMerge.length > 0" :justify="start">
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
                </v-row>-->
                <v-col cols="12">
                  <v-row justify="center">
                    <v-col>
                      <v-select label="Top Songs"></v-select>
                    </v-col>
                    <v-col>
                      <v-select label="Align"></v-select>
                    </v-col>
                    <v-col></v-col>
                  </v-row>
                </v-col>
              </div>
              <v-row v-if="columns != -1">
                <v-col :cols="3" v-if="selectedSongsForMerge.length > 0">
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
                    <v-card-subtitle style="float: right">
                      <v-icon v-on="on" @click="UndoLastMerge()">undo</v-icon>
                    </v-card-subtitle>
                    <v-divider></v-divider>
                    <v-list class="scrollStyle" max-height="500px">
                      <v-list-item
                        two-line
                        v-for="songs in selectedSongsForMerge"
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
                          <b-dropdown
                            id="dropdown-1"
                            offset="-120px"
                            size="sm"
                            text
                            class
                            no-caret
                            variant="transparent"
                          >
                            <template v-slot:button-content>
                              <v-icon>settings</v-icon>
                            </template>
                            <b-dropdown-header id="dropdown-header-label1">Merge Options</b-dropdown-header>
                            <b-dropdown-divider></b-dropdown-divider>
                            <b-dropdown-header id="dropdown-header-label1">Top Songs</b-dropdown-header>
                            <b-dropdown-item @click="SortTop(5)" style="min-width:250px">Top 5</b-dropdown-item>

                            <b-dropdown-item @click="SortTop(10)">Top 10</b-dropdown-item>
                            <b-dropdown-item @click="SortTop(50)">Top 50</b-dropdown-item>
                            <b-dropdown-divider></b-dropdown-divider>
                            <b-dropdown-form>
                              <b-form-group
                                label="Genre"
                                label-for="dropdown-form-genre"
                                @submit.stop.prevent
                              >
                                <b-form-input
                                  v-bind:id="playlist.playlistID"
                                  list="options-list"
                                  size="sm"
                                  @input="SearchPlaylistGenre(playlistSongsSelected[index].playlistID)"
                                  @focus="SetPlaylistSearchGenres(playlistSongsSelected[index].playlistID)"
                                  placeholder="Enter Genre"
                                ></b-form-input>
                                <b-form-datalist
                                  v-if="readyToSort"
                                  id="options-list"
                                  v-bind:options="currentFocusedGenresSearch"
                                ></b-form-datalist>
                              </b-form-group>

                              <b-button
                                variant="primary"
                                size="sm"
                                @click="OnGenreSelect(playlist.playlistID)"
                              >Merge</b-button>
                            </b-dropdown-form>
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
import { BDropdown } from 'bootstrap-vue';

const spotify = new SpotifyWebApi();

interface playlist {
  name: string;
  id: string;
}

interface playlistSongs {
  playlistName: string;
  playlistID: string;
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

interface playlistGenres {
  playlistID: string;
  genres: artistGenres[];
}

interface artistGenres {
  artistName: string;
  artistId: string;
  genres: string[];
}

@Component({
  components: {}
})
export default class main extends Vue {
  private playlists: playlist[] = [];
  private playlistSongsSelected: playlistSongs[] = [];
  private selected: number[] = [];
  private selectedSongsForMerge: playlistItem[] = [];
  private playlistCount: number = 0;
  private showMerged: boolean = true;
  private playlistsLoaded: boolean = false;
  private showSongs: boolean = true;
  private userID: string = "";
  private dialog: boolean = false;
  private newPlaylistPublic: boolean = true;
  private newPlaylistCollaborative: boolean = false;
  private playlistGenresList: playlistGenres[] = [];
  private currentFocusedGenresSearch: string[] = [];
  private readyToSort: boolean = false;
  public created() {
    spotify.getMe().then(user => {
      this.userID = user.id;
    });
    this.LoadPlaylists();
  }

  public LoadPlaylists() {
    this.playlists = [];
    this.selected = [];
    this.playlistSongsSelected = [];
    this.playlistsLoaded = false;
    this.playlistCount = 0;
    spotify.getUserPlaylists().then(
      response => {
        response.items.forEach(playlist => {
          const playlist1: playlist = {
            name: playlist.name,
            id: playlist.id
          };
          this.playlists.push(playlist1);
          // this.OpenPlayList(playlist1);
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

  public OpenPlayLists() {
    const promiseArray: any = [];
    this.playlists.forEach(playlist => {
      const promise = spotify.getPlaylist(playlist.id);
      promiseArray.push(promise);
    });
    Promise.all(promiseArray).then(playlists => {
      playlists.forEach(playlist => {
        this.ParsePlaylist(playlist);
      });
    }).then(() => (this.playlistsLoaded = true));
  }

  public OpenPlayList(aplayList: playlist) {
    spotify.getPlaylist(aplayList.id).then(response => {
      this.ParsePlaylist(response);
    });
  }

  public ParsePlaylist(playlist: any) {
    const playlistIndex: number = this.playlistSongsSelected
      .map(x => x.playlistID)
      .indexOf(playlist.id);
    if (
      this.playlistSongsSelected.map(x => x.playlistID).includes(playlist.id)
    ) {
      this.playlistSongsSelected.splice(playlistIndex, 1);
    } else {
      const totalPlayListSongs: number = playlist.tracks.total;
      const playlistItems1: playlistItem[] = [];

      const numberCalls = Math.ceil(totalPlayListSongs / 100);
      const promiseArray = [];
      let offset = 0;
      for (let i = 0; i < numberCalls; ++i) {
        const promise = spotify.getPlaylistTracks(playlist.id, {
          limit: 100,
          offset
        });
        promiseArray.push(promise);
        offset += 100;
      }
      const artistIds: string[] = [];
      let numberSongs = 0;
      Promise.all(promiseArray)
        .then(setOfTracks => {
          setOfTracks.forEach(set => {
            set.items.forEach(item => {
              let artistsTemp: string = "";
              let artists: string = "";
              item.track.artists.forEach(artist => {
                artistsTemp = artistsTemp + artist.name + ", ";
                if (artist.id != null && !artistIds.includes(artist.id)) {
                  artistIds.push(artist.id);
                }
              });
              if (artistsTemp.length > 0) {
                artists = artistsTemp.substring(0, artistsTemp.length - 2);
              }
              const playlistItem1: playlistItem = {
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
        }).then(() => this.GetArtistGenres(artistIds, playlist.id));

      const playlistSongs1: playlistSongs = {
        playlistName: playlist.name,
        playlistID: playlist.id,
        songs: playlistItems1,
        numberSongs
      };
      this.playlistSongsSelected.push(playlistSongs1);
    }
  }

  public SearchPlaylistGenre(playlistID: string) {
    if (this.readyToSort == false) {
      this.SetPlaylistSearchGenres(playlistID);
    }
    this.readyToSort = true;
  }

  public SetPlaylistSearchGenres(playlistID: string) {
    this.currentFocusedGenresSearch = [];
    console.log(playlistID);
    //let playlistGenreIndex = this.playlistGenresList.findIndex(x => x.playlistID == playlistID);
    let playlistGenres = this.playlistGenresList[this.playlistGenresList.findIndex(x => x.playlistID == playlistID)];
    playlistGenres.genres.forEach((genres: artistGenres) => {
      genres.genres.forEach((genre: string) => {
        if (!this.currentFocusedGenresSearch.includes(genre)) {
          this.currentFocusedGenresSearch.push(genre);
        }
      })
    });
  }

  public OnGenreSelect(playlistID: string) {
    /*const dropdown = this.$refs.dropdown as BDropdown;
    dropdown.hide(true);*/

    const selectedGenre = (document.getElementById(playlistID) as HTMLInputElement).value;
    let playlistGenres: playlistGenres = this.playlistGenresList[this.playlistGenresList.findIndex(x => x.playlistID == playlistID)];
    let playlistSongs: playlistItem[] = this.playlistSongsSelected[this.playlistSongsSelected.findIndex(x => x.playlistID == playlistID)].songs;
    let artistsContainingGenre: string[] = [];

    playlistGenres.genres.forEach((genres: artistGenres) => {
      genres.genres.forEach((genre: string) => {
        if (genre == selectedGenre) {
          artistsContainingGenre.push(genres.artistName);
        }
      })
    });
    console.log(artistsContainingGenre);

    playlistSongs.forEach((song) => {
      artistsContainingGenre.forEach(artist => {
        if (song.artist.includes(artist)) {
          //console.log(song);
          if (!this.selectedSongsForMerge.map(x => x.songId).includes(song.songId)) {
            this.selectedSongsForMerge.push(song);
          }
        }
      });
    });

  }

  public GetArtistGenres(artistIds: string[], playlistId: string) {
    const numberIds = Math.ceil(artistIds.length);
    const numberCalls = numberIds / 50;
    const promiseArray = [];
    let offset = 0;
    for (let i = 0; i < numberCalls; ++i) {
      const partitionedArtistIds = artistIds.slice(offset, offset + 50);
      offset += 50;
      const promise = spotify.getArtists(partitionedArtistIds);
      promiseArray.push(promise);
    }
    let genres: string[] = [];
    const artistGenres1: artistGenres[] = [];
    Promise.all(promiseArray).then(setOfArtistResponses => {
      setOfArtistResponses.forEach(artistsResponse => {
        artistsResponse.artists.forEach(artist => {
          genres = [];
          artist.genres.forEach(genre => {
            genres.push(genre);
          });
          const artistGenre1: artistGenres = {
            artistName: artist.name,
            artistId: artist.id,
            genres: genres
          };
          artistGenres1.push(artistGenre1);
        });
      });
    }).then(() => this.SetPlaylistGenres(artistGenres1, playlistId));
  }

  public SetPlaylistGenres(artistGenres: artistGenres[], playlistId: string) {
    const playlistGenres1: playlistGenres = {
      playlistID: playlistId,
      genres: artistGenres
    };
    this.playlistGenresList.push(playlistGenres1);
    console.log(this.playlistGenresList);
  }

  public SortTop(numberItems: number) {
    this.selectedSongsForMerge = [];
    spotify.getMyTopTracks({ limit: numberItems }).then(topSongs => {
      const topSongsArray = topSongs.items.sort(function (a, b) {
        return b.popularity - a.popularity;
      });

      this.playlistSongsSelected.forEach(playlist => {
        playlist.songs.forEach(song => {
          if (
            topSongsArray.map(x => x.id).includes(song.songId) ||
            topSongsArray.map(x => x.name).includes(song.song)
          ) {
            if (!this.selectedSongsForMerge.map(x => x.songId).includes(song.songId)
            ) {
              this.selectedSongsForMerge.push(song);
              song.highlight = true;
            }
          }
        });
      });
    });
  }

  public CreateMergedPlaylist() {
    this.dialog = false;
    const newPlaylistName = (document.getElementById("nameField") as HTMLInputElement).value;
    const newPlaylistDescription = (document.getElementById("descriptionField") as HTMLInputElement).value;
    spotify.createPlaylist(this.userID, {
      name: newPlaylistName,
      description: newPlaylistDescription,
      public: this.newPlaylistPublic,
      collaborative: this.newPlaylistCollaborative
    }).then(createResponse => {
      console.log(createResponse);
      const newPlaylistId = createResponse.id;
      const songsToAdd = this.selectedSongsForMerge.map(x => x.uri);
      spotify.addTracksToPlaylist(newPlaylistId, songsToAdd).then(addSongsResponse => {
        console.log(addSongsResponse);
        this.LoadPlaylists();
      });
    });
  }

  public SortIndividualTop(numberItems: number, playlist: playlistSongs) { }

  public UndoLastMerge() {

  }

  public ShowOrHide() {
    if (this.showMerged === true) {
      this.showMerged = false;
    } else {
      this.showMerged = true;
    }
  }

  public ShowOrHideSongs() {
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