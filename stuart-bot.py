from flask import Flask
import datetime
import requests
import tweepy
import time
import sys
import cv2
import os

app = Flask(__name__)
    
CAM_URL = os.environ["CAM_URL"]
CONSUMER_KEY = os.environ['CONSUMER_KEY']
CONSUMER_SECRET = os.environ['CONSUMER_SECRET']
ACCESS_KEY = os.environ['ACCESS_KEY']
ACCESS_SECRET = os.environ['ACCESS_SECRET']

@app.route('/')
def home():
    searching_for_cat = True

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    api = tweepy.API(auth)

    while True:
        if searching_for_cat:
            try:
                take_snapshot("snapshot.jpg")
                image = cv2.imread("snapshot.jpg")
                rects = any_cats(image)

                if len(rects) > 0:
                    print('Cat Detected')
                    sys.stdout.flush()
                    api.update_with_media("snapshot.jpg")
                    searching_for_cat = False
                else:
                    print('No cat detected')
                    sys.stdout.flush()
            
            except requests.RequestException as e:
                print(f"Webcam inaccessible.")
                print(f"{e}")
                sys.stdout.flush()
            except Exception as e:
                print(f"{e}")
                sys.stdout.flush()
            
            time.sleep(5)
        else:
            time.sleep(60 * 50)
            searching_for_cat = True


def any_cats(image, classifier = "haarcascade_frontalcatface_extended.xml"):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
     
    detector = cv2.CascadeClassifier(classifier)
    rects = detector.detectMultiScale(gray, scaleFactor=1.01,
	    minNeighbors=2, minSize=(75, 75)) 
    
    return rects

def take_snapshot(filename, omega_url = f"http://{CAM_URL}/?action=snapshot"):
    r = requests.get(omega_url, stream=True)
    if r.status_code == 200:
        with open(filename, 'wb') as f:
            for chunk in r.iter_content():
                f.write(chunk)
    else:
        raise requests.RequestException()

if __name__ == '__main__':
    app.run(host= '0.0.0.0', port=os.environ.get('PORT'))