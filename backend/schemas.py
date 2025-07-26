from pydantic import BaseModel, Field

class Anvelope(BaseModel):
    id: int = Field(ge=0)
    anvelope_name: str = Field(max_length=100)
    anvelope_budget: int = Field(ge=0)
    budget_id: int = Field(ge=0)

class Budget(BaseModel):
    id: int = Field(ge=0)
    total_budget: int = Field(ge=0)

class CreateBudget(BaseModel):
    total_budget: int = Field(ge=0)

class CreateAnvelope(BaseModel):
    anvelope_name: str = Field(max_length=100)
    anvelope_budget: int = Field(ge=0)
    budget_id: int = Field(ge=0)