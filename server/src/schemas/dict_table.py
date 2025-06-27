from pydantic import BaseModel


class DepartmentResponse(BaseModel):
    id: int
    name: str

class PositionResponse(BaseModel):
    id: int
    name: str
class InterestResponse(BaseModel):
    id: int
    name: str

