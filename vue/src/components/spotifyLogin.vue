<template>
	<div class="loginWrapper">
		<div class="centered">
			<p>Merge your spotify playlists based on account, song, and artist meta data</p>
			<a v-bind:href="URL">
				<img style="cursor: pointer;" src="../../Images/log_in-desktop-large.png" />
			</a>
		</div>
	</div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';
import axios from 'axios';
import SpotifyWebApi from 'spotify-web-api-js';
import router from '../router';
declare var process: any;

const spotify = new SpotifyWebApi();

@Component({
	components: {}
})
export default class SpotifyLogin extends Vue {
	private params: any;
	private URL: string = process.env.VUE_APP_FLASK_API_URL;
	private refreshToken: string = '';
	created() {
		document.title = router.currentRoute.meta.title;
		this.params = this.getHashParams();
		console.log(this.params);
		if (this.params.access_token) {
			spotify.setAccessToken(this.params.access_token);
			sessionStorage.setItem('access_token', this.params.access_token);
			router.push('/');
		}
		if (this.params.refresh_token) {
			this.refreshToken = this.params.refresh_token;
		}
	}

	getHashParams() {
		var hashParams = {} as any;
		var e, r = /([^&;=]+)=?([^&;]*)/g,
			q = window.location.hash.replace('#/login/', '').substring(1)
		while (e = r.exec(q)) {
			hashParams[e[1]] = decodeURIComponent(e[2]);
		}
		return hashParams;
	}

}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.center-screen {
	display: flex;
	flex-direction: column;
	justify-content: center;
	align-items: center;
	text-align: center;
}

.centered {
	display: flex;
	flex-direction: column;
	justify-content: center;
	align-items: center;
	text-align: center;
	position: fixed;
	top: 50%;
	left: 50%;
	/* bring your own prefixes */
	transform: translate(-50%, -50%);
}
</style>