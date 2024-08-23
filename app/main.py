from fastapi import FastAPI , status;
from pydantic import BaseModel;
import psycopg

app = FastAPI()

class Post(BaseModel):
    name: str
    price: int
    inventory: int

# connect server to the database
try:
    conn = psycopg.connect("dbname = fastapi user = postgres password = Moshi1996")
    cursor = conn.cursor()
    print("Database connected successfully")

except Exception as error:
    print(f"Database could not connect successfully , error: {error} ")
    

# get all the posts in the database
@app.get("/posts")
def get_posts():
    
    cursor.execute("SELECT * FROM products")
    new_posts_rows = cursor.fetchall()
    column_name =  [desc[0] for desc in cursor.description]
    social_media_posts = [dict(zip(column_name , new_posts_row)) for new_posts_row in new_posts_rows]
    
    return {"data" : social_media_posts}

# create the posts 
@app.post("/posts" , status_code = status.HTTP_201_CREATED)
def create_posts(post: Post):
    
    cursor.execute("INSERT INTO products (name , price , inventory) VALUES (%s , %s , %s) RETURNING *" , (post.name , post.price , post.inventory))
    new_post = cursor.fetchone()
    column_names = [desc[0] for desc in cursor.description]
    new_post_dict = dict(zip(column_names, new_post))
    
    conn.commit()
    
    return {"data" : new_post_dict}
    

