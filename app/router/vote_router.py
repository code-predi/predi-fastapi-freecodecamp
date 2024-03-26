from fastapi import status, HTTPException, Response, Depends, APIRouter
from sqlalchemy.orm import Session
import app.schemas as schemas
import app.database as database
import app.oauth2 as oauth2 
import app.models as models

voteapi = APIRouter(
    prefix="/votes", 
    tags=["Vote"]
    )

@voteapi.post("/", status_code=status.HTTP_201_CREATED)
async def vote_post(vote: schemas.Vote, db: Session = Depends(database.get_db), 
                    current_user : dict = Depends(oauth2.get_current_token)): 
    post_exist = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post_exist: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {vote.post_id} not found", 
                            headers={
                                "error":"No Post"
                                })
    post_query = db.query(models.Votes).filter(
        models.Votes.post_id == vote.post_id, models.Votes.user_id == current_user.id
        )
    if (vote.direction == 1):
        if not post_query.first():
            new_vote = models.Votes(post_id = vote.post_id, user_id = current_user.id)
            db.add(new_vote)
            db.commit()
            return {
                "status":f"Successfully voted post {vote.post_id}"
                }
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Post {vote.post_id} is alredy voted")
    elif(vote.direction == 0):
        if not post_query.first(): 
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No vote found for post {vote.post_id}")
        db.delete(post_query.first())
        db.commit()
        return {"status":f"Vote for post {vote.post_id} deleted"}
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Something went wrong")
    

