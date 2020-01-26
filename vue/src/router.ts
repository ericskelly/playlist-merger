import Vue from 'vue';
import Router from 'vue-router';
import spotifyLogin from './components/spotifyLogin.vue';
import main from './components/main.vue';

Vue.use(Router);

export default new Router({
  mode: 'hash',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'main',
      component: main,
      meta: { title: 'Playlist Merger' }
    },
    {
      path: '/login',
      name: 'spotifyLogin',
      component: spotifyLogin,
      meta: { title: 'Playlist Merger - Login' }
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (about.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import(/* webpackChunkName: "about" */ './views/About.vue'),
    },
  ],
});
