from fastapi import HTTPException, status

ProjectNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Project not found",
)

ProjectAccessForbiddenException = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Not enough permissions to access this project",
)