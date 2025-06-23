from pydantic import BaseModel, Field

class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3)
    priority: int = Field(gt=0, lt=6)
    complete: bool

    model_config = {
    "json_schema_extra": {
        "example": {
            "title": "Todo title",
            "description": "Todo Description",
            "priority": 5,
            "complete": True
        }
    }
}