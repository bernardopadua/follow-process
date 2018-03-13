const path = require('path');

module.exports = {
  mode: 'development',
  entry: './src/index.js',
  output: {
    filename: 'index.bundled.js',
    path: path.resolve(__dirname, 'dist/assets/js/')
  },
  module: {
    rules: [
      { 
        test: /\.js$/, 
        exclude: /node_modules/, 
        loader: "babel-loader" 
      }
    ]
  },
  devServer: {
    contentBase: path.join(__dirname, "dist"),
    //compress: true,
    port: 9000,
    historyApiFallback: true
  }
};
