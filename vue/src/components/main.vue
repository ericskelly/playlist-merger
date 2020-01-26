<template>
	<div>
		<link href="https://fonts.googleapis.com/css?family=Material+Icons" rel="stylesheet" />
		<link
			href="https://cdn.jsdelivr.net/npm/@mdi/font@4.x/css/materialdesignicons.min.css"
			rel="stylesheet"
		/>
		<nav class="topNav navbar navbar-inverse navbar-fixed-top header">
			<a class="navbar-brand" style="color: #1DB954">Spotify Playlist Merger</a>
			<form class="form-inline" style="margin: 0 auto">
				<input
					class="form-control mr-sm-2"
					style="width: 30vw"
					type="search"
					placeholder="Search Playlists"
					aria-label="Search"
					v-model="playlistSearchText"
				/>
			</form>
		</nav>
		<div class="container-fluid">
			<div class="row">
				<v-card dark class="col sidenav" tile>
					<v-list rounded style="background-color">
						<v-subheader>
							Playlists
							<b-form-checkbox v-model="showSongs" switch style="margin-left: auto;">Songs</b-form-checkbox>
						</v-subheader>
						<v-list-item-group multiple v-model="selected" style="text-align: left">
							<v-list-item
								v-for="playlist in playlists"
								v-bind:key="playlist.id"
								@click="OpenPlayList(playlist)"
							>
								<template>
									<v-list-item-content>
										<v-list-item-title v-text="playlist.name"></v-list-item-title>
									</v-list-item-content>
								</template>
							</v-list-item>
						</v-list-item-group>
					</v-list>
				</v-card>
				<div class="col containerdiv">
					<div class="customcontainer" v-if="playlistsLoaded">
						<div class="globalMergeDiv">
							<v-col cols="12" style="height:100%">
								<v-row justify="center" style="height:100%">
									<v-col cols="3">
										<b-form-group label="Top Songs" label-for="dropdown-top-songs" style="color:white;">
											<b-form-select
												v-model="selectedTopSong"
												id="globalTopSongsNumber"
												size="sm"
												:options="numbersOneToFifty"
											></b-form-select>
										</b-form-group>
									</v-col>
									<v-col cols="3">
										<b-form-group
											label="Top Songs Time Range"
											label-for="dropdown-top-songs"
											style="color:white;"
										>
											<b-form-select
												:value="null"
												id="topSongsTimeRange"
												size="sm"
												:options="topSongsTimeRange"
												:disabled="selectedTopSong == null"
											></b-form-select>
										</b-form-group>
									</v-col>
									<v-col cols="3">
										<b-form-group label="Genre" label-for="dropdown-form-genre" style="color:white;">
											<b-form-input
												id="globalGenreSelect"
												list="genre-list"
												size="sm"
												placeholder="Enter Genre"
											></b-form-input>
											<b-form-datalist id="genre-list" v-bind:options="globalUniqueGenres"></b-form-datalist>
										</b-form-group>
									</v-col>
									<v-col cols="3" style="position:relative; height:100%">
										<button
											type="submit"
											class="btn btn-outline-success my-2 my-sm-0"
											style="position:absolute; bottom:0; right: 5%;"
											@click="PerformGlobalMerge()"
										>Merge</button>
									</v-col>
								</v-row>
							</v-col>
						</div>
						<v-row class="playlistsDiv">
							<v-col cols="3" v-if="selectedSongsForMergeStack.playlistSongsSelectDisplay.length > 0">
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

												<v-icon color="primary" dark @click="dialog = true">create</v-icon>

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
																		<v-checkbox v-model="newPlaylistPublic" label="Public Playlist?"></v-checkbox>
																	</v-col>
																	<v-col>
																		<v-checkbox v-model="newPlaylistCollaborative" label="Collaborative Playlist?"></v-checkbox>
																	</v-col>
																</v-row>
															</v-container>
															<small>*indicates required field</small>
														</v-card-text>
														<v-card-actions>
															<v-spacer></v-spacer>

															<v-btn color="green darken-1" text @click="dialog = false">Cancel</v-btn>

															<v-btn color="green darken-1" text @click="CreateMergedPlaylist()">Create</v-btn>
														</v-card-actions>
													</v-card>
												</v-dialog>
											</div>
										</div>
									</v-card-title>
									<v-card-subtitle style="float: right">
										<v-icon @click="UndoLastMerge()">undo</v-icon>
									</v-card-subtitle>
									<v-divider></v-divider>
									<v-list class="scrollStyle" max-height="500px">
										<v-list-item
											two-line
											v-for="songs in selectedSongsForMergeStack.playlistSongsSelectDisplay"
											v-bind:key="songs.uri"
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
								v-for="(playlist, index) in FilteredPlaylists()"
								v-bind:key="playlist.playlistID"
								v-bind:cols="3"
							>
								<v-card class="mx-auto" tile dark>
									<v-card-title>
										<div style="display: flex; justify-content: space-between; width: 100%">
											<v-chip outlined>
												{{
												playlist.playlistName
												}}
											</v-chip>
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
													<b-dropdown-header id="dropdown-header-label1">Popular Songs</b-dropdown-header>
													<b-dropdown-item @click="SortMostPopular(5, playlist)" style="min-width:250px">Top 5</b-dropdown-item>
													<b-dropdown-item @click="SortMostPopular(10,playlist)">Top 10</b-dropdown-item>
													<b-dropdown-item @click="SortMostPopular(50,playlist)">Top 50</b-dropdown-item>
													<b-dropdown-divider></b-dropdown-divider>
													<b-dropdown-form>
														<b-form-group label="Genre" label-for="dropdown-form-genre" @submit.stop.prevent>
															<b-form-input
																v-bind:id="playlist.playlistID"
																list="options-list"
																size="sm"
																@input="SearchPlaylistGenre(playlist.playlistID)"
																@focus="SetPlaylistSearchGenres(playlist.playlistID)"
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
											v-bind:key="songs.uri"
											v-bind:style="[songs.highlight? { color: '#008000' } : { color: '#000000' }]"
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
				</div>
			</div>
		</div>
	</div>
