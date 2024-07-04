import cv2
import numpy as np
import sys
import os

def MovingAvg(source, output="bg.png", val=0.01, show_process=False, delay=0.0):

	max_frames = source.get(cv2.CAP_PROP_FRAME_COUNT)
	_,f = source.read()
	if f is None:
		print("No source input")
		return
	
	h, w = f.shape[:2]

	avg = np.float32(0.1*f)
	res = avg

	min_density = 1

	first_loop_flag = 1
	frame_count = 1

	while(1):
		_,f = source.read()
		if f is None:
			print("Source input over")
			break

		progress_bar(frame_count, end=max_frames)
		frame_count+=1

		avg = cv2.accumulateWeighted(f, avg, val)

		res_before = res
		res = cv2.convertScaleAbs(avg)

		if(not first_loop_flag):
			diff_array = cv2.absdiff(res_before, res)
			diff = np.sum(diff_array)
			diff_density = diff/(w*h)

			if(diff_density<min_density):
				min_density = diff_density
				if(show_process):
					cv2.imshow('bg_optimal', res)
				cv2.imwrite(output, res)				

		first_loop_flag = 0

		if(show_process):
			cv2.imshow('source', f)
			cv2.imshow('moving_average', res)

			k = cv2.waitKey(1)
			if k & 255 == 27:
				break
			elif k & 255 == 32:
				cv2.imshow('bg_snap', res)
				filename, file_ext = os.path.splitext(output)
				cv2.imwrite(filename + '_snap' + file_ext, res)				


		if(delay != 0.0):
			from time import sleep
			sleep(delay)
	print("Background image at " + output)

	if(show_process):
		cv2.destroyAllWindows()

def progress_bar(val, start=0, end=100, style='percent', fill='='):
	if(val>end):
		val = end
	elif (val<start):
		val = start

	percent = int(val*100/(end-start))
	
	if(style == 'bar'):
		sys.stdout.write("Progress: [")
		for i in range(50):
			if(i<percent/2):
				sys.stdout.write(fill)
			else:
				sys.stdout.write(" ")
		sys.stdout.write("]")

	else:
		sys.stdout.write("Progress: " + str(percent) + "%")
	
	sys.stdout.write("\r")
	


def GenerateBackground(video_path, output_dir="output", value=0.1, show_process=False, delay=0.0):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    filename, file_ext = os.path.splitext(os.path.basename(video_path))
    output = os.path.join(output_dir, filename + '_bg.png')

    print("Press SPACE to take a snap during process.")

    cam = cv2.VideoCapture(video_path)

    MovingAvg(cam, output=output, val=value, show_process=show_process, delay=delay)

    cam.release()

