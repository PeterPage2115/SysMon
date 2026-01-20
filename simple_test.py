from typing import Optional
from sqlmodel import Field, SQLModel

class TestHero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = "test"

print("SUCCESS! Model created.")
print(TestHero.__annotations__)
