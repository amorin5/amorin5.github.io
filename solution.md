---
title: Implementation and Results
layout: pagejs
permalink: "/solution/"
customjs:
 - /assets/js/maps.js
comments: false
---
<!-- also include results and takeaways here? -->
Our implementation has three main portions. The first is the trained YOLOv5 [model](#model) that detects potholes out of images and videos. The second part is an additional layer of functionality that allows users to upload their own photos and run the model over those via a [web application](#the-web-application). The third and final part is a [map](#pothole-mapping) of user submissions, plotting the location of potholes in an area using metadata from the user image. 
[Link to our code base](https://github.com/amorin5/amorin5.github.io)
<br>

Don't feel like reading all this? Check out our 5min presentation:
[Presentation Video](assets/img/pres_video.mp4)

## Model
We decided to use a YOLO (You Only Look Once) model for object detection. We settled on this approach because the current research points to this being the most efficient for detection. To get started, we found a dataset of potholes in order to train our model. We used a YOLO skeleton we found online and tweaked it for our use. The model was written and hosted on Google Collab for training. Using our dataset and other sources, we trained our model up to 1000 epochs. The best results were observed at epoch 373 and the model stopped training early at epoch 474 as improvements were not observed. After training the model, we generated performance metrics for the bounding box creation and the actual object detection. 

<!-- insert graph of metrics -->

We measured the both the training and validation loss for both bounding box creation and pothole detection. Loss represents how far away our model is from making accurate predictions. It can and should trend to zero and we were trying to minimize the loss in the given areas. Validation loss occurs at the end of an epoch by comparing the output to the validation dataset. Training loss occurs at the end of each step inside an epoch as the model is trying to improve the loss. Above, we can see that both training and validation loss are trending downward for pothole detection and bounding box generation, which is a good indicator that our model has high accuracy.  

![Performance Metrics](assets/img/metrics.jpg)

We also measured mAP, the Mean Average Performance of the model. mAP is a formula that considers the confusion matrix, intersection over region, recall, and precision. A higher mAP indicates a higher performing ML model. In our case, these metrics aren't the best as our mAP is around 71%. However, this can be explained as a higher mAP can also indicate an over-fitting of data, and we optimized our model to reduce over-detection. 

The final two metrics were precision and recall.  Precision is the fraction of relevant instances compared to retrieved instances, which measures how many objects are correctly classified. Recall is the fraction of relevant instances that were retrieved, which measures the percentage of true positives vs. false positives. Having a high number for both of these metrics is encouraging, as it suggests that the model is correctly detecting potholes. Our precision metrics is around 80% and our recall is around 70%, which aren't amazing but do show that our model is working correctly a high majority of the time. In our own tests images, there were no cases in which a pothole was not detected or the model drew a bounding box around something that was not a pothole. 

### Model: Results
Our model outputs these images, with bounding boxes drawn around the detected potholes and a numerical indication of how confident the model is in its detection. Some output images can be seen below:

![Annotated pothole image](/assets/img/annotated-pothole-1.jpeg) <img align = "center">

![Annotated pothole image](/assets/img/annotated-pothole-2.jpeg)

![Annotated pothole image](/assets/img/annotated-pothole-3.jpeg)

![Annotated pothole image](/assets/img/annotated-pothole-4.jpeg)

![Annotated pothole image](/assets/img/annotated-pothole-5.jpeg) <img align = "center">

<br>
We wanted to include this image to show that when no potholes are detected, the model also recognizes that and does not draw any bounding boxes or identification markers.

### Model: Problems Encountered
The biggest problem with the model was just choosing which CNN to use, which is covered in more detail on the background page. Beyond that, most of the troubleshooting was tinkering with the training, seeing how many epochs created the optimal model, and getting the model to communicate with the Python code for the user upload functionality. These problems were easily overcome with trial and error. 

## The Web Application

### Web App: Frameworks and Tools

The web application was built using the framework [flask](https://flask.palletsprojects.com/en/2.2.x/), which facilitated the process of creating files to populate for a web app that involves user uploads. We added the yolo repository to the flask setup, which made it such that we could send any user-uploaded image to the model we had already trained, without needing to re-train each time. 

We also used a Python virtual environment to iteratively develop and see our results on a local web page. 

### Web App: Backend

In our `app.py`, we implemented the following restAPI methods:
1. `detect`, POST method: saves the user-uploaded photo/video
2. `opencam`, GET method: opens user's front camera and running our `detect.py` on it to draw labeling boxes around potholes over real-time video footage.
3. `return-files`, GET method: returns annotated version of user-uploaded image 

### Web App: Interaction with YOLO

After we trained our model, we preserved `best.pt`, the file with weights that yielded the most accurate results. Then, we used our `detect.py` in conjunction with these weights to perform object detection on each new photo/video without needing to re-train the model.

### Web App: Frontend

To create the frontend visuals of our web application, we built out simple `html` files and populated them with the buttons and links we wanted. We added attributes that called the appropriate backend methods when the respective buttons were clicked. Additionally, we created a second `html` file for the functionality of our clickable "Download" button appearing after the object-detection had completed. 


### Web App: Results of User Uploads

 Below is a demo of one of our application's functionalities: performing pothole-detection on a user-uploaded image and then presenting the annotated image for user download.
 
 <iframe width="560" height="315" src="https://www.youtube.com/embed/d8X3WLZLb5Q" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>


### Web App: Problems Encountered

One of the biggest sources of difficulties was just managing different imports, packages, and dependencies. The YOLO repository has hundreds of imports of commonly-used packages, which were in many occasions inconsistent or conflicting with the versions used by `flask`. To fix these, we often had to manually uninstall packages and reinstall different versions of them using `pip`. Additionally, there were inconsistencies around versions of `python` that newer versions of packages were compatible, and sometimes we had dependency issues due to our `venv`.

And since none of us had strong prior experience with web development, we were debugging each of these issues on the fly, sometimes finding that resolving one just opened up the door to an influx of new issues.

## Pothole Mapping

### Pothole Mapping: The Map

Our pothole map with markers can be found at the bottom of the page. This interactive map marks all of the pothole locations that are stored in our database. The motivation of adding this, as mentioned, is to improve outcomes of road maintenance. The most costly portion of maintenance is materials, with time cost for mapping an optimal route coming in second. Our map reduces that cost. Not only are the potholes plotted with precision, but we have images of all the potholes at those locations so workers can identify severity, amount of materials needed, estimate repair time, and a number of other features. Some future implementations might include having a shortest-path route generation which would attempt to draw a path that intersects all of the pothole points in the shortest distance possible. This would allow workers to not have to determine an optimal route themselves and instead follow an optimal computer generated route. 

### Pothole Mapping: Frameworks and Tools

The pothole map was built using [Google Maps Platform](https://developers.google.com/maps) which allows this website to host an interactive Google Map and [Google Firebase](https://cloud.google.com/firestore/docs) which is our database that holds coordinate data for our pothole markers. The map code is written in JavaScript. 

### Pothole Mapping: Problems Encountered

One of the issues we encountered was trying to set up a Google Developer account to access their API for both Maps and Firebase. We ended up having to learn about how to manage API keys and credentials, figure out how our website code would access our Google Developer account and how to connect the Map with Firebase. Luckily, there were a lot of resources about how to embed a Map on a website and how to connect to a Firebase. Connecting to a Firebase was a little tricky since all of the code and examples provided were written in Typescript so it took some time trying to convert it into working JavaScript. The main issue was connecting the database back to the website. This ended up taking the bulk of our time because none of us had experience with embedded JavaScript elements. The issue ended up just being a simple syntax error (that we spent hours tracking down, apparently there was a race condition where if the map would load before the JS code to fetch coordinate data from the database then the map would not initialize. The fix was adding the defer keyword for the JS code) so once we figured that out our map worked, finishing the flow from user upload to map plot points.

## Final Thoughts
Going into this implementation, we set goals to automate the detection of potholes, simplify data collection, and improve the repair process to broadly reduce the presence of potholes. Our YOLO model is able to detect potholes with high accuracy. Users' ability to run the model over dashcam footage, photos, and videos creates a better and simpler way to collect broad data. Mapping those user uploads and plotting an accurate map of local potholes frees time and resources of repair workers. In this way, the entire process is automated. Through these three steps, we have addressed and achieved each of our goals. Hopefully, we can continue to work with this technology to contribute to safer infrastructure across the US and world at large.

## Interactive Pothole Map
