"""Database initialization and session management."""
import os
from sqlmodel import SQLModel, create_engine, Session, select
from app.models import Tamagotchi


# Database URL from environment or default
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/sysmon.db")

# Create engine
engine = create_engine(
    DATABASE_URL,
    echo=False,  # Set to True for SQL query logging
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)


def init_db():
    """Initialize database tables."""
    SQLModel.metadata.create_all(engine)
    
    # Create default Tamagotchi if none exists
    with Session(engine) as session:
        tamagotchi = session.exec(select(Tamagotchi)).first()
        if not tamagotchi:
            tamagotchi = Tamagotchi(name="Server-chan")
            session.add(tamagotchi)
            session.commit()
            print("✓ Created default Tamagotchi: Server-chan")


def get_session():
    """Get database session."""
    with Session(engine) as session:
        yield session
