import enum

from pydantic import BaseModel, conint
from typing import Optional, Literal, Dict


class HTTPMethod(enum.Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"


class Config(BaseModel):
    url: str
    method: HTTPMethod = HTTPMethod.GET
    expected_status: conint(ge=100, le=599) = 200
    concurrency: conint(ge=1) = 10
    requests: conint(ge=1) = 100
    headers: Optional[Dict[str, str]] = None
    data: Optional[str] = None
