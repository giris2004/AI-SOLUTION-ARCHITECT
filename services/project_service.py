import json
import logging
from typing import Dict, Any, List, Optional
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from models.project import Project
from models.recommendation import Recommendation
from repositories.project_repository import ProjectRepository
from repositories.recommendation_repository import RecommendationRepository
from services.gemini_service import GeminiService
from services.report_service import ReportService

logger = logging.getLogger("ai_solution_architect")

class ProjectService:
    """
    Business logic coordinator for Project Requirement Forms, AI Recommendation pipelines,
    and PDF Briefing Exports.
    """

    @classmethod
    async def analyze_project_requirements(
        cls, db: AsyncSession, owner_id: int, data: Dict[str, Any]
    ) -> Recommendation:
        """
        Takes project constraints, stores intake model, triggers Gemini AI pipelines,
        and saves final recommendation schemas.
        """
        logger.info(f"Initiating architecture requirements analysis for project: {data.get('name')}")
        
        # 1. Instantiate and persist Project requirements
        project = Project(
            name=data.get("name"),
            description=data.get("description"),
            domain=data.get("domain"),
            expected_users=int(data.get("expected_users", 0)),
            budget=data.get("budget"),
            deadline=data.get("deadline"),
            team_size=int(data.get("team_size", 1)),
            target_platform=data.get("target_platform"),
            required_features=data.get("required_features"),
            security_level=data.get("security_level", "Standard"),
            scalability=data.get("scalability", "Medium"),
            availability=data.get("availability", "99.9%"),
            preferred_cloud=data.get("preferred_cloud", "Any"),
            expected_traffic=data.get("expected_traffic", "Low"),
            third_party_integrations=data.get("third_party_integrations", ""),
            owner_id=owner_id
        )

        project = await ProjectRepository.create_project(db, project)
        logger.info(f"Persisted project intake form record: ID={project.id}")

        # 2. Invoke Gemini AI Service
        rec_json = await GeminiService.generate_architecture_recommendation(data)

        # 3. Instantiate and persist Recommendation record
        recommendation = Recommendation(
            project_id=project.id,
            architecture_pattern=rec_json.get("architecture_pattern", "Modular N-Tier"),
            frontend_tech=rec_json.get("frontend_tech", "React SPA"),
            backend_tech=rec_json.get("backend_tech", "FastAPI"),
            database_tech=rec_json.get("database_tech", "PostgreSQL"),
            auth_tech=rec_json.get("auth_tech", "JWT Bearer Tokens"),
            cloud_platform=rec_json.get("cloud_platform", "AWS"),
            deployment_strategy=rec_json.get("deployment_strategy", "Docker Containers"),
            devops_tools=rec_json.get("devops_tools", "Docker Compose"),
            cicd_pipeline=rec_json.get("cicd_pipeline", "GitHub Actions"),
            comparison_data=json.dumps(rec_json.get("comparison_data", [])),
            cost_estimation_data=json.dumps(rec_json.get("cost_estimation_data", {})),
            timeline_data=json.dumps(rec_json.get("timeline_data", [])),
            sprint_plan_data=json.dumps(rec_json.get("sprint_plan_data", [])),
            risk_analysis_data=json.dumps(rec_json.get("risk_analysis_data", [])),
            diagram_mermaid=rec_json.get("diagram_mermaid", "graph TD; User-->Server"),
            diagram_drawio=rec_json.get("diagram_drawio", ""),
            summary=rec_json.get("summary", "System Architecture Blueprint")
        )

        recommendation = await RecommendationRepository.create_recommendation(db, recommendation)
        logger.info(f"Persisted AI recommendation report record: ID={recommendation.id}")
        return recommendation

    @classmethod
    async def get_project_by_id(cls, db: AsyncSession, project_id: int, user_id: int) -> Project:
        """
        Fetches project requirements checking access permissions.
        """
        project = await ProjectRepository.get_project_by_id(db, project_id)
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project requirement record not found."
            )
        if project.owner_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied to requested project record."
            )
        return project

    @classmethod
    async def get_recommendation_by_project(
        cls, db: AsyncSession, project_id: int, user_id: int
    ) -> Recommendation:
        """
        Retrieves generated architectural blueprints checking access permissions.
        """
        # Ensure project exists and belongs to active user session
        await cls.get_project_by_id(db, project_id, user_id)
        
        rec = await RecommendationRepository.get_recommendation_by_project(db, project_id)
        if not rec:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No recommendation report registered for this project."
            )
        return rec

    @classmethod
    async def get_user_projects_history(cls, db: AsyncSession, user_id: int) -> List[Dict[str, Any]]:
        """
        Queries all historical records created by user.
        """
        projects = await ProjectRepository.get_projects_by_user(db, user_id)
        history = []
        for p in projects:
            rec = await RecommendationRepository.get_recommendation_by_project(db, p.id)
            history.append({
                "project_id": p.id,
                "name": p.name,
                "domain": p.domain,
                "platform": p.target_platform,
                "created_at": p.created_at.isoformat(),
                "has_recommendation": rec is not None,
                "architecture_pattern": rec.architecture_pattern if rec else None
            })
        return history

    @classmethod
    async def delete_project(cls, db: AsyncSession, project_id: int, user_id: int) -> None:
        """
        Deletes project and cascade clears all attached recommendations.
        """
        project = await cls.get_project_by_id(db, project_id, user_id)
        await ProjectRepository.delete_project(db, project)
        logger.info(f"Deleted project ID {project_id} from database catalog.")

    @classmethod
    async def export_pdf_report(cls, db: AsyncSession, project_id: int, user_id: int) -> str:
        """
        Generates PDF documentation returns path.
        """
        project = await cls.get_project_by_id(db, project_id, user_id)
        rec = await cls.get_recommendation_by_project(db, project_id, user_id)
        
        filepath = await ReportService.generate_pdf_report(project, rec)
        return filepath
