import cv2
from tqdm import tqdm

def get_frame(video_capture, start_frame):
    video_capture.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
    ret, frame = video_capture.read()
    if not ret:
        raise
    
    return frame

def create_clip(video_path, start_frame_index, end_frame_index, output_path):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Error: Could not open video file.")
        return

    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    fourcc = cv2.VideoWriter_fourcc(*"VP90")  # VP8 codec for WebM format
    video_writer = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame_index)
    for i in tqdm(range(start_frame_index, end_frame_index)):
        _, frame = cap.read()
        video_writer.write(frame)

    cap.release()
    video_writer.release()

def preview(video_path, start_idx, end_idx):
    video_capture = cv2.VideoCapture(video_path)
    start_frame = get_frame(video_capture, start_idx)
    end_frame = get_frame(video_capture, end_idx)
    # Display or use the closest frame as needed
    cv2.imshow('First Frame',start_frame)
    cv2.imshow('End Frame', end_frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def main():
    video_path = "./yorushika_radio.webm"
    start_idx = 3600
    end_idx = start_idx + 6250

    output_path = "./yorushika_radio.webp"

    # preview(video_path, start_idx, end_idx)
    create_clip(video_path, start_idx, end_idx-1, output_path)

if __name__ == "__main__":
    main()
