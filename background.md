---
title: Backstory, Approach, and Motivation
permalink: /background/
layout: pagejs
excerpt: Approach, Motivation, and Background Information
comments: false
---
### Jump to...
[Current State-of-the-Art](#current-state-of-the-art)


### Background Information
<details open>
<summary>What you need to know about potholes...</summary>
There are 55 million potholes in the U.S. alone, causing 27% of the roads to be deemed substandard. Potholes can cause collisions and severe injuries to all types of vehicles, including cyclists and pedestrians. Places with cold climates, such as Wisconsin, are especially susceptible to potholes as they form easily due to water and snow seeping into cracks and freezing during the night. Currently, the only way used to identify potholes on roads involves having a person manually inspect and report potholes they come across. This can lead to potholes going undetected and is also an inefficient way of gathering data. In order to save taxpayer money and government resources, we can identify potholes from drone and CCTV footage using computer vision. By using computer vision, we can automate the detection process of potholes, simplifying the collection of data necessary to determine how best to allocate infrastructure funds. This would lead to potholes getting noticed earlier and thus fixed faster. 
</details>

### Motiviation
<details>
<summary>Why we want to solve this problem...</summary>
We are personally inconvenienced when there are potholes on the road, and find it to be a general danger to our community. Potholes are a massive issue that is close to our hearts. Samyu’s family member died from a pothole injury – she was sitting sideways on the back of a scooter in India, and although they were driving at a slow pace, the scooter hit a pothole and she fell off, and ultimately died from the head injury that resulted. We felt that by using computer vision to detect potholes, we could positively impact communities around the world, and optimize for better allocation of resources.
</details>

### Approach
##### Current State-of-the-Art

The current approach to solving the prevalence of potholes is by using deep learning. 
[This paper](https://www.hindawi.com/journals/ace/2022/9221211/) describes the current solutions:  

* [Here](https://scholar.google.com/scholar_lookup?title=Three%20combination%20value%20of%20extraction%20features%20on%20glcm%20for%20detecting%20pothole%20and%20asphalt%20road&author=Y.%20K.%20Arbawa&author=F.%20Utaminingrum&author=E.%20Setiawan&publication_year=2021), a pothole detection system exists using a grey-level co-occurrence matrix (GLCM) feature extractor and a support vector machine (SVM) as the classifier.  

* [Here](https://scholar.google.com/scholar_lookup?title=Real-time%20machine%20learning-based%20approach%20for%20pothole%20detection&author=O.%20A.%20Egaji&author=G.%20Evans&author=M.%20G.%20Griffiths&author=G.%20Islas&publication_year=2021), five binary classifiers (SVM, Logistic regression, Naive Bayes, KNN, and Random forest tree) are used over data from cell phones and synthesized to create a complete model.  
    
* [Here](https://scholar.google.com/scholar_lookup?title=Convolutional%20neural%20network%20for%20pothole%20detection%20in%20asphalt%20pavement&author=W.%20Ye&author=W.%20Jiang&author=Z.%20Tong&author=D.%20Yuan&author=J.%20Xiao&publication_year=2021), a model using conventional CNN and pre-pooling CNN are used to inspect potholes with 96% accuracy.  

Overall, the current state of the art includes many machine and deep learning models, especially those relating to neural networks like CNN. 
<br>
Upon researching further, there are many expansions upon a simple CNN model, with the two most prevalent being YOLO (You Only Look One) and SSD (Single Shot Detector). 
<br>
[This paper](https://www.irjmets.com/uploadedfiles/paper/issue_5_may_2022/22270/final/fin_irjmets1652093163.pdf) describes how SSD works and how it detects objects. At a high level, CNN is a neural network model where neurons on one layer have connections only with other neurons on its own layer, not on other layers. SSD is an optimization of this in which the algorithm uses many convolutional layers. This allows it to run both quicker and more vigorously to classify and create bounding boxes on images. 
<br>

![SSD diagram](https://www.researchgate.net/profile/Antoine-Vacavant/publication/340654462/figure/fig4/AS:893266799128593@1589982809926/Single-Shot-Multi-Box-Detector-SSD-architecture-47.ppm)

<br>
YOLO is similar to SSD in that they are both one-step detectors, both detecting and classifying the image on the first (and only) look. At a high level, it is a neural network that makes predictions of bounding boxes and probabilities at the same time on one connected layer.
<br>

![YOLO diagram](https://miro.medium.com/max/1400/1*ZbmrsQJW-Lp72C5KoTnzUg.jpeg)

<br>
Both these neural network models/algorithms have been used in object detection, and much of our research so far has been determining what the best model would be for our problem. Right now, we are looking at using YOLOv5 for our object classification. This model requires images to be annotated before passing them through, which will be another step to consider in our updated timetable. 

##### Our Execution Plan
<details>
<summary>What our solution will look like...</summary>
Since our project is a simple classification task (pothole versus non-pothole) and we have found multiple models that can classify them in real-time with accuracy >95%, we will re-implement an existing solution. However, in an attempt to better understand the code and have greater control in tweaking variables and layers, we will draw inspiration from multiple models and hopefully make one that can perform at least as good as existing models. We will also combine multiple datasets of potholes while training our model to lower variance (to a certain extent) and also reduce the chance of overfitting the data. This is part of why we feel our solution can perform better than existing solutions. We decided to try and build the model in YOLOv5 using Google Collab, but if we run into issues with building our model in YOLOv5, we may look into using a different type of CNN. We will use Google Collab or our personal devices to train the model. 
<br>

Since current solutions to this problem exist, we’re hoping to add a novel layer via our expansions on the model. After we train our model, we will make a simple web-based user application which will allow a user to upload a photo and run it against our pretrained model. Our model will draw bounding boxes on the photo and we will extract EXIF data (if available) from the image and show on a map where the photo was taken. We will also personally take/collect photos from around the UW-Madison campus and feed them into our application so we can build a very detailed and up-to-date map of potholes around our campus. Afterwards we hope to get in contact with the Wisconsin Department of Transportation and see if our detailed model/map will be of any use to them. We will also relay our findings to certain contractors around campus who could use this information to find work. We hope that by reaching out, we will draw attention to the pothole issue so these organizations will hopefully fix these potholes in the long run and make our campus a safer place.
<br>

We think this will be a worthy time investment as the detection models alone are not enough to create real-world change. As far as we have researched, most of the current solutions exist as academic projects or toy projects -- nothing so far has been applied to the state of the roads so that progress can be made in the real world. This work has not been adequately completed in our minds, and this is the other part of why our solution will expand and improve upon work already done. 
</details>
