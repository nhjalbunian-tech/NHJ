from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, require_permission
from app.models.procurement import (
    GoodsReceivedNote,
    GRNLine,
    MaterialIssue,
    MaterialIssueLine,
    PurchaseOrder,
    PurchaseOrderLine,
    PurchaseRequisition,
    PurchaseRequisitionLine,
)
from app.models.user import User
from app.schemas.procurement import (
    GoodsReceivedNoteCreate,
    GoodsReceivedNoteRead,
    MaterialIssueCreate,
    MaterialIssueRead,
    PurchaseOrderCreate,
    PurchaseOrderRead,
    PurchaseRequisitionCreate,
    PurchaseRequisitionRead,
)
from app.services import audit_service

router = APIRouter(prefix="/procurement", tags=["procurement"])


# --- Purchase Requisition ----------------------------------------------------
@router.post("/pr", response_model=PurchaseRequisitionRead, status_code=status.HTTP_201_CREATED)
def create_pr(
    payload: PurchaseRequisitionCreate,
    db: Session = Depends(get_db),
    user: User = Depends(require_permission("pr:create")),
) -> PurchaseRequisition:
    pr = PurchaseRequisition(
        project_id=payload.project_id, pr_number=payload.pr_number, requested_by_id=user.id
    )
    db.add(pr)
    db.flush()
    for line in payload.lines:
        db.add(PurchaseRequisitionLine(pr_id=pr.id, **line.model_dump()))

    audit_service.record(db, entity_type="purchase_requisition", entity_id=pr.id, action="create", actor_id=user.id)
    db.commit()
    db.refresh(pr)
    return pr


@router.get("/pr", response_model=list[PurchaseRequisitionRead])
def list_prs(
    db: Session = Depends(get_db), _user: User = Depends(require_permission("pr:read"))
) -> list[PurchaseRequisition]:
    return db.query(PurchaseRequisition).all()


# --- Purchase Order -----------------------------------------------------------
@router.post("/po", response_model=PurchaseOrderRead, status_code=status.HTTP_201_CREATED)
def create_po(
    payload: PurchaseOrderCreate,
    db: Session = Depends(get_db),
    user: User = Depends(require_permission("po:create")),
) -> PurchaseOrder:
    po = PurchaseOrder(
        project_id=payload.project_id,
        pr_id=payload.pr_id,
        po_number=payload.po_number,
        supplier_name=payload.supplier_name,
        created_by_id=user.id,
    )
    db.add(po)
    db.flush()
    for line in payload.lines:
        db.add(PurchaseOrderLine(po_id=po.id, **line.model_dump()))

    audit_service.record(db, entity_type="purchase_order", entity_id=po.id, action="create", actor_id=user.id)
    db.commit()
    db.refresh(po)
    return po


@router.get("/po", response_model=list[PurchaseOrderRead])
def list_pos(
    db: Session = Depends(get_db), _user: User = Depends(require_permission("po:read"))
) -> list[PurchaseOrder]:
    return db.query(PurchaseOrder).all()


# --- Goods Received Note -------------------------------------------------------
@router.post("/grn", response_model=GoodsReceivedNoteRead, status_code=status.HTTP_201_CREATED)
def create_grn(
    payload: GoodsReceivedNoteCreate,
    db: Session = Depends(get_db),
    user: User = Depends(require_permission("grn:create")),
) -> GoodsReceivedNote:
    po = db.get(PurchaseOrder, payload.po_id)
    if not po:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Purchase order not found")

    grn = GoodsReceivedNote(
        po_id=payload.po_id,
        grn_number=payload.grn_number,
        received_by_id=user.id,
        received_date=payload.received_date,
    )
    db.add(grn)
    db.flush()
    for line in payload.lines:
        db.add(GRNLine(grn_id=grn.id, **line.model_dump()))

    audit_service.record(db, entity_type="grn", entity_id=grn.id, action="create", actor_id=user.id)
    db.commit()
    db.refresh(grn)
    return grn


@router.get("/grn", response_model=list[GoodsReceivedNoteRead])
def list_grns(
    db: Session = Depends(get_db), _user: User = Depends(require_permission("grn:read"))
) -> list[GoodsReceivedNote]:
    return db.query(GoodsReceivedNote).all()


# --- Material Issue -------------------------------------------------------------
@router.post("/material-issue", response_model=MaterialIssueRead, status_code=status.HTTP_201_CREATED)
def create_material_issue(
    payload: MaterialIssueCreate,
    db: Session = Depends(get_db),
    user: User = Depends(require_permission("material_issue:create")),
) -> MaterialIssue:
    issue = MaterialIssue(
        project_id=payload.project_id,
        issue_number=payload.issue_number,
        issued_to=payload.issued_to,
        issued_by_id=user.id,
        issue_date=payload.issue_date,
    )
    db.add(issue)
    db.flush()
    for line in payload.lines:
        db.add(MaterialIssueLine(material_issue_id=issue.id, **line.model_dump()))

    audit_service.record(db, entity_type="material_issue", entity_id=issue.id, action="create", actor_id=user.id)
    db.commit()
    db.refresh(issue)
    return issue


@router.get("/material-issue", response_model=list[MaterialIssueRead])
def list_material_issues(
    db: Session = Depends(get_db), _user: User = Depends(require_permission("material_issue:read"))
) -> list[MaterialIssue]:
    return db.query(MaterialIssue).all()
