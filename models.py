from pydantic import BaseModel

class CallSummary(BaseModel):
    key_points: list[str]
    sentiment: str
    action_items: list[str]