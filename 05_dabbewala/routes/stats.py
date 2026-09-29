from fastapi import APIRouter, Depends,HTTPException,Query
from database import get_session
from models import Order, OrderCreate, OrderUpdate,StatusLog,OrderStatus
from sqlmodel import Session,select,func
from datetime import datetime,date


router = APIRouter(prefix="/stats", tags=["stats"])

@router.get('/daily')
def get_daily_stats(
    summary_date: date | None = Query(None, description="Date for which to retrieve daily stats (YYYY-MM-DD)"),
    session: Session = Depends(get_session)
):
    if summary_date is None:
        summary_date = date.today()

    start = datetime.combine(summary_date, datetime.min.time())
    end = datetime.combine(summary_date, datetime.max.time())

    total = 0
    summary = {}

    for status in OrderStatus:

        count = session.exec(
            select(func.count(Order.id)).where(
                Order.created_at >= start,
                Order.created_at <= end,
                Order.status == status
            )
        ).one()

        summary[status.value] = count
        total += count

    return {
        'date': summary_date,
        'total_orders': total,
        'by_status': summary
    }

  