</template>

<script lang="ts">
import { Prop, Vue } from 'vue-property-decorator';
import Component from 'vue-class-component';
import SpotifyWebApi from 'spotify-web-api-js';
import axios from 'axios';
import router from '../router';
import { BDropdown } from 'bootstrap-vue';

declare var process: any;
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
	globalPopularity: number;
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

interface topSongsPerPlaylist {
	songFromPlaylist: playlistItem,
	popularity: number;
}

class selectedSongsForMergeHistoryStack {
	playlistSongsSelectDisplay: playlistItem[];
	playlistSongsSelectList: Array<playlistItem[]>;
	//isEmpty: boolean = this.playlistSongsSelectList.pop() == undefined;

	constructor() {
		this.playlistSongsSelectList = new Array<playlistItem[]>();
		this.playlistSongsSelectDisplay = [];
	}

	public IsEmpty() {
		return this.playlistSongsSelectList.length == undefined || this.playlistSongsSelectList.length == 0;
	}

	public PushPlaylistItem(playlistitem: playlistItem[]) {
		if (this.GetTopPlaylistItem() == undefined) {
			this.playlistSongsSelectList.push(playlistitem);
		} else {
			this.playlistSongsSelectList.push(this.GetTopPlaylistItem().concat(playlistitem));
		}
	}

	public GetTopPlaylistItem(): playlistItem[] {
		return this.playlistSongsSelectList[this.playlistSongsSelectList.length - 1];
	}

	public GetLength(): number {
		return this.playlistSongsSelectList.length;
	}

	public PopPlaylistItem() {
		this.playlistSongsSelectList.pop();
	}

}

//document.title = "Playlist Merger";

