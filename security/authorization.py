from fastapi import HTTPException
from common.responses import BadRequest, Unauthorized


def admin_auth(payload):
    if payload["key"]["is_admin"] == 0:
        return Unauthorized(content='Admin role authorization is needed.')


