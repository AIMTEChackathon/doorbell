#!/usr/bin/env python3

from datetime import date
import time
import urllib.request
import json
import hashlib
import aiy.audio

URL = 'https://services.speechtech.cz/tts/v3'
CHARSET = 'utf-8'

# init some shit
cp = urllib.request.HTTPCookieProcessor()
opener = urllib.request.build_opener(cp)
opener_valid = 0

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

    data_tts = json.dumps({'text': text, 'engine': engine, 'format' : 'wav'}).encode(CHARSET)
    wavdata = opener.open(URL+'/synth', data=data_tts).read()
    return wavdata

def main():
    d = date.today()
    text = 'Dnes je {0}.'.format(d.strftime("%A %d. %B %Y"))
    engine = 'Jan210'
    username = 'aimtechackathon'
    password = 'yojnecEct1'
    
    print('Hello')
    wavdata = tts_synth(username, password, text, engine)
    
    with open('test.wav', 'wb') as f:
        f.write(wavdata)
    
    print('playing greeting')
    aiy.audio.play_audio(wavdata)

if __name__ == '__main__':
    main()
