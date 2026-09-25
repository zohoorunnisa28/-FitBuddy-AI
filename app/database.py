from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

DATABASE_URL = "sqlite:///./fitbuddy.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(String(100), unique=True, index=True)
    username = Column(String(100))

    age = Column(Integer)
    weight = Column(String(50))

    goal = Column(String(100))
    intensity = Column(String(50))

    workout_plan = Column(Text)
    updated_plan = Column(Text)

    nutrition_tip = Column(Text)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


Base.metadata.create_all(bind=engine)