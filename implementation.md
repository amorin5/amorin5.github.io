---
title: Implementation of Our Solution
layout: pagejs
permalink: "/implementation/"
customjs:
 - /assets/js/maps.js
comments: false
---
<!-- also include results and takeaways here? -->
Our implementation has three main portions. The first is the trained YOLOv5 [model](#model) that detects potholes out of images and videos. The second part is an additional layer of [functionality](#user-uploads) that allows users to upload their own photos and run the model over those. The third and final part is a [map](#pothole-mapping) of user submissions, plotting the location of potholes in an area using metadata from the user image. 
<br>

### Model
We decided to use a YOLO (You Only Look Once) model for object detection. We settled on this approach because the current research points to this being the most efficient for detection. To get started, we found a dataset of potholes in order to train our model. Using that dataset and other sources, we trained our model up to 1000 epochs. The best results were observed at epoch 373 and the model stopped training early at epoch 474 as improvements were not observed. After training the model, we generated performance metrics for the bounding box creation and the actual object detection. 

<!-- insert graph of metrics -->

We measured the both the training and validation loss for both bounding box creation and pothole detection. Loss represents how far away our model is from making accurate predictions. It can and should trend to zero and we were trying to minimize the loss in the given areas. Validation loss occurs at the end of an epoch by comparing the output to the validation dataset. Training loss occurs at the end of each step inside an epoch as the model is trying to improve the loss. Above, we can see that both training and validation loss are trending downward for pothole detection and bounding box generation, which is a good indicator that our model has high accuracy.  

We also measured mAP, the Mean Average Performance of the model. mAP is a formula that considers the confusion matrix, intersection over region, recall, and precision. A higher mAP indicates a higher performing ML model. In our case, these metrics aren't the best as our mAP is around 71%. However, this can be explained as a higher mAP can also indicate an over-fitting of data, and we optimized our model to reduce over-detection. 

The final two metrics were precision and recall.  


# INSERT PERFORMANCE METRICS AND MORE DETAILS ABOUT THE MODEL
# INSERT TABLES AND IMAGES OF BOUNDING BOXES


