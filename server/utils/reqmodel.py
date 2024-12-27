from robyn.types import JSONResponse

class LoginResponse(JSONResponse):
    code: int
    status: str
    msg: str
    token: str
    data: dict

class GeneralResponse(JSONResponse):
    code: int
    status: str
    msg: str

class BlogGetSingleResponse(JSONResponse):
    code: int
    status: str
    msg: str
    data: dict