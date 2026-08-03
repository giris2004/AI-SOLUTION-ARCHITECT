import os
from typing import Dict, Any
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import FileResponse
from models.user import User
from routes.auth_routes import get_current_user
from services.gemini_service import GeminiService
from services.report_service import ReportService
from models.project import Project
from models.recommendation import Recommendation

router = APIRouter(prefix="/api/ai", tags=["AI Core Sandboxes"])

@router.post(
    "/recommend",
    status_code=status.HTTP_200_OK,
    summary="Generate architecture recommendations on-the-fly",
)
async def ai_recommend(
    data: Dict[str, Any],
    current_user: User = Depends(get_current_user),
):
    """
    Submits requirements form data and returns the full AI generated recommendation JSON payload directly.
    """
    return await GeminiService.generate_architecture_recommendation(data)

@router.post(
    "/compare",
    status_code=status.HTTP_200_OK,
    summary="Compare architecture technology stack options",
)
async def ai_compare(
    data: Dict[str, Any],
    current_user: User = Depends(get_current_user),
):
    """
    Analyzes project requirements and isolates the technology alternatives table and comparisons.
    """
    result = await GeminiService.generate_architecture_recommendation(data)
    return {
        "comparison_data": result.get("comparison_data", [])
    }

@router.post(
    "/cost",
    status_code=status.HTTP_200_OK,
    summary="Estimate hosting and subscription costs",
)
async def ai_cost(
    data: Dict[str, Any],
    current_user: User = Depends(get_current_user),
):
    """
    Analyzes requirements and isolates the estimated cloud resource cost sizing matrix.
    """
    result = await GeminiService.generate_architecture_recommendation(data)
    return {
        "cost_estimation_data": result.get("cost_estimation_data", {})
    }

@router.post(
    "/timeline",
    status_code=status.HTTP_200_OK,
    summary="Generate milestone timelines",
)
async def ai_timeline(
    data: Dict[str, Any],
    current_user: User = Depends(get_current_user),
):
    """
    Analyzes requirements and isolates the implementation deliverables timeline.
    """
    result = await GeminiService.generate_architecture_recommendation(data)
    return {
        "timeline_data": result.get("timeline_data", [])
    }

@router.post(
    "/risk",
    status_code=status.HTTP_200_OK,
    summary="Analyze architectural risks",
)
async def ai_risk(
    data: Dict[str, Any],
    current_user: User = Depends(get_current_user),
):
    """
    Analyzes requirements and isolates risk mitigation registries.
    """
    result = await GeminiService.generate_architecture_recommendation(data)
    return {
        "risk_analysis_data": result.get("risk_analysis_data", [])
    }

@router.post(
    "/pdf",
    status_code=status.HTTP_200_OK,
    summary="Generate PDF directly from structured payload data",
)
async def ai_pdf(
    payload: Dict[str, Any],
    current_user: User = Depends(get_current_user),
):
    """
    Takes a structured project description and its compiled recommendation properties,
    and returns a downloadable executive PDF report.
    """
    try:
        # Re-map temporary Project & Recommendation models (unsaved in database)
        proj_data = payload.get("project", {})
        rec_data = payload.get("recommendation", {})
        
        project = Project(
            id=9999,
            name=proj_data.get("name", "Transient Project"),
            description=proj_data.get("description", "Sandbox Analysis"),
            domain=proj_data.get("domain", "General"),
            expected_users=int(proj_data.get("expected_users", 0)),
            budget=proj_data.get("budget", "Flexible"),
            deadline=proj_data.get("deadline", "Flexible"),
            target_platform=proj_data.get("target_platform", "Web App"),
            required_features=proj_data.get("required_features", "Standard"),
            security_level=proj_data.get("security_level", "Standard"),
            scalability=proj_data.get("scalability", "Medium"),
            availability=proj_data.get("availability", "99.9%"),
            preferred_cloud=proj_data.get("preferred_cloud", "AWS"),
            expected_traffic=proj_data.get("expected_traffic", "Low"),
            third_party_integrations=proj_data.get("third_party_integrations", ""),
            owner_id=current_user.id
        )
        
        # Import dynamic lists to JSON strings
        import json
        recommendation = Recommendation(
            project_id=9999,
            architecture_pattern=rec_data.get("architecture_pattern", "Custom"),
            frontend_tech=rec_data.get("frontend_tech", "React"),
            backend_tech=rec_data.get("backend_tech", "FastAPI"),
            database_tech=rec_data.get("database_tech", "PostgreSQL"),
            auth_tech=rec_data.get("auth_tech", "JWT"),
            cloud_platform=rec_data.get("cloud_platform", "AWS"),
            deployment_strategy=rec_data.get("deployment_strategy", "Docker"),
            devops_tools=rec_data.get("devops_tools", "Terraform"),
            cicd_pipeline=rec_data.get("cicd_pipeline", "GitHub Actions"),
            comparison_data=json.dumps(rec_data.get("comparison_data", [])),
            cost_estimation_data=json.dumps(rec_data.get("cost_estimation_data", {})),
            timeline_data=json.dumps(rec_data.get("timeline_data", [])),
            sprint_plan_data=json.dumps(rec_data.get("sprint_plan_data", [])),
            risk_analysis_data=json.dumps(rec_data.get("risk_analysis_data", [])),
            diagram_mermaid=rec_data.get("diagram_mermaid", "graph TD;"),
            summary=rec_data.get("summary", "Summary Analysis")
        )
        
        filepath = await ReportService.generate_pdf_report(project, recommendation)
        if not os.path.exists(filepath):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="PDF generation failed"
            )
            
        return FileResponse(
            path=filepath,
            media_type="application/pdf",
            filename=os.path.basename(filepath)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate custom PDF: {str(e)}"
        )
