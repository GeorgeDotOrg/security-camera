#!/usr/bin/env python3
#
# Copyright (c) 2020, NVIDIA CORPORATION. All rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
#

import sys
import argparse
#import struct
#import cv2

from tabulate import tabulate
from jetson_inference import detectNet
from jetson_utils import videoSource, videoOutput, Log

video_length = int(input("Please enter footage duration (in seconds): "))
# parse the command line
parser = argparse.ArgumentParser(description="Locate objects in a live camera stream using an object detection DNN.", 
                                 formatter_class=argparse.RawTextHelpFormatter, 
                                 epilog=detectNet.Usage() + videoSource.Usage() + videoOutput.Usage() + Log.Usage())

parser.add_argument("input", type=str, default="", nargs='?', help="URI of the input stream")
parser.add_argument("output", type=str, default="", nargs='?', help="URI of the output stream")
parser.add_argument("--network", type=str, default="ssd-mobilenet-v2", help="pre-trained model to load (see below for options)")
parser.add_argument("--overlay", type=str, default="box,labels,conf", help="detection overlay flags (e.g. --overlay=box,labels,conf)\nvalid combinations are:  'box', 'labels', 'conf', 'none'")
parser.add_argument("--threshold", type=float, default=0.5, help="minimum detection threshold to use") 

try:
	args = parser.parse_known_args()[0]
except:
	print("")
	parser.print_help()
	sys.exit(0)

#video = cv2.VideoCapture("input/vid10.mp4")
#print(f'CHECK HERE {args.input}')
#frame_count = video.get(cv2.CAP_PROP_FRAME_COUNT)


# create video sources and outputs
input = videoSource(args.input, argv=sys.argv)
output = videoOutput(args.output, argv=sys.argv)
	
# load the object detection network
net = detectNet(args.network, sys.argv, args.threshold)

# note: to hard-code the paths to load a model, the following API can be used:
#
# net = detectNet(model="model/ssd-mobilenet.onnx", labels="model/labels.txt", 
#                 input_blob="input_0", output_cvg="scores", output_bbox="boxes", 
#                 threshold=args.threshold)

#video_length = int(input("Please enter video length: "))
#print(f'CHECK HERE {dir(input)}')

frame_num = 0
final_out = ""
people_in_frame = []
# process frames until EOS or the user exits
while True:
    
    # capture the next image
    try:
        img = input.Capture()
    except:
        break

    if img is None: # timeout
        continue
    
    # detect objects in the image (with overlay)
    detections = net.Detect(img, overlay=args.overlay)

    # print the detections
    print("detected {:d} objects in image".format(len(detections)))

    for detection in detections:
        final_out += str(net.GetClassDesc(detection.ClassID))
        print(detection)
    
    if 'person' in map(net.GetClassDesc, [d.ClassID for d in detections]):
        print(f'found person at {frame_num}')
        people_in_frame.append(int(frame_num))

    frame_num += 1
    if 'person' not in map(net.GetClassDesc, [d.ClassID for d in detections]):
        continue

    # render the image
    output.Render(img)

    # update the title bar
    output.SetStatus("{:s} | Network {:.0f} FPS".format(args.network, net.GetNetworkFPS()))
    print(net.GetNetworkFPS())

    # print out performance info
    net.PrintProfilerTimes()

    
    # exit on input/output EOS
    if not input.IsStreaming() or not output.IsStreaming():
        break

#print(f'total # of frames {frame_num}')
#print(f'frames with people {people_in_frame}')

new_log = [["Timestamp", "Object Detected"]]
previous_time = 0.0
for num in people_in_frame:
    time_stamp = round(num / frame_num * video_length, 1)
    if time_stamp - previous_time >= 1.0:
        new_log.append(["",""])
    #print(f'{time_stamp}s - People Detected')
    new_log.append([f'{time_stamp}s', "Person(s) detected"])
    previous_time = time_stamp

if new_log[1] == ["",""]:
    new_log.remove(new_log[1])

print(f'\nDETECTION LOG\n')
print(tabulate(new_log, headers="firstrow"))
print(f'\nSee original footage at: {args.input}\nSee shortened footage at: {args.output}\n')

#video = cv2.VideoCapture(args.output)
#duration = video.get(cv2.CAP_PROP_FRAME_COUNT)
#print(f'CHECK HERE {duration}')
#print(f'CHECK HERE {args.input}')