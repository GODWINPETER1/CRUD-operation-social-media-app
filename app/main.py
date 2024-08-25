from fastapi import FastAPI , status , HTTPException;
from pydantic import BaseModel;
from fastapi.middleware.cors import CORSMiddleware
import psycopg

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    print(new_posts_rows)
    
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

# Get a single post
@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute("SELECT * FROM products WHERE id = %s", (id,))
    new_post = cursor.fetchone()

    if not new_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    column_name = [desc[0] for desc in cursor.description]
    social_media_post = dict(zip(column_name, new_post))
    
    return {"data": social_media_post}

# Delete a single post 
@app.delete("/posts/{id}")
def deleted_post(id: int):
    
    cursor.execute("DELETE FROM products WHERE id = %s RETURNING *" , (id,))
    new_post_deleted_row = cursor.fetchone()
    
    if not new_post_deleted_row:
        
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    conn.commit()
    
    
    column_name = [desc[0] for desc in cursor.description]
    social_media_post_deleted = dict(zip(column_name, new_post_deleted_row))
    
    return {"data" : social_media_post_deleted} 

# Update a single post
@app.put("/posts/{id}")

def update_post(id: int , post: Post):
    
    cursor.execute("UPDATE products SET name = %s , price = %s , inventory = %s WHERE id = %s RETURNING *" , (post.name , post.price , post.inventory , id))
    updated_post = cursor.fetchone()
    
    
    conn.commit()
    
    column_name = [desc[0] for desc in cursor.description]
    social_media_post_updated = dict(zip(column_name, updated_post))
    
    return {"data" : social_media_post_updated}
    

    
    
    

