from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
import time
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()

class Post(BaseModel):
    title : str
    content: str
    published : bool = True # Default Value for optional field
    rating : Optional[int] = None

while True:

    try:
        conn = psycopg2.connect(host="localhost", database="fastapi_app", user="postgres", password="postgres", cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Data Connection established successfull")
        break
    except Exception as error:
        print("Connection to Data Failed")
        print("Error : ", error)
        time.sleep(2)
        

@app.get("/")
def root():
    return {
        "Message" : "API development using FastAPI."
    }

@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM POSTS""")
    posts = cursor.fetchall()
    return {
        "Data" : posts
    }

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post:Post):
    cursor.execute(""" INSERT INTO POSTS (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
    conn.commit()
    new_post = cursor.fetchone()
    return {"data" : new_post}

@app.get("/posts/{id}")
def get_post(id : str):
    cursor.execute(""" SELECT * FROM POSTS WHERE id = %s """, (id,))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id : {id} was not found."
        )
    return {
        "Data" : post
    }

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : str):
    cursor.execute(""" DELETE FROM POSTS WHERE id = %s RETURNING * """, (id,))
    deleted_post = cursor.fetchone()
    conn.commit()
    if not deleted_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id : {id} does not exist"
        )
    return {
        "Data" : deleted_post
    }


@app.put("/posts/{id}")
def update_post(id : str, post:Post):
    cursor.execute(""" UPDATE POSTS SET title = %s, content = %s, published = %s WHERE id = %s  RETURNING * """, (post.title, post.content, post.published, id, ))
    updated_post = cursor.fetchone()
    conn.commit()
    if not updated_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id : {id} does not exist"
        )
    return {
        "Data" : updated_post
    }