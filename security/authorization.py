from fastapi import HTTPException, status


def admin_auth(payload):
    if payload["key"]["is_admin"] == 0:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Admin role authorization is needed.'
        )
    return True


