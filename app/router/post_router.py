from fastapi import status, HTTPException, Response, Depends, APIRouter
from fastapi.responses import JSONResponse
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
import app.models as models
from app.database import get_db
from app.schemas import PostCreate, PostUpdate, ResponsePost
import app.oauth2 as oauth2

postapi = APIRouter(
    prefix="/posts", 
    tags=["Posts"]
)

#Get List of all the Posts
@postapi.get("/")
async def get_posts(db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_token), 
                    limit: int = 10, skip: int = 0, search: Optional[str] = ""): 
    # cursor.execute(""" SELECT * FROM posts""")
    # posts = cursor.fetchall()
    #posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit=limit).offset(offset=skip).all()
    result = db.query(models.Post, func.count(models.Votes.post_id).label("vote_count")).join(
        models.Votes, models.Votes.post_id == models.Post.id, isouter= True).group_by(
        models.Post.id).filter(models.Post.title.contains(search)).limit(limit=limit).offset(offset=skip).all()
    posts_with_counts = [{"post": post, "vote_count": vote_count} for post, vote_count in result]
    return posts_with_counts

#Create Post 
@postapi.post("/create", status_code=status.HTTP_201_CREATED, response_model=ResponsePost)
async def create_post(post:PostCreate,db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_token)): 
    # cursor.execute("INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *", 
    #                (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
   new_post = models.Post(owner_id = current_user.id,**post.model_dump())
   db.add(new_post)
   db.commit()
   db.refresh(new_post)
   return new_post

# Get Post using ID
@postapi.get("/{id}", response_model=ResponsePost)
async def single_post(id: int, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_token)): 
    # cursor.execute("SELECT * FROM posts WHERE id = %s ", (str(id),))
    # searched_post = cursor.fetchone()
    #post = id_post(id=id)
    post_query = db.query(models.Post).filter(models.Post.id == id)
    if not post_query.first(): 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} not found", headers={
            "error":"404"
        })
    if post_query.first().owner_id != current_user.id: 
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, 
                            detail=f"No post found with user id: {current_user.id}", headers={
                                "status":"No Post Found"
                            })
    return post_query.first()

#Get posts owned by the user only
@postapi.get("/collection/myposts", response_model=List[ResponsePost])
async def get_recentPost(db: Session = Depends(get_db), current_user: dict = Depends( oauth2.get_current_token)): 
    #recpost = len(my_posts)
    # cursor.execute("SELECT COUNT(id) FROM posts")
    # countPost = cursor.fetchone()
    myPost = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
    if not myPost:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=f"No posts found, created by {current_user.id}", headers={
            "posts":"None"
        })
    return myPost


#Count the number of posts
@postapi.get("/collection/count",)
async def get_recentPost(db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_token)): 
    #recpost = len(my_posts)
    # cursor.execute("SELECT COUNT(id) FROM posts")
    # countPost = cursor.fetchone()
    print(current_user.email)
    countPost = db.query(models.Post).filter(models.Post.owner_id == current_user.id).count()
    return {f"number of post by id: {current_user.id}":countPost}

#Delete post using ID
@postapi.delete("/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int,db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_token)): 
    #cursor.execute("""DELETE FROM posts WHERE id = %s returning *""",(str(id),))
    #deleted_post = cursor.fetchone()
    print(current_user.email)
    post_query = db.query(models.Post).filter(models.Post.id == id)

    if not post_query.first(): 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist",
                         headers={
                            "error":"post unavailable"
                            })
    if post_query.first().owner_id != current_user.id: 
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform task",
                            headers={
                                "status":"Not Authorized"
                            })
    post_query.delete()
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    
# Update Post using ID
@postapi.put("/update/{id}", status_code=status.HTTP_200_OK, response_model=ResponsePost)
async def update_post(id:int, post:PostUpdate,db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_token)): 
   
    #cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
    #              (post.title, post.content, post.published, str(id)) )
    #updated_post = cursor.fetchone()
    #conn.commit()
    print(current_user.email)
    post_query = db.query(models.Post).filter(models.Post.id == id)
    if not post_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post id: {id} does not exist",
                            headers={
                                "error":"post unavailable"
                                })
    if post_query.first().owner_id != current_user.id: 
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform task",
                            headers={
                                "status":"Not Authorized"
                            })
    post_query.update(post.model_dump())
    db.commit()
    return post_query.first()