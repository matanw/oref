//read  config from json file
var config = require('./config.json');
var scrape = require('./scrape.js');
const fs = require('fs');
const { convert } = require('html-to-text');

const convertOptions = {
    wordwrap: 130,
    // ...
  };
//loop all json config, each entry set interval ny the interval value
//call scrape.getHtmlByUrlAndSelector and send the result to the a file in output folder
config.forEach(function (item) {
    setInterval(function () {
        scrape.getHtmlByUrlAndSelector(item.url, item.selector).then(function (data) {
            var fileName = item.fileName + '.html';
            data = convert(data, convertOptions);
            fs.writeFile('./output/' + fileName, data, function (err) {
                if (err) {
                    return console.log(err);
                }
                console.log('The file ' + fileName + ' was saved!');
            });
        });
    }, item.interval * 1000);
    console.log(item.fileName + ' interval set to ' + item.interval + ' seconds');
});