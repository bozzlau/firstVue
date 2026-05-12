from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_admin
from app.schemas.blog import CommentOut, CommentUpdate
from app.services import blog as svc

router = APIRouter(prefix="/admin", tags=["admin-comments"])


@router.get("/comments", response_model=list[CommentOut])
def list_all_comments(
    db: Session = Depends(get_db),
    _: str = Depends(get_current_admin),
):
    return svc.get_all_comments(db)


@router.patch("/comments/{comment_id}", response_model=CommentOut)
def update_comment(
    comment_id: int,
    data: CommentUpdate,
    db: Session = Depends(get_db),
    _: str = Depends(get_current_admin),
):
    obj = svc.update_comment(db, comment_id, data)
    if not obj:
        raise HTTPException(status_code=404, detail="Comment not found")
    return obj


@router.delete("/comments/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    _: str = Depends(get_current_admin),
):
    if not svc.delete_comment(db, comment_id):
        raise HTTPException(status_code=404, detail="Comment not found")
