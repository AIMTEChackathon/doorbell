'use strict';

const https = require('https');

/**
 * Pass the data to send as `event.data`, and the request options as
 * `event.options`. For more information see the HTTPS module documentation
 * at https://nodejs.org/api/https.html.
 *
 * Will succeed with the response body.
 */
exports.handler = (event, context, callback) => {
    
    const options = {
          hostname: 'https://slack.com/api/chat.postMessage',
          port: 443,
          path: '/',
          method: 'POST'
        };
    
    const req = https.request(options, (res) => {
        let body = {channel: "doorbell",text:"I hope the tour went well, Mr. Wonka.",attachments: [ { title: "The Further Adventures of Slackbot", image_url: "https://s3-eu-west-1.amazonaws.com/bucket-doorbell/obrazek" } ]};
        console.log('Status:', res.statusCode);
        console.log('Headers:', JSON.stringify(res.headers));
        res.setEncoding('utf8');
        res.on('data', (chunk) => body += chunk);
        res.on('end', () => {
            console.log('Successfully processed HTTPS response');
            // If we know it's JSON, parse it
            if (res.headers['content-type'] === 'application/json') {
                body = JSON.parse(body);
            }
            callback(null, body);
        });
    });
    req.on('error', callback);
    req.write(JSON.stringify(event.data));
    req.end();
};
