#!/bin/sh
echo $1
curl -X POST -H 'Authorization: Bearer xoxb-327950042709-6CvTY9U7eepQrTNrjUI46wJS' -H 'Content-type: application/json' --data '{"channel":"doorbell","attachments": [ { "title": "Někdo stojí u dveří!!!", "image_url": "https://s3-eu-west-1.amazonaws.com/bucket-doorbell/'$1'" } ]}' https://slack.com/api/chat.postMessage
