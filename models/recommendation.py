from typing import TYPE_CHECKING
from sqlalchemy import Integer, String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.base import Base, TimestampMixin

if TYPE_CHECKING:
    from models.project import Project

class Recommendation(Base, TimestampMixin):
    """
    SQLAlchemy ORM model representing structured AI architecture recommendations and comparative metadata.
    """
    __tablename__ = "recommendations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    project_id: Mapped[int] = mapped_column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)

    # Core AI Recommendations
    architecture_pattern: Mapped[str] = mapped_column(String(255), nullable=False)
    frontend_tech: Mapped[str] = mapped_column(String(255), nullable=False)
    backend_tech: Mapped[str] = mapped_column(String(255), nullable=False)
    database_tech: Mapped[str] = mapped_column(String(255), nullable=False)
    auth_tech: Mapped[str] = mapped_column(String(255), nullable=False)
    cloud_platform: Mapped[str] = mapped_column(String(255), nullable=False)
    deployment_strategy: Mapped[str] = mapped_column(String(255), nullable=False)
    devops_tools: Mapped[str] = mapped_column(String(255), nullable=False)
    cicd_pipeline: Mapped[str] = mapped_column(String(255), nullable=False)

    # Advanced Analysis Payload (JSON Strings)
    comparison_data: Mapped[str] = mapped_column(Text, nullable=False)
    cost_estimation_data: Mapped[str] = mapped_column(Text, nullable=False)
    timeline_data: Mapped[str] = mapped_column(Text, nullable=False)
    sprint_plan_data: Mapped[str] = mapped_column(Text, nullable=False)
    risk_analysis_data: Mapped[str] = mapped_column(Text, nullable=False)

    # Visualizations & Summaries
    diagram_mermaid: Mapped[str] = mapped_column(Text, nullable=False)
    diagram_drawio: Mapped[str] = mapped_column(Text, nullable=True)
    summary: Mapped[str] = mapped_column(Text, nullable=False)

    # Relationships
    project: Mapped["Project"] = relationship("Project", back_populates="recommendations")

    def __repr__(self) -> str:
        return f"<Recommendation(id={self.id}, project_id={self.project_id}, pattern='{self.architecture_pattern}')>"
