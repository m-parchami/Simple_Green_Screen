# Build your own Green Screen!

Hey there!
In this tutorial I will try to help you get familiar with background subtraction, and some morphological operations. Then to see the results in practice, we will build our own green screen ;). If you have already bought a green screen don't worry, it is really unlikely that this method with this level of simplicity will out perform your actual one. 


# What is Background Subtraction and why bother?

Background Subtraction has been attracting many Computer Vision scientists in the past years. In my opinion, it mainly consists of two steps. Measuring the background, that is knowing the value each pixel must have to construct the background image. The second step is to process the differences of a frame and the stored background image and get the good stuff. Imagine a security guard staring multiple monitors every second to find out whether there's a change in the scene (someone passing by etc.), however, with the help of background subtraction and some further processings, the guard can just wait for an alarm that indicates a change in the scene. This can even be used to reduce the amound of storage needed to keep the security tapes. The time periods that scene remains stable can be cut easily.

## Getting the background image

Depending on the situations and use cases, background measurement can be tricky. In an easy case, we assume that the scene itself is not changing at all. Not even in illumination. Therefore we can assume the pixel intensities will almost keep the same values over periods of time. But even with this, we can't be sure on what's the correct pixel value. The camera noise, no matter what restrictions you assume, are always there. Even with a fixed camera and a static scene, you can see the pixel values keep changing. This noise can harm our process in two ways. First, finding the right pixel value, and Second, deciding whether the change must be considered as new object.

### A Quick Solution!
One of the easiest solutions is to avoid constructing background from a single image. We can use a short sequence of frames (remember the security camera example) and conclude the background image in a more robust manner. Since the camera noise often has Normal Distribution, using median (or even averaging) in a sequence of values will eventually discard the noise. Therefore all we need to do is to store couple of frames, do pixel-wise median over the sequence, and valla, a much more clean background image will be smiling at you. This is also great when the background itself tends to change gradually. It will take just a couple of frames to have the updated version. 

### Enough talking, show me the code!

Alright let's see how easy it really is to get the background image with this trick. As I mentioned this method will require a few background frames to overcome the noise. So, we define a mode for capturing these background frames. We switch the modes with 'b' button.
```python
import cv2  
import numpy as np  
  
cap = cv2.VideoCapture(0) # If you have an additional webcam you may change this line
buffer = []  
mode = "capture"  
background = None
threshold = 70
while True:  
    ok, frame = cap.read()
    if not ok:
	    print("Capture Ended!")
	    break
	cv2.imshow("camera", frame)  
	key = cv2.waitKey(1) & 0xFF # You may change this line if you need a specific FPS
	if key == ord('b'): 
		if mode == "background":  # If it was taking background till now:
	    
	        # Compute background and go to capture mode  
			background = np.median(buffer, axis = 0)
			
			# In case you used other methods resulting in floating point pixels:
	        background = np.asarray(background, dtype = np.uint8)
	        
			# Background is done, go to the capture (normal) mode
	        mode = "capture"  
	  
	    else:  
	        # Free the buffer for new background computation
			buffer = []  
			
			# Switch the mode
	        mode = "background"
	        
	elif key == ord('q'): # Just for ending the cycle  
       	    break
``` 
Ok now we have the code to compute the background. Let's go through storing and showing the background frames.
```Python
	if mode == "background":  
	    buffer.append(frame)
	if background is not None: # We have a background computed  
		# This is just for you to check the computed background, comment these in later usages.
		cv2.imshow("background", background)  
		cv2.waitKey(1)
```
Ok now we have the background image. The next step is to subtract each frame from our background to get the green screen like output. 
First we compute absolute difference between two images( captured frame and previously computer background). Then, in order to remove differences caused by noise, we apply a threshold to this difference. Unfortunately, this will not be enough to fix all of the noises. To do so, we take advantage of already implemented morphological operations in OpenCV. Make sure you read the docs properly. I will try to add images of each operation in the future.
```Python

		sub_image = cv2.absdiff(frame, background)
                sub_image = np.sum(sub_image, axis=2)

		binary = np.zeros(sub_image.shape, dtype=np.uint8)  
		binary[sub_image > threshold] = 1
				
		kernel = np.ones((5, 5), np.uint8)  
		binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)  
		kernel = np.ones((17, 17), np.uint8)  
		binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
		
		masked_frame = frame.copy()  
		masked_frame[binary == 0] = 0  
		cv2.imshow("masked", masked_frame)  # This is the final output
		cv2.waitKey(1)
```

![Testing]("test.png")
