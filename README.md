Changes in this fork:
- Added progress bar via tqdm
- Changed working threads from 32 to as many CPU threads as the user's PC has.
- Cleaned some text so it works in a cleaner way.

To do:
+ Add audio and possibly worble it via FFMPEG.
+ Check viability of GPU processing via OpenCL

Original Description:
--------------------------------------------------------------------------------------------------
# Content Aware Scale
A alternative to using a photoshop script to do content aware scale using python seam carving.

Before & After
![alt text](https://github.com/X8J/py-content-aware-scale/blob/main/before%20and%20after.png?raw=true)

# What is content aware scale?
"Content Aware Scaling was first introduced in Photoshop CS4 and is used to resize an image while preserving the proportions of important image elements. Normal scaling affects all pixels uniformly when resizing an image but content aware scale attempts to only alter pixels that have little visual content"

This script allows content aware scale to be applied frame by frame over a video, without a need for photoshop.

To add
+ Loading bar
+ Optimize
+ UI or integration to After Effects

# Usage 

python content_aware_scale.py input_video.mp4 output_scaled_video.mp4 --scale_x 0.5 --scale_y 0.5
--------------------------------------------------------------------------------------------------

