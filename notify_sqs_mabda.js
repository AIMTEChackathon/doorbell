'use strict';

console.log('Loading function');

const doc = require('dynamodb-doc');

const dynamo = new doc.DynamoDB();

// Load the SDK for JavaScript
var AWS = require('aws-sdk');
// Set the region 
AWS.config.update({region: 'eu-west-1'});

var sqs = new AWS.SQS({region: 'eu-west-1'});


/**
 * Demonstrates a simple HTTP endpoint using API Gateway. You have full
 * access to the request and response payload, including headers and
 * status code.
 *
 * To scan a DynamoDB table, make a GET request with the TableName as a
 * query string parameter. To put, update, or delete an item, make a POST,
 * PUT, or DELETE request respectively, passing in the payload to the
 * DynamoDB API as a JSON body.
 */
exports.handler = (event, context, callback) => {
    //console.log('Received event:', JSON.stringify(event, null, 2));
    
    if (event.challenge == null) {
        console.log('Received event event.challenge=null');
        done(new Error('Received event event.challenge=null'));
        return
    }

    const done = (err, res) => callback(null, {
        statusCode: err ? '400' : '200',
        body: err ? err.message : event.challenge,
        headers: {
            'Content-Type': 'text/plain',
        },
    });

    var params = {
  MessageBody: JSON.stringify({Challenge: event.challenge}), /* requred */
  QueueUrl: 'https://sqs.eu-west-1.amazonaws.com/233680902524/sqsDoorbell.fifo', /* required */
  DelaySeconds: 0,
  MessageGroupId: 'test',
  MessageDeduplicationId: (new Date()).getTime().toString()
};
sqs.sendMessage(params, done);

 // done(new Error(`Unsupported method "${event.httpMethod}"`));
};
