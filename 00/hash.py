import argparse
import json
import os

import cv2
import imagehash
from PIL import Image
from tqdm import tqdm


def find_duplicate_images(video_path):
    cap = cv2.VideoCapture(video_path)

    frame_hashes = {}
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    for index in tqdm(range(total_frames), desc="Processing Frames"):
        ret, frame = cap.read()
        if not ret:
            continue # skip if fail to read

        # find hash
        image = Image.fromarray(frame)
        frame_hash = str(imagehash.average_hash(image))

        # store hash
        if frame_hash in frame_hashes:
            frame_hashes[frame_hash].append(index)
        else:
            frame_hashes.update({frame_hash:[index]})

    cap.release()
    return frame_hashes

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script to compute the imagehash of each frame in the video")
    parser.add_argument("-o", "--output",help="name of the output json",default="hash.json", type=str)
    parser.add_argument("input", metavar= "INPUT_FILE", type=str)
    args = parser.parse_args()

    if not os.path.isfile(args.input):
        print(f"{args.input} does not exist, or not a file")
        exit()

    if os.path.exists(args.output):
        print(f"{args.output} already exist, try remove the old file")
        exit()

    duplicate_indices = find_duplicate_images(args.input)

    with open(args.output, 'w') as f:
        json.dump(duplicate_indices, f)
