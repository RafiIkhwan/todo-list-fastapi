from fastapi import HTTPException, status

TaskNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Task not found",
)