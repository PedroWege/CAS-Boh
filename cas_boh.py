"""
Changes from the original marked with #####
"""

import cv2
import numpy as np
import os
from seam_carving import resize
import time
from multiprocessing import Pool, cpu_count
import argparse
from tqdm import tqdm

def seam_carve(image, scale_x, scale_y):
    new_width = int(image.shape[1] * scale_x)
    new_height = int(image.shape[0] * scale_y)

    carved_image = resize(image, (new_height, new_width))
    if carved_image is None or carved_image.size == 0:
        print("Error: the carved image is empty or None.")
    
    return carved_image

def process_frame(frame, scale_x, scale_y):
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    carved_frame = seam_carve(frame_rgb, scale_x, scale_y)
    if carved_frame is None:
        return None
    return cv2.cvtColor(carved_frame, cv2.COLOR_RGB2BGR)

def process_video(input_path, output_path, scale_x=1.0, scale_y=1.0):
    if not os.path.exists(input_path):
        print(f"Error: video file {input_path} not found.")
        return

    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        print(f"Error: couldn't open the video file {input_path}")
        return

    fps = int(cap.get(cv2.CAP_PROP_FPS))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    ret, frame = cap.read()
    if not ret:
        print("Error: couldn't read the first frame of the video.")
        return

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    carved_frame = seam_carve(frame_rgb, scale_x, scale_y)
    wid = int(frame_rgb.shape[1])#####
    hei = int(frame_rgb.shape[0])#####
    new_width = round(wid * scale_x)#####
    new_height = round(hei * scale_y)#####
    print(f"\nOriginal frame size {wid}x{hei} - Total frames: {total_frames}")#####
    print(f"Resizing image to {new_width}x{new_height} ({scale_x*100:.1f}% width, {scale_y*100:.1f}% height)")#####

    if carved_frame is None:
        print("Warning: skipping video processing due to an error with the first frame.")
        return

    new_height, new_width, _ = carved_frame.shape
    #print(f"Processed frame dimensions: {new_width}x{new_height}")

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    if not os.path.isabs(output_path):
        output_path = os.path.join(os.getcwd(), output_path)

    out = cv2.VideoWriter(output_path, fourcc, fps, (new_width, new_height))
    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    batch_size = cpu_count()#####from 32 to cpu_count()
    print(f"Using {batch_size} CPU Threads.")#####    
    pbar = tqdm(total=total_frames)#####
    
    frame_buffer = []
    total_processed_frames = 0

    start_time = time.time()
    pool = Pool(cpu_count())

    while True:
        ret, frame = cap.read()
        if not ret:
            if frame_buffer:
                processed_frames = pool.starmap(process_frame, [(f, scale_x, scale_y) for f in frame_buffer])
                for processed_frame in processed_frames:
                    if processed_frame is not None:
                        out.write(processed_frame)
                        total_processed_frames += 1
            break

        frame_buffer.append(frame)
        if len(frame_buffer) >= batch_size:
            processed_frames = pool.starmap(process_frame, [(f, scale_x, scale_y) for f in frame_buffer])
            for processed_frame in processed_frames:
                if processed_frame is not None:
                    out.write(processed_frame)
                    total_processed_frames += 1
            frame_buffer = []
        pbar.update(1)#####

    pool.close()
    pool.join()
    cap.release()
    out.release()
    pbar.close()#####

    end_time = time.time()
    total_time = end_time - start_time
    average_fps = total_processed_frames / total_time if total_time > 0 else 0
    average_spf = total_time / total_processed_frames if total_processed_frames > 0 else 0
    print(f"Processing complete in {total_time:.2f} seconds. Average FPS: {average_fps:.2f}, Average SPF: {average_spf:.2f}")

def main():
    parser = argparse.ArgumentParser(description="Content-aware scaling using seam carving.")
    parser.add_argument('input_video', type=str, help='Path to the input video file')
    parser.add_argument('output_video', type=str, help='Path to save the scaled output video file')
    parser.add_argument('--scale_x', type=float, default=1.0, help='Scaling factor for width (default: 1.0)')
    parser.add_argument('--scale_y', type=float, default=1.0, help='Scaling factor for height (default: 1.0)')

    args = parser.parse_args()
    input_video = args.input_video
    output_video = args.output_video
    scale_x = args.scale_x
    scale_y = args.scale_y

    process_video(input_video, output_video, scale_x, scale_y)

if __name__ == "__main__":
    main()
