from fastapi import Response


class BadRequest(Response):
    def __init__(self, content=''):
        super().__init__(status_code=400, content=content)

class Unauthorized(Response):
    def __init__(self, content=''):
        super().__init__(status_code=401, content=content)

class Forbidden(Response):
    def __init__(self, content=''):
        super().__init__(status_code=403, content=content)

class NotFound(Response):
    def __init__(self, content=''):
        super().__init__(status_code=404, content=content)



class Successful(Response):
    def __init__(self, content=''):
        super().__init__(status_code=200, content=content)

class Created(Response):
    def __init__(self, content=''):
        super().__init__(status_code=201, content=content)

class NoContent(Response):
    def __init__(self, content=''):
        super().__init__(status_code=204)

class InternalServerError(Response):
    def __init__(self, content=''):
        super().__init__(status_code=500, content=content)