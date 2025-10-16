from typing import TypeVar, Generic, Optional

from pydantic import BaseModel

T = TypeVar("T")    # This line defines a type variable named T. It’s a placeholder type you can use inside generic classes.

class ApiResponseModel(BaseModel, Generic[T]):
    message: str
    data: Optional[T] = None  # optional means this field can be None
    status: bool