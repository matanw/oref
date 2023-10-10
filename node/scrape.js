//nodejs get html of https://www.oref.org.il/
const https = require('https');
const cheerio = require('cheerio');

async function getHtmlByUrlAndSelector( url, selector ) {
    let options = {
        headers: {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    };
    let html = await new Promise((resolve, reject) => {
        https.get(url, options, (res) => {
            let data = '';
            res.on('data', (chunk) => {
                data += chunk;
            });
            res.on('end', () => resolve(data));
            res.on('error', reject);
        });
    });
    //get html by selector
    const $ = cheerio.load(html);
    const htmlBySelector = $(selector).html();

    return htmlBySelector;
        
}


module.exports = {
    getHtmlByUrlAndSelector
};