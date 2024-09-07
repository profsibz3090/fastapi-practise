from fastapi import APIRouter, HTTPException, Response, status, Depends
from .. import database, oauth2, schemas, models
from sqlalchemy.orm import Session

router = APIRouter(prefix='/vote', tags=['Vote'])

@router.post('/')
def vote(vote_data: schemas.Vote, db: Session = Depends(database.get_db), current_user: schemas.UserOut = Depends(oauth2.get_current_user)):
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote_data.post_id, models.Vote.user_id == current_user.id)
    vote = vote_query.first()
    if vote_data.dir == 1:
        if vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f'User with id {current_user.id} has already like post {vote_data.post_id}'
            )
        new_vote = models.Vote(
            post_id = vote_data.post_id,
            user_id = current_user.id
        )
        db.add(new_vote)
        db.commit()
        return Response(
            status_code=status.HTTP_201_CREATED,
            content='post liked successfully'
        )
    else:
        if not vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'User with id {current_user.id} has never liked this post'
            )
        vote_query.delete()
        db.commit()
        return Response(
            status_code=status.HTTP_204_NO_CONTENT
        )