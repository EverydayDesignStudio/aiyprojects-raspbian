#!/usr/bin/env python3
# Copyright 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Trigger PiCamera when face is detected."""
import os,sys
from aiy.vision.inference import CameraInference
from aiy.vision.models import face_detection

from picamera import PiCamera
import time
from neopixel import *
import argparse
import strandtest
from aip import AipFace
from aip import AipImageClassify
import base64
""" 你的 APPID AK SK """
APP_ID = '16862435'
API_KEY = 'NK4Wq0YooPUYaiiWazXrKdPN'
SECRET_KEY = 'fSotIH8AKaZBHxmzirEeOfWh4c1jq7s1'
client = AipFace(APP_ID, API_KEY, SECRET_KEY)

def image2base64(filepath):
    with open(filepath,'rb') as f:
        base64_data=base64.b64encode(f.read())
    image64 =str(base64_data,'utf-8')
    return image64

def avg_joy_score(faces):
    if faces:
        return sum(face.joy_score for face in faces) / len(faces)
    return 0.0

def main():
    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    args = parser.parse_args()

     # Create NeoPixel object with appropriate configuration.
    strip = strandtest.strip
     # Intialize the library (must be called once before other functions).
    strandtest.colorWipe(strip, Color(0, 0, 0), 10)
    strip.show()
    i=0

    with PiCamera() as camera:
        # Configure camera
        camera.resolution = (1640, 922)  # Full Frame, 16:9 (Camera v2)
        camera.start_preview()
        while True:
            # Do inference on VisionBonnet
            with CameraInference(face_detection.model()) as inference:
                for result in inference.run():
                    faces = face_detection.get_faces(result)
                    if len(faces) >= 1:
                        print('who are you?')
                        camera.capture('face.jpg')
                        face64=image2base64('./face.jpg')
                        classify_result = client.search(face64, "BASE64", "EDS")
                        print(classify_result)
                        options = {}
                        options["face_field"] = "expression"
                        detect_result = client.detect(face64, "BASE64", options)
                        print(detect_result)
                        os.remove('./face.jpg')
                        '''
                        if detect_result.get('result').get('face_list')[0].get('expression').get('type') == 'none':
                            light=63
                        elif detect_result.get('result').get('face_list')[0].get('expression').get('type') == 'smile':
                            light=127
                        else:
                            light=255
                        '''
                        if classify_result.get('result'):
                            if classify_result.get('result').get('user_list')[0].get('user_id') == 'Ini':
                                print(int(255*avg_joy_score(faces)))
                                strip.setPixelColor(i, Color(int(255*avg_joy_score(faces)),0,0))
                            elif classify_result.get('result').get('user_list')[0].get('user_id') == 'Ana':
                                strip.setPixelColor(i, Color(0, int(255*avg_joy_score(faces)), 0))
                            elif classify_result.get('result').get('user_list')[0].get('user_id') == 'Henry':
                                strip.setPixelColor(i, Color(0,0,int(255 * avg_joy_score(faces))))
                            elif classify_result.get('result').get('user_list')[0].get('user_id') == 'Tol':
                                strip.setPixelColor(i, Color(0,int(255 * avg_joy_score(faces)),int(255 * avg_joy_score(faces))))
                            elif classify_result.get('result').get('user_list')[0].get('user_id') == 'Jordan':
                                strip.setPixelColor(i, Color(int(255 * avg_joy_score(faces)),0,int(255 * avg_joy_score(faces))))
                            elif classify_result.get('result').get('user_list')[0].get('user_id') == 'Min':
                                strip.setPixelColor(i, Color(int(255 * avg_joy_score(faces)),int(255 * avg_joy_score(faces)),0))
                            else:
                                strip.setPixelColor(i, Color(int(255 * avg_joy_score(faces)),int(255 * avg_joy_score(faces)),int(255 * avg_joy_score(faces))))
                            strip.show()
                            i = i + 1
                            if i >= 5:
                                i = 0
                                strandtest.rainbow(strip)
                                time.sleep(3)
                                strandtest.colorWipe(strip, Color(0, 0, 0), 10)
                            #time.sleep(1)
                        else:
                            pass
        # Stop preview
        #camera.stop_preview()


if __name__ == '__main__':
    main()
