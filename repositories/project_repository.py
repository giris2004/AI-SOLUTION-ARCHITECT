from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.project import Project

class ProjectRepository:
    """
    Data Access Object (DAO) for Project entities.
    """

    @staticmethod
    async def create_project(db: AsyncSession, project: Project) -> Project:
        """
        Persists a new project requirement intake record in the database.
        """
        db.add(project)
        await db.flush()
        await db.refresh(project)
        return project

    @staticmethod
    async def get_project_by_id(db: AsyncSession, project_id: int) -> Optional[Project]:
        """
        Queries a single project by its primary key ID.
        """
        result = await db.execute(select(Project).where(Project.id == project_id))
        return result.scalars().first()

    @staticmethod
    async def get_projects_by_user(db: AsyncSession, owner_id: int) -> List[Project]:
        """
        Queries all projects matching a specific owner ID.
        """
        result = await db.execute(
            select(Project)
            .where(Project.owner_id == owner_id)
            .order_by(Project.created_at.desc())
        )
        return list(result.scalars().all())

    @staticmethod
    async def delete_project(db: AsyncSession, project: Project) -> None:
        """
        Deletes a project record from the database.
        """
        await db.delete(project)
        await db.flush()
