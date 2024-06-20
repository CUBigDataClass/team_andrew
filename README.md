# Right Click Save As

Right Click Save As is an NFT minting verification web application where user can check if their NFT/image is a derivative of another similar art or is it unique before investing

* Our app allows users to upload NFT/image and runs a reverse Google image search
* Gets Top 5 image matches -> runs image similarity and NER machine learning models
  - Image similarity returns percent % matching similarity between original image upload and top 5 images
  - NER returns top 5 associated tags and top 3 entities for image matches
  
Architecture:
![image](https://github.com/yugo9081/Right-Click-Save-As/assets/54964332/6887e861-88be-46af-acdc-0624af18adec)
![image](https://github.com/yugo9081/Right-Click-Save-As/assets/54964332/64ed6f7e-fe38-4647-97ad-80c31434dff8)

Demo Screenshot:
![image](https://github.com/yugo9081/Right-Click-Save-As/assets/54964332/20642059-dbd8-4d25-9249-a2d8b8ba3fef)


﻿Requirements for Installing Project:

* For Windows users.
* Install Python3 and pip before installing these.

MongoDB:
1. Install MongoDB Compass (https://www.mongodb.com/products/compass)
2. Get Invitation for our Cluster from Emma
3. Mongo connection string: mongodb+srv://team_andrew:Green91%40%40@cluster1.jsqyd.mongodb.net/test

PyMongo:
1. Run the following command in your IDE terminal(Mine is Visual Studio Code) : pip install pymongo
2. Also, run this command for connecting cluster: pip install pymongo[gssapi,aws,ocsp,snappy,srv,tls,zstd,encryption]

Flask:
1. Run the following command in your IDE terminal(Mine is Visual Studio Code) : pip install flask


To Run Flask, run the following command in terminal: python3 -m flask run, then, click on the website address(on the terminal) to open up the flask web application.

Spacy

1. Install the following pip commands. 
  pip install --user -U pip setuptools wheel
  pip install --user -U spacy
  pip install --user pyresparser
  pip install --user spacytextblob
2. Install the following python commands. 
  python -m textblob.download_corpora
  python -m spacy download en_core_web_sm
