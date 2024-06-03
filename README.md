# Right Click Save As

Right Click Save As is an NFT minting verification web application that allows users to upload NFT/Image and runs a reverse Google image search.



﻿Requirements for Installing Project:


*For Windows users.
*Install Python3 and pip before installing these.

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