@Component({
	components: {}
})
export default class main extends Vue {
	private numbersOneToFifty: any[] = [{ value: null, text: '--Select a number--' }, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38,
		39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50];
	private selectedTopSong: any = null;
	private playlists: playlist[] = [];
	private playlistSongsSelected: playlistSongs[] = [];
	private selected: number[] = [];
	private playlistCount: number = 0;
	private showMerged: boolean = true;
	private playlistsLoaded: boolean = false;
	private showSongs: boolean = true;
	private userID: string = '';
	private dialog: boolean = false;
	private newPlaylistPublic: boolean = true;
	private newPlaylistCollaborative: boolean = false;
	private playlistGenresList: playlistGenres[] = [];
	private currentFocusedGenresSearch: string[] = [];
	private globalUniqueGenres: string[] = [];
	private readyToSort: boolean = false;
	private totalSongs: number = 0;
	private selectedSongsForMergeStack: selectedSongsForMergeHistoryStack = new selectedSongsForMergeHistoryStack();
	private playlistSearchText: string = '';
	private topSongsTimeRange: any[] = [{ value: null, text: '--Select Top Songs & Range--' }, { value: 'long_term', text: 'Long Term (several years)' },
	{ value: 'medium_term', text: 'Medium Term (last 6 months)' }, { value: 'short_term', text: 'Short Term (last month)' }];
	public created() {
		document.title = router.currentRoute.meta.title;
		const URL: string = process.env.VUE_APP_FLASK_API_URL + 'getcachedtoken';
		let access_token_stored = sessionStorage.getItem('access_token');
		if (!access_token_stored) {
			axios.get(URL).then((response) => {
				access_token_stored = response.data.access_token;
				if (!access_token_stored) {
					router.push("/login");
				} else {
					sessionStorage.setItem('access_token', access_token_stored);
					this.SetAccessAndLoadData(access_token_stored);
				}
			});
		} else {
			this.SetAccessAndLoadData(access_token_stored);
		}
	}

