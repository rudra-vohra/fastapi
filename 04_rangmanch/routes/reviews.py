from fastapi import APIRouter,Depends,Query,HTTPException
from sqlmodel import Session, select,func
from models import ReadReview,CreateReview,Review,UpdateReview
from database import getSession

router = APIRouter(prefix='/review', tags=['reviews'])

@router.post('/',response_model=ReadReview)
def create(review:CreateReview, session: Session = Depends(getSession)):
    db_review = Review(**review.model_dump())
    session.add(db_review)
    session.commit()
    session.refresh(db_review)
    return db_review


@router.get('/',response_model=list[Review])
def list_reviews(
    play_name : str | None = Query(None,description="Filter by play name"),
    skip : int = Query(0,ge=0,description='Offset value'),
    limit : int = Query(10,ge=1,le=50, description=('Max number of reviews to return')),
    session: Session = Depends(getSession)
):
    query = select(Review)

    if play_name:
        query = query.where(Review.play_name == play_name)

    query = query.offset(skip).limit(limit)

    reviews = session.exec(query).all()
    return reviews

@router.get('/average/{play_name}')
def get_avg(play_name : str, session : Session = Depends(getSession)):
    result = session.exec(
        select(func.avg(Review.rating),func.count(Review.id)).where(Review.play_name == play_name)
    ).first()

    avg_rating, total = result

    if total == 0:
        raise HTTPException(status_code=404,detail='No review found')

    return {
        'play_name' : play_name,
        'avg_rating' : avg_rating,
        'total_reviews': total
    }

@router.get('/{review_id}',response_model=ReadReview)
def get_review(review_id: int, session:Session = Depends(getSession)):
    review = session.get(Review,review_id)
    if not review:
        raise HTTPException(status_code=404, detail='Review not found')

    return review


@router.patch('/{review_id}',response_model=ReadReview)
def update_review(review_id: int, update: UpdateReview, session:Session = Depends(getSession)):
    review = session.get(Review,review_id)
    if not review:
        raise HTTPException(status_code=404, detail='Review not found')

    update_data = update.model_dump()
    for key, value in update_data.items():
        setattr(review,key,value)

    session.add(review)
    session.commit()
    session.refresh(review)

    return review



@router.delete('/{review_id}')
def del_review(review_id: int, session:Session = Depends(getSession)):
    review = session.get(Review,review_id)
    if not review:
        raise HTTPException(status_code=404, detail='Review not found')

    session.delete(review)
    session.commit()

    return {
        'message':'Review Deleted'
    }



