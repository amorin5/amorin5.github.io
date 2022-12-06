---
title: Implementation of Our Solution
layout: pagejs
permalink: "/implementation/"
comments: false
---

Our implementation has three main portions. The first is the trained YOLOv5 [model](#model) that detects potholes out of images and videos. The second part is an additional layer of [functionality](#user-uploads) that allows users to upload their own photos and run the model over those. The third and final part is a [map](#pothole-mapping) of user submissions, plotting the location of potholes in an area using metadata from the user image.
<br>

### Model
We decided to use a YOLO (You Only Look Once) model for object detection. We settled on this approach because the current research points to this being the most efficient for detection. To get started, we found a dataset of potholes in order to train our model. Using that dataset and other sources, we trained our model up to...

# INSERT PERFORMANCE METRICS AND MORE DETAILS ABOUT THE MODEL
# INSERT TABLES AND IMAGES OF BOUNDING BOXES


