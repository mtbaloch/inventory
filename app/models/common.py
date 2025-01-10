from sqlmodel import SQLModel, Field
from uuid import uuid4, UUID
from datetime import datetime, timezone


class BaseModel(SQLModel):
    id : UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    create_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    # explicitly
    class Config:
        orm_mode = True
