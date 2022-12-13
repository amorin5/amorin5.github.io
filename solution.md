---
title: Implementation and Results
layout: pagejs
permalink: "/solution/"
customjs:
 - /assets/js/maps.js
comments: false
---
<!-- also include results and takeaways here? -->
Our implementation has three main portions. The first is the trained YOLOv5 [model](#model) that detects potholes out of images and videos. The second part is an additional layer of [functionality](#user-uploads) that allows users to upload their own photos and run the model over those. The third and final part is a [map](#pothole-mapping) of user submissions, plotting the location of potholes in an area using metadata from the user image. 
<br>

### Model
We decided to use a YOLO (You Only Look Once) model for object detection. We settled on this approach because the current research points to this being the most efficient for detection. To get started, we found a dataset of potholes in order to train our model. We used a YOLO skeleton we found online and tweaked it for our use. The model was written and hosted on Google Collab for training. Using our dataset and other sources, we trained our model up to 1000 epochs. The best results were observed at epoch 373 and the model stopped training early at epoch 474 as improvements were not observed. After training the model, we generated performance metrics for the bounding box creation and the actual object detection. 

<!-- insert graph of metrics -->

We measured the both the training and validation loss for both bounding box creation and pothole detection. Loss represents how far away our model is from making accurate predictions. It can and should trend to zero and we were trying to minimize the loss in the given areas. Validation loss occurs at the end of an epoch by comparing the output to the validation dataset. Training loss occurs at the end of each step inside an epoch as the model is trying to improve the loss. Above, we can see that both training and validation loss are trending downward for pothole detection and bounding box generation, which is a good indicator that our model has high accuracy.  

![Performance Metrics](assets/img/metrics.jpg)

We also measured mAP, the Mean Average Performance of the model. mAP is a formula that considers the confusion matrix, intersection over region, recall, and precision. A higher mAP indicates a higher performing ML model. In our case, these metrics aren't the best as our mAP is around 71%. However, this can be explained as a higher mAP can also indicate an over-fitting of data, and we optimized our model to reduce over-detection. 

The final two metrics were precision and recall.  Precision is the fraction of relevant instances compared to retrieved instances, which measures how many objects are correctly classified. Recall is the fraction of relevant instances that were retrieved, which measures the percentage of true postives vs. false positives. Having a high number for both of these metrics is encouraging, as it suggests that the model is correctly detecting potholes. Our precision metrics is around 80% and our recall is around 70%, which aren't amazing but do show that our model is working correctly a high majority of the time. In our own tests images, there were no cases in which a pothole was not detected or the model drew a bounding box around something that was not a pothole. 

### Model: Results
# INSERT TABLES AND IMAGES OF BOUNDING BOXES

### Model: Problems Encountered

### User Uploads
Once we had a trained YOLO model, we were able to move into other functionality. One of our main goals with this project was to take the current state-of-the-art and make it real-world usable. In order to do that, we came up with an idea that users can upload their own images, videos, or live captures and the model is run over that submission. To build this functionality, we used Python...

# Samyu explains how she built the upload page

### User Uploads: Results
# link to upload page

### User Uploads: Problems Encountered

The intention of this functionality is to notify government officials of potholes in specific areas so that the time typically taken for screening roads and mapping the ideal route for maintenance and repair is cut down. Because this application can be run on live video, users could attach their dashcams to the model as they are driving -- the survellience process is fully automated in this scenario. Otherwise, pedestrians, bikers, and other commuters could take pictures with their phones and submit that data. Essentially, this step is intended to eliminate the need for road surveys. In order to optimize the repair process, we will use metadata from user uploads to create a map of potholes in a given area.

### Pothole Mapping
The final step of our implementation is mapping the location of images uploaded by users. In order to do this, we hosted a database of images and wrote a JavaScript script to pull the metadata (latitude, longitude coordinates) from each image. Then, a dot is populated on the map at those points. The resulting map is embedded below, with points corresponding to our own collected images to prove correctness of our workflow. 

# Eric adds more details about how he built this part.

### Pothole Mapping: Problems Encountered

The motivation of adding this, as mentioned, is to improve outcomes of road maintenance. The most costly portion of maintenance is materials, with time cost for mapping an optimal route coming in second. Our map reduces that cost. Not only are the pothole plotted exactly, but we have images of all the potholes at those locations so workers can identify severity, amount of materials needed, estimate repair time, and a number of other features. 

### Conclusion
Going into this implementation, we set goals to automate the detection of potholes, simplify data collection, and improve the repair process to broadly reduce the presence of potholes. Our YOLO model is able to detect potholes with high accuracy. Users' ability to run the model over dashcam footage, photos, and videos creates a better and simplier way to collect broad data. Mapping those user uploads and plotting an accurate map of local potholes frees time and resources of repair workers. Through these three steps, we have addressed and achieved each of our goals. Hopefully, we can continue to work with this technology to contribute to safer infrastructure across the US and world at large.
