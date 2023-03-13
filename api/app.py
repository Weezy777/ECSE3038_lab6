from fastapi import FastAPI, Request
import motor.motor_asyncio
import pydantic
import  datetime 
from datetime import timedelta
import time
import pytz
from bson import ObjectId
from fastapi.middleware.cors import CORSMiddleware

import requests

app = FastAPI()

origins = [
    "https://rg-lab6-api.onrender.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = motor.motor_asyncio.AsyncIOMotorClient("mongodb+srv://Weezy777:Evadneybaroo1@cluster0.r9znpc2.mongodb.net/?retryWrites=true&w=majority")
db = client.GWright_lab_6
states = db["state"]

pydantic.json.ENCODERS_BY_TYPE[ObjectId]=str

sunset_api_endpoint = f'https://ecse-sunset-api.onrender.com/api/sunset'

sunset_api_response = requests.get(sunset_api_endpoint)
sunset_api_data = sunset_api_response.json()

sunset_time = datetime.datetime.strptime(sunset_api_data['sunset'], '%Y-%m-%dT%H:%M:%S.%f').time()
now_time = datetime.datetime.now(pytz.timezone('Jamaica')).time()


datetime1 = datetime.datetime.strptime(str(sunset_time),"%H:%M:%S")
datetime2 = datetime.datetime.strptime(str(now_time),"%H:%M:%S.%f")

@app.get("/")
async def home():
    return {"LAB 6": "redirect to /api/state"}


@app.put("/api/state")
async def toggle(request: Request): 
  state = await request.json()
  #final_sunset_time = str(get_sunset())
  state["light"] = (datetime1<datetime2)
  state["fan"] = (float(state["temperature"]) >= 28.0) 

  obj = await states.find_one({"tobe":"updated"})
  
  if obj:
    await states.update_one({"tobe":"updated"}, {"$set": state})
  else:
    await states.insert_one({**state, "tobe": "updated"})
  new_obj = await states.find_one({"tobe":"updated"}) 
  return new_obj,204



@app.get("/api/state")
async def get_state():
  state = await states.find_one({"tobe": "updated"})
  
  state["fan"] = (float(state["temperature"]) >= 28.0) 
  state["light"] = (datetime1<datetime2)

  if state == None:
    return {"fan": False, "light": False}
  return 