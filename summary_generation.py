import moviepy.editor as mp

video = mp.VideoFileClip('path_to_video')

# Extract and combine key segments
key_segments = []
for label, periods in clusters.items():
    for period in periods:
        start_time = period / video.fps
        end_time = (period + 1) / video.fps  # Adjust the window as necessary
        key_segments.append(video.subclip(start_time, end_time))

# Concatenate the key segments
synopsis = mp.concatenate_videoclips(key_segments)
synopsis.write_videofile('video_synopsis.mp4')