	public SetAccessAndLoadData(access_token: string) {
		spotify.setAccessToken(access_token);
		spotify.getMe().then(user => {
			this.userID = user.id;
			this.LoadPlaylists();
		},
			function (err) {
				if (err.status == "401") {
					sessionStorage.removeItem('access_token');
					router.push("/login");
				}
			});
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
					this.selected.push(this.playlistCount);
					this.playlistCount += 1;
				});
			},
			function (err) {
				if (err.status == "401") {
					sessionStorage.removeItem('access_token');
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
				this.ParsePlaylist(playlist, true);
			});
		}).then(() => (this.playlistsLoaded = true));
	}

	public OpenPlayList(aplayList: playlist) {
		spotify.getPlaylist(aplayList.id).then(response => {
			this.ParsePlaylist(response, false);
		});
	}

	public ParsePlaylist(playlist: any, countNumbers: boolean) {
		const playlistIndex: number = this.playlistSongsSelected
			.map(x => x.playlistID)
			.indexOf(playlist.id);
		if (this.playlistSongsSelected.map(x => x.playlistID).includes(playlist.id)) {
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
					offset: offset
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
								globalPopularity: item.track.popularity,
								uri: item.track.uri,
								highlight: false
							};
							playlistItems1.push(playlistItem1);
							numberSongs += 1;
						});
					});
					const playlistSongs1: playlistSongs = {
						playlistName: playlist.name,
						playlistID: playlist.id,
						songs: playlistItems1,
						numberSongs: numberSongs
					};
					this.playlistSongsSelected.push(playlistSongs1);
				}).then(() => this.GetArtistGenres(artistIds, playlist.id));
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

		let songsMerged: playlistItem[] = [];
		playlistSongs.forEach((song) => {
			artistsContainingGenre.forEach(artist => {
				if (song.artist.includes(artist)) {
					if (!this.selectedSongsForMergeStack.playlistSongsSelectDisplay.map(x => x.songId).includes(song.songId)) {
						this.selectedSongsForMergeStack.playlistSongsSelectDisplay.push(song);
						songsMerged.push(song);
					}
				}
			});
		});

		this.AddToMergedHistory(songsMerged);
	}

	public GetArtistGenres(artistIds: string[], playlistId: string) {
		const numberIds = Math.ceil(artistIds.length);
		const numberCalls = numberIds / 50;
		let promiseArray = [];
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
		artistGenres.forEach(artistGenres => {
			artistGenres.genres.forEach(genre => {
				if (!this.globalUniqueGenres.includes(genre)) {
					this.globalUniqueGenres.push(genre);
				}
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
			const newPlaylistId = createResponse.id;
			const songsToAdd = this.selectedSongsForMergeStack.playlistSongsSelectDisplay.map(x => x.uri);
			spotify.addTracksToPlaylist(newPlaylistId, songsToAdd).then(addSongsResponse => {
				this.selectedSongsForMergeStack.playlistSongsSelectDisplay = [];
				this.LoadPlaylists();
			});
		});
	}

	public CreateArtistsStringList(artists: SpotifyApi.ArtistObjectSimplified[]): string {
		let artistsReturn: string = '';
		let artistsTemp: string = '';
		artists.forEach(artist => {
			artistsTemp = artistsTemp + artist.name + ", ";
		});
		if (artistsTemp.length > 0) {
			artistsReturn = artistsTemp.substring(0, artistsTemp.length - 2);
		}

		return artistsReturn;
	}

	public async GetGlobalTop(numberItems: number, timeRange: string): Promise<playlistItem[]> {
		let playlistItemPromise: playlistItem[] = [];
		var topSongs: SpotifyApi.UsersTopTracksResponse;
		if (timeRange) {
			topSongs = await spotify.getMyTopTracks({ limit: numberItems, time_range: timeRange });
		} else {
			topSongs = await spotify.getMyTopTracks({ limit: numberItems });
		}
		topSongs.items.forEach(topSong => {
			let artists = this.CreateArtistsStringList(topSong.artists);
			const playlistItem: playlistItem = {
				songId: topSong.id,
				song: topSong.name,
				uri: topSong.uri,
				artist: artists,
				globalPopularity: topSong.popularity,
				highlight: false
			}
			playlistItemPromise.push(playlistItem);
		});

		return playlistItemPromise;
	}


	public SortMostPopular(numberItems: number, playlist: playlistSongs) {
		let playlistSongs: playlistItem[] = Object.create(playlist.songs);
		let mostPopularOrdered: playlistItem[] = playlistSongs.sort(function (a: playlistItem, b: playlistItem) { return b.globalPopularity - a.globalPopularity });
		let songsMerged: playlistItem[] = [];
		const loopCount = playlistSongs.length > numberItems ? numberItems : playlistSongs.length;
		for (let i = 0; i < loopCount; ++i) {
			if (!this.selectedSongsForMergeStack.playlistSongsSelectDisplay.map(x => x.songId).includes(mostPopularOrdered[i].songId)) {
				this.selectedSongsForMergeStack.playlistSongsSelectDisplay.push(mostPopularOrdered[i]);
				songsMerged.push(mostPopularOrdered[i]);
				mostPopularOrdered[i].highlight = true;
			}
		}
		this.AddToMergedHistory(songsMerged);
	}

	public AddToMergedHistory(songsMerged: playlistItem[]) {
		if (songsMerged.length != 0) {
			if (this.selectedSongsForMergeStack.GetLength() == 0) {
				this.selectedSongsForMergeStack.PushPlaylistItem(songsMerged);
			} else if (this.selectedSongsForMergeStack.GetTopPlaylistItem().length != undefined) {
				if (this.selectedSongsForMergeStack.playlistSongsSelectDisplay.length > this.selectedSongsForMergeStack.GetTopPlaylistItem().length) {

					this.selectedSongsForMergeStack.PushPlaylistItem(songsMerged);
				}
			}
		}
	}

	public async PerformGlobalMerge() {
		const globalTopSongsNumber: number = Number((document.getElementById("globalTopSongsNumber") as HTMLInputElement).value);
		const topSongsRange: string = String((document.getElementById("topSongsTimeRange") as HTMLInputElement).value);
		const globalGenre: string = (document.getElementById("globalGenreSelect") as HTMLInputElement).value;

		let artistsContainingGenre: string[] = [];

		let fromAll: any = new Object();

		if (globalGenre) {
			this.playlistGenresList.forEach(playlist => {
				playlist.genres.forEach((genres: artistGenres) => {
					genres.genres.forEach((genre: string) => {
						if (genre == globalGenre) {
							artistsContainingGenre.push(genres.artistName);
						}
					});
				});
			});

			this.playlistSongsSelected.forEach(playlist => {
				playlist.songs.forEach((song) => {
					artistsContainingGenre.forEach(artist => {
						if (song.artist.includes(artist)) {
							//fromGenre[song.uri] = song;
							fromAll[song.uri] = song;
						}
					})
				});
			});
		}

		if (globalTopSongsNumber) {
			let fromAllTemp: any = new Object();
			let topSongsPlaylist: playlistItem[] = await this.GetGlobalTop(globalTopSongsNumber, topSongsRange);
			topSongsPlaylist.forEach(song => {
				const songUri: string = song.uri;
				const inMergedValue = fromAll[songUri];
				if (inMergedValue || globalGenre == '') {
					fromAllTemp[song.uri] = song;
				}
			});
			fromAll = fromAllTemp;
		}

		let songsMerged: playlistItem[] = [];
		let songUris: string[] = Object.keys(fromAll);
		songUris.forEach(songUri => {
			if (!this.selectedSongsForMergeStack.playlistSongsSelectDisplay.map(x => x.uri).includes(songUri)) {
				let playlistItem: playlistItem = fromAll[songUri];
				if (playlistItem) {
					this.selectedSongsForMergeStack.playlistSongsSelectDisplay.push(playlistItem);
					songsMerged.push(playlistItem);
				}
			}
		});


		//TODO: Maybe make this a better popup dialog
		if (songsMerged.length == 0) {
			alert("No Songs Matched the Merge Criteria");
		}

		this.AddToMergedHistory(songsMerged);
	}

	public UndoLastMerge() {
		if (!this.selectedSongsForMergeStack.IsEmpty()) {
			const length: number = this.selectedSongsForMergeStack.GetLength();
			if (length < 2) {
				this.selectedSongsForMergeStack.playlistSongsSelectDisplay = [];
			} else {
				this.selectedSongsForMergeStack.PopPlaylistItem();

				this.selectedSongsForMergeStack.playlistSongsSelectDisplay = this.selectedSongsForMergeStack.GetTopPlaylistItem();
			}
		} else {
			this.selectedSongsForMergeStack.playlistSongsSelectDisplay = [];
		}
	}

	public FilteredPlaylists(): playlistSongs[] {
		return this.playlistSongsSelected.filter(playlist => {
			return playlist.playlistName.toLowerCase().includes(this.playlistSearchText.toLowerCase());
		})
	}
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.topNav {
	position: fixed;
	width: 100%;
	z-index: 2;
}

.sidenav {
	height: 100%;
	position: fixed;
	top: 55px;
	overflow-y: auto;
	width: 300px;
}

.containerdiv {
	background-color: #353535;
	min-height: 100vh;
	height: auto;
	margin-left: 300px;
	margin-top: 55px;
}

.customcontainer {
	width: 100%;
	padding-right: 15px;
	padding-left: 15px;
	padding: 12px;
	margin-right: auto;
	margin-left: auto;
	max-width: 1200px;
}

.globalMergeDiv {
	border: 1px solid #1db954;
	height: 100px;
}

@media screen and (max-width: 1330px) {
	.containerdiv {
		background-color: #353535;
		min-height: 100vh;
		height: auto;
		margin-left: 300px;
		padding-right: 300px;
		margin-top: 55px;
	}
}

@media screen and (min-width: 801px) and (max-width: 1200px) {
	.playlistsDiv .col-3 {
		min-width: 50%;
	}

	.globalMergeDiv .col-3 {
		min-width: 50%;
	}

	.globalMergeDiv {
		height: auto;
	}
}

@media screen and (max-width: 800px) {
	.playlistsDiv .col-3 {
		min-width: 100%;
	}

	.globalMergeDiv .col-3 {
		min-width: 100%;
	}

	.globalMergeDiv {
		height: auto;
	}
}

@media screen and (max-width: 600px) {
	.sidenav {
		height: 200px;
		overflow-y: auto;
		top: 55px;
		width: 100%;
		font-size: small;
	}

	.containerdiv {
		background-color: #353535;
		min-height: 100vh;
		height: auto;
		margin-left: 0;
		padding: 0;
		margin-top: 255px;
	}
}

@media screen and (max-width: 380px) {
	.globalMergeDiv {
		height: auto;
	}

	.globalMergeDiv .col-3 {
		min-width: 100%;
	}

	.sidenav {
		display: none;
	}

	.containerdiv {
		margin-top: 55px;
		padding: 0.5em;
	}
}

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

.sidenav li:active {
	color: #f1f1f1;
}

.header {
	background-color: #282828;
}

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
		border-top: 1px solid #181818;
	}
}
</style>