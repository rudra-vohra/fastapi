from fastapi import APIRouter, Depends,HTTPException,Query
from database import get_session
from models import Order, OrderCreate, OrderUpdate,OrderStatus
from sqlmodel import Session,select
from datetime import datetime



router = APIRouter(prefix="/orders", tags=["Orders"])


# Create a new order
@router.post("/", response_model=Order)
def create_order(order: OrderCreate, session: Session = Depends(get_session)):
    db_order = Order(**order.model_dump())
    session.add(db_order)
    session.commit()
    session.refresh(db_order)
    return db_order


# Get orders with multiple query filters
@router.get("/", response_model=Order)
def get_orders(
    status: OrderStatus | None = Query(None, description="Filter orders by status"),
    created_date: str | None = Query(None, description="Filter orders by creation date (YYYY-MM-DD)"),
    skip: int = Query(0,ge=0),
    limit: int = Query(10, ge=1, le=100),
    session: Session = Depends(get_session)
):
    query = select(Order)

    if status:
        query = query.where(Order.status == status)

    if created_date:
        start = datetime.combine(created_date, datetime.min.time())
        end = datetime.combine(created_date, datetime.max.time())
        query = query.where(Order.created_at >= start, Order.created_at <= end)

    query = query.offset(skip).limit(limit)
    return session.exec(query).all()



# Update order status or delivery address
@router.patch('/{order_id}', response_model=Order)
def update_order(

    order_id: int,
    order_update: OrderUpdate,
    session: Session = Depends(get_session)
):
    db_order = session.get(Order, order_id)
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")

    updated_order = order_update.model_dump(exclude_unset=True)

    for key, value in updated_order.items():
        setattr(db_order, key, value)

    session.add(db_order)
    session.commit()
    session.refresh(db_order)
    return db_order







