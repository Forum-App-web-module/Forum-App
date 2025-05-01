from fastapi import HTTPException


def admin_auth(payload):
    if payload["key"]["is_admin"] == 0:
        raise HTTPException(status_code=403, detail='Admin role authorization is needed.')


