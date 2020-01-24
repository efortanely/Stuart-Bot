from imageai.Detection import ObjectDetection
from dotenv import load_dotenv
import requests
import tweepy
import time
import sys
import cv2
import os

load_dotenv()

CAM_URL = os.getenv("CAM_URL")
CONSUMER_KEY = os.getenv('CONSUMER_KEY')
CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')
ACCESS_KEY = os.getenv('ACCESS_KEY')
ACCESS_SECRET = os.getenv('ACCESS_SECRET')

searching_for_cat = True
sec = 0

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

detector = ObjectDetection()
detector.setModelTypeAsRetinaNet()
detector.setModelPath("resnet50.h5")
detector.loadModel()

def any_cats(image):
    detections = detector.detectObjectsFromImage(input_image=image, output_image_path="imagenew.jpg")
    for d in detections:
        if d['name'] is "cat" and d['percentage_probability'] > 69:
            return True
    return False

def take_snapshot(filename, omega_url = f"http://{CAM_URL}/?action=snapshot"):
    r = requests.get(omega_url, stream=True)
    if r.status_code == 200:
        with open(filename, 'wb') as f:
            for chunk in r.iter_content():
                f.write(chunk)
    else:
        raise requests.RequestException()

while True:
    if searching_for_cat:
        try:
            take_snapshot("snapshot.jpg")
            is_cats = any_cats("snapshot.jpg")

            if is_cats:
                print('Cat Detected')
                api.update_with_media("snapshot.jpg")
                searching_for_cat = False
            else:
                print('No cat detected')
        
        except requests.RequestException as e:
            print(f"Webcam inaccessible.")
            print(f"{e}")
        except Exception as e:
            print(f"{e}")
        
        sec += 5
        time.sleep(5)
        if sec == 60 * 10:
            searching_for_cat = False
            sec = 0

    else:
        time.sleep(60 * 50)
        searching_for_cat = True