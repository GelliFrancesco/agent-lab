from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime
import enum

Base = declarative_base()

class Difficulty(enum.Enum):
    EASY = "Easy"
    MEDIUM = "Medium"
    HARD = "Hard"

class Attempt(Base):
    __tablename__ = "attempts"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    problem_id = Column(Integer, ForeignKey("problems.id"))
    attempts_count = Column(Integer, default=0)
    time_minutes = Column(Integer, default=0)
    gave_up = Column(Boolean, default=False)
    solved = Column(Boolean, default=False)
    elo_before = Column(Integer)
    elo_after = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="attempts")
    problem = relationship("Problem", back_populates="attempts")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    username = Column(String(100), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    topic_elos = relationship("TopicElo", back_populates="user", cascade="all, delete-orphan")
    attempts = relationship("Attempt", back_populates="user", cascade="all, delete-orphan")

    def overall_elo(self):
        if not self.topic_elos:
            return 1200
        return sum(t.elo for t in self.topic_elos) / len(self.topic_elos)


class TopicElo(Base):
    __tablename__ = "topic_elos"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    topic = Column(String(50), nullable=False)
    elo = Column(Integer, default=1200)
    problems_solved = Column(Integer, default=0)
    problems_given_up = Column(Integer, default=0)

    user = relationship("User", back_populates="topic_elos")


class Problem(Base):
    __tablename__ = "problems"

    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    slug = Column(String(200), unique=True)
    difficulty = Column(Enum(Difficulty), nullable=False)
    topics = Column(String(500))  # comma-separated: "arrays,trees,dynamic-programming"
    companies = Column(String(500))  # comma-separated: "Google,Meta,Amazon"
    importance = Column(Integer, default=5)  # 1-10 how important/representative
    leetcode_number = Column(Integer)
    leetcode_url = Column(String(300))
    description = Column(Text)
    pattern_hint = Column(String(300))  # "sliding window", "two pointers", etc.
    created_at = Column(DateTime, default=datetime.utcnow)

    attempts = relationship("Attempt", back_populates="problem")
