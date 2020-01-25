module.exports = {
    productionSourceMap: false,
    configureWebpack: {
        "devtool": "source-map"
    },
    publicPath: process.env.ENVIRONMENT === 'production' ? '/playlist-merger/' : '/'
}