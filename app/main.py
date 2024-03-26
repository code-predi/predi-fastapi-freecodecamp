from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
from psycopg2.extras import RealDictCursor
import app.my_variables as my_variables
import time
from app.router.post_router import postapi
from app.router.user_router import userapi
from app.router.auth_router import authapi
from app.router.vote_router import voteapi



app = FastAPI()


while True: 
    try: 
        conn = psycopg2.connect(host=my_variables._host,database=my_variables._database, user=my_variables._user, 
                            password=my_variables._password, cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection ESTABLISHED SUCCESSFULLY")
        break 
    except Exception as error:
        print("Connection to database FAILED!")
        print("*ERROR*", error)
        time.sleep(2)
    
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(authapi)  
app.include_router(postapi)   
app.include_router(userapi)   
app.include_router(voteapi) 
  


@app.get("/")
async def root():
    return{"message":"Hello World"}

