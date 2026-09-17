from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, require_permission
from app.models.pricing import PriceList, PriceListItem
from app.models.user import User
from app.schemas.pricing import PriceListCreate, PriceListItemCreate, PriceListItemRead, PriceListRead

router = APIRouter(prefix="/pricing", tags=["pricing"])


@router.post("/lists", response_model=PriceListRead, status_code=status.HTTP_201_CREATED)
def create_price_list(
    payload: PriceListCreate,
    db: Session = Depends(get_db),
    _user: User = Depends(require_permission("pricing:create")),
) -> PriceList:
    price_list = PriceList(**payload.model_dump())
    db.add(price_list)
    db.commit()
    db.refresh(price_list)
    return price_list


@router.get("/lists", response_model=list[PriceListRead])
def list_price_lists(
    db: Session = Depends(get_db), _user: User = Depends(require_permission("pricing:read"))
) -> list[PriceList]:
    return db.query(PriceList).all()


@router.post("/items", response_model=PriceListItemRead, status_code=status.HTTP_201_CREATED)
def add_price_list_item(
    payload: PriceListItemCreate,
    db: Session = Depends(get_db),
    _user: User = Depends(require_permission("pricing:create")),
) -> PriceListItem:
    item = PriceListItem(**payload.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.get("/lists/{price_list_id}/items", response_model=list[PriceListItemRead])
def list_price_list_items(
    price_list_id: str,
    db: Session = Depends(get_db),
    _user: User = Depends(require_permission("pricing:read")),
) -> list[PriceListItem]:
    return db.query(PriceListItem).filter(PriceListItem.price_list_id == price_list_id).all()
