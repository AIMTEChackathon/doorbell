#!/usr/bin/env python3

from datetime import date
from random import randint
import wave, struct
import time
import urllib.request
import urllib.parse
import json
import hashlib
import aiy.audio
import aiy.voicehat
import numpy as np
import scipy.io.wavfile
import os
import RPi.GPIO as GPIO
import boto3


# Storage
BUCKET = 'bucket-doorbell'
KEY = os.urandom(32)
s3 = boto3.client('s3')

URL = 'https://services.speechtech.cz/tts/v3'
URL_SLACK = 'https://slack.com/api/channels.history'

CHARSET = 'utf-8'
WAIT_FOR_INPUT = 28

# init some shit
cp = urllib.request.HTTPCookieProcessor()
opener = urllib.request.build_opener(cp)
opener_valid = 0

opener_slack = urllib.request.build_opener()

def auth_cookies(username, password):
    challenge = opener.open(URL+'/auth/challenge').read()
    challenge = json.loads(challenge.decode(CHARSET))
    
    ha1string = (username + ":" + challenge['realm'] + ":" + password).encode(CHARSET)
    ha1 = hashlib.md5(ha1string).hexdigest()
    
    digeststring = (ha1 + ':' + challenge['nonce']).encode(CHARSET)
    digest = hashlib.md5(digeststring).hexdigest()
    
    data = {'username': username, 'digest': digest}
    data = json.dumps(data).encode(CHARSET)
    
    auth = opener.open(URL+'/auth/response', data).read()
    auth = json.loads(auth.decode(CHARSET))
    opener_valid = int(auth['valid'])

def tts_synth(username, password, text, engine):
    current_timestamp = int(time.time())
    if current_timestamp > opener_valid:
        auth_cookies(username, password)
    
    arguments = {'text': text, 'engine': engine, 'format' : 'wav'}
    query = urllib.parse.urlencode(arguments)
    wavdata = opener.open(URL+'/synth'+'?'+query).read()
    return wavdata

def send_image(imageName):
    print("Uploading S3 object with SSE-C")
    image_file = open(imageName, 'rb')
    s3.put_object(Bucket=BUCKET, Key=imageName, Body=image_file)

def main():
    
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
    while True:
        slack_counter = 0
        input_state = GPIO.input(26)
        if input_state == False:
            print('Button Pressed')
            
            rate, data = scipy.io.wavfile.read('bell.wav')
            
            timestamp = time.time()
        
            print('playing greeting')
            aiy.audio.play_wave('bell.wav')
            
            imageName = "image" + str(randint(0, 1000000)) + ".jpg"
            
            os.system('raspistill -w 640 -h 480 -q 100 -o ' + imageName)
            send_image(imageName)
            os.system("./post.sh " + imageName)

            while slack_counter < WAIT_FOR_INPUT:
                arguments = {'token' : 'xoxp-325527629477-328538304838-327275090945-bd38ed29faa07f6c185b6f1fe00a6a04',
                             'channel' : 'C9ML7HDBL',
                             'count' : 1}
                query = urllib.parse.urlencode(arguments)                
                req = urllib.request.Request(url=URL_SLACK+'?'+query)
                req.add_header("Content-Type", "application/x-www-form-urlencoded;charset=utf-8")
                
                f = urllib.request.urlopen(req)
                messages = f.read().decode(CHARSET)
                messages_json = json.loads(messages)
                if (not 'bot_id' in messages_json['messages'][0]):
                    if (messages != None and len(messages_json['messages']) > 0 and float(messages_json['messages'][0]['ts']) > timestamp):
                        print('speaking: '+messages_json['messages'][0]['text'])
                        wavdata = tts_synth('aimtechackathon', 'yojnecEct1', messages_json['messages'][0]['text'], 'Iva210')
                        aiy.audio.play_audio(wavdata)
                        
                        slack_counter = WAIT_FOR_INPUT # funny

                time.sleep(1)
                slack_counter = slack_counter + 1


if __name__ == '__main__':
    main()

