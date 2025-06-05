from typing import Optional

from pydantic import BaseModel


class HTTPResponseResult(BaseModel):
    is_success: bool
    status_code: int
    response_time: float
    error_message: Optional[str] = None
