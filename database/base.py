from datetime import datetime, timezone
from typing import Any, Dict
from sqlalchemy import DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    """
    Base class for all SQLAlchemy ORM models.
    """
    pass

class TimestampMixin:
    """
    Reusable ORM mixin providing creation and modification audit timestamps.
    """
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the ORM model attributes into a serializable dictionary.
        """
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }
