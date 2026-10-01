from pydantic import BaseModel, Field, root_validator
from typing import Optional

class ServiceSchema(BaseModel):
    id: Optional[int] = None
    name: str
    description: str | None
    price_min: float = Field(ge=0)
    price_max: float = Field(ge=0)
    duration_minutes: int
    is_available: bool
    image: Optional[str] = None

    class Config:
        orm_mode = True

    @root_validator(skip_on_failure=True)
    def validate_price_range(cls, values):
        if values.get("price_min") is not None and values.get("price_max") is not None and values["price_max"] < values["price_min"]:
            raise ValueError("price_max must be greater than or equal to price_min")
        return values

class ServiceCreateSchema(BaseModel):
    name: str
    description: str | None = None
    price_min: float = Field(ge=0)
    price_max: float = Field(ge=0)
    duration_minutes: int
    is_available: bool = True
    image: Optional[str] = None

    @root_validator(skip_on_failure=True)
    def validate_price_range(cls, values):
        if values.get("price_min") is not None and values.get("price_max") is not None and values["price_max"] < values["price_min"]:
            raise ValueError("price_max must be greater than or equal to price_min")
        return values



class ServiceUpdateSchema(BaseModel):
    name: str
    description: str | None
    price_min: float = Field(ge=0)
    price_max: float = Field(ge=0)
    duration_minutes: int
    is_available: bool
    image: Optional[str] = None

    @root_validator(skip_on_failure=True)
    def validate_price_range(cls, values):
        if values.get("price_min") is not None and values.get("price_max") is not None and values["price_max"] < values["price_min"]:
            raise ValueError("price_max must be greater than or equal to price_min")
        return values
