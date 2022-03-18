from fastapi import FastAPI
from models import image
from typing import List

app = FastAPI()

db: List[image] = [
    # image(
    # tags = [['best', 'dog', 'breeds', 'firsttime', 'owners', '5', 'easy', 'train', 'pups', 'hello'],
    #         ['10', 'cutest', 'dog', 'breeds'],
    #         ['10', 'cutest', 'dog', 'breeds', '2022', 'love', 'doodles'],
    #         ['15', 'cute', 'dog', 'breeds', 'wo', 'nt', 'able', 'resist', 'southern', 'living'],
    #         ['43', 'best', 'small', 'dog', 'breeds', 'toy', 'breed', 'dogs']]

    # ),
    # image( 
    # tags = [['best', 'dog', 'breeds', 'firsttime', 'owners', '5', 'easy', 'train', 'pups', 'hello'],
    #         ['10', 'cutest', 'dog', 'breeds'],
    #         ['10', 'cutest', 'dog', 'breeds', '2022', 'love', 'doodles'],
    #         ['15', 'cute', 'dog', 'breeds', 'wo', 'nt', 'able', 'resist', 'southern', 'living'],
    #         ['43', 'best', 'small', 'dog', 'breeds', 'toy', 'breed', 'dogs']]

    # )
    ]

@app.get("/")
async def root():
    return {"Make more specific request."}

@app.get("/images")
async def fetch_images():
    return db

@app.post("/images")
async def post_image(image: image):
    db.append(image)
    

