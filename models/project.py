from typing import TYPE_CHECKING, List, Optional
from sqlalchemy import Integer, String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.base import Base, TimestampMixin

if TYPE_CHECKING:
    from models.user import User
    from models.recommendation import Recommendation

class Project(Base, TimestampMixin):
    """
    SQLAlchemy ORM model representing user project architectures and intake form constraints.
    """
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    domain: Mapped[str] = mapped_column(String(100), nullable=False)
    expected_users: Mapped[int] = mapped_column(Integer, default=0)
    budget: Mapped[str] = mapped_column(String(100), nullable=True)
    deadline: Mapped[str] = mapped_column(String(100), nullable=True)
    team_size: Mapped[int] = mapped_column(Integer, default=1)
    target_platform: Mapped[str] = mapped_column(String(100), nullable=False)
    required_features: Mapped[str] = mapped_column(Text, nullable=False) # JSON or Comma-separated list
    security_level: Mapped[str] = mapped_column(String(50), default="Standard")
    scalability: Mapped[str] = mapped_column(String(50), default="Medium")
    availability: Mapped[str] = mapped_column(String(50), default="99.9%")
    preferred_cloud: Mapped[str] = mapped_column(String(50), default="Any")
    expected_traffic: Mapped[str] = mapped_column(String(100), default="Low")
    third_party_integrations: Mapped[str] = mapped_column(Text, nullable=True) # JSON or Text

    owner_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    # Relationships
    owner: Mapped["User"] = relationship("User", back_populates="projects")
    recommendations: Mapped[List["Recommendation"]] = relationship(
        "Recommendation", 
        back_populates="project", 
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Project(id={self.id}, name='{self.name}', owner_id={self.owner_id})>"
