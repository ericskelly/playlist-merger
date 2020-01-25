module.exports = {
    productionSourceMap: false,
    configureWebpack: {
        "devtool": "source-map"
    },
    publicPath: process.env.ENVIRONMENT === 'production' ? '/spotify-playlist-merger/' : '/'
}