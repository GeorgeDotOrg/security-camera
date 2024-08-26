# Security Footage Helper

<p align="justify">This program aids viewing security footage by automatically detecting and logging times when people appear in the footage and creating a trimmed down video of when people appear in footage.</p>

## The Algorithm

<p align="justify">The algorithm can be run by entering a command in the terminal, with arguments consisting of the addresses of the input mp4 file and desired adress of the output mp4 file, and this information is then gathered with ArgumentParser. The project includes folders dedicated to storing input and output files used in this project. At runtime, the program asks the user how long the input video is in total seconds. Then, the algorithm uses the DetectNet model for continuously detecting people in frame throughout the inputted video. The algorithm uses that information to compile a list of frame numbers in which people appear. Additionally, the program uses continue to loop again before rendering a frame to the output video, if that frame does not have people in it, as a way to make an output video file only consisting of frames wherein people appear. After the input video is fully processed, the program iterates through the list of the recorded frame numbers and calculates timestamps by dividing the indivdual frame numbers by the total frames to find the percent of time into the video when the detection of people occurs, and multiplying that by the total video length, as specified by the user.</p>

## Running this project

1. Import the tabulate, jetson-inference, and jetson-utils libraries.
2. Download the project folder.
3. Place videos that you wish to process into the input folder.
4. Open terminal.
5. Enter "cd final-project" into terminal if necessary.
6. Enter "python3 final-project4.py input/***the filename (including .mp4) that you wish to process from. e.g. in-video1.mp*** output/***the filename (including .mp4) that you wish to render the trimmed footage to. e.g. out-video1.mp4***" into the terminal.
7. Enter the length of the video you wish to input (in seconds) when prompted.
- Length information available for test videos in input-desc.txt
8. Wait.
9. See detection log at end of terminal output.
10. See trimmed video in the output folder.

## Before

https://github.com/user-attachments/assets/fa2ec8c2-83cf-4450-a0fc-e20e8ab3288e

## After

https://github.com/user-attachments/assets/446432a1-6b8d-45e8-899f-f70f5daeaec4

### Detection Log
![3](https://github.com/user-attachments/assets/dc4b0750-44e7-41e9-83a4-561bec752ad1)
--->
![4](https://github.com/user-attachments/assets/c9bbc68d-8682-4e44-8f96-b756332dd942)

### Video Demonstration
https://drive.google.com/file/d/1uHULt2pA-cIGeiDij7CbWrl77H6EobEC/view?usp=sharing
