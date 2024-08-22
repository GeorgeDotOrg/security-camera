import sys
import argparse

from jetson_inference import detectNet
from jetson_utils import videoSource, videoOutput, Log

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

# process frames until EOS or the user exits
print("RUNNING GEORGE")
while True:
    # capture the next image
    img = input.Capture()

    if img is None: # timeout
        continue  
        
    # detect objects in the image (with overlay)
    detections = net.Detect(img, overlay=args.overlay)
    #detections2 = net.Detect(img)

    # print the detections
    #print("detected {:d} objects in image".format(len(detections)))

    #if output.IsStreaming():
    #    output.Close()
    #person_seen = True
    #for detection in detections2:
    #    class_name = net.GetClassDesc(detection.ClassID)
    #    print(f"Detected3 '{class_name}'")
        #if detection.ClassID == 1:
        #    person_seen = True
            #if not output.IsStreaming():
            #    output.Open()
        #    print("test1")
        #print(detection)
        #print("test")
        #class_idx, confidence = net.Classify(img)
        #class_desc = net.GetClassDesc(class_idx)
        #print("test" + class_desc)
    
    if 'person' not in map(net.GetClassDesc, [d.ClassID for d in detections]):
        continue

    # render the image
    #if person_seen:
    output.Render(img)
    
    #if not person_seen:
    #    output.Close()

    # update the title bar
    output.SetStatus("{:s} | Network {:.0f} FPS".format(args.network, net.GetNetworkFPS()))

    # print out performance info
    net.PrintProfilerTimes()

    #if not output.IsStreaming():
    #    output.Open()

    # exit on input/output EOS
    if not input.IsStreaming() or not output.IsStreaming():
        break