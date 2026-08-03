from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.recommendation import Recommendation

class RecommendationRepository:
    """
    Data Access Object (DAO) for Recommendation entities.
    """

    @staticmethod
    async def create_recommendation(db: AsyncSession, recommendation: Recommendation) -> Recommendation:
        """
        Persists a new AI recommendation record in the database.
        """
        db.add(recommendation)
        await db.flush()
        await db.refresh(recommendation)
        return recommendation

    @staticmethod
    async def get_recommendation_by_id(db: AsyncSession, rec_id: int) -> Optional[Recommendation]:
        """
        Queries a single recommendation by its primary key ID.
        """
        result = await db.execute(select(Recommendation).where(Recommendation.id == rec_id))
        return result.scalars().first()

    @staticmethod
    async def get_recommendation_by_project(db: AsyncSession, project_id: int) -> Optional[Recommendation]:
        """
        Queries a single recommendation matching a specific project ID.
        """
        result = await db.execute(select(Recommendation).where(Recommendation.project_id == project_id))
        return result.scalars().first()

    @staticmethod
    async def delete_recommendation(db: AsyncSession, recommendation: Recommendation) -> None:
        """
        Removes a recommendation record from the database.
        """
        await db.delete(recommendation)
        await db.flush()
