#!/usr/bin/python3

import jetson_inference
import jetson_utils
import argparse
from jetson_utils import detectNet

net = detectNet()

net.SetTrackingEnabled(True)
net.SetTrackingParams(minFrames=3, dropFrames=15, overlapThreshold=0.5)

detections = net.Detect(img)

for detection in detections:
    if detection.TrackStatus >= 0:  # actively tracking
        print(f"object {detection.TrackID} at ({detection.Left}, {detection.Top}) has been tracked for {detection.TrackFrames} frames")
    else:  # if tracking was lost, this object will be dropped the next frame
        print(f"object {detection.TrackID} has lost tracking")