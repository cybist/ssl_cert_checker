module.exports = {
  lintOnSave: false,
  publicPath: 'https://ssl-check.yourdomain.xyz/',
  devServer: {
    host: 'localhost',
    port: 8030,
    disableHostCheck: true,
    public: 'https://ssl-check.yourdomain.xyz/',
  }
}
