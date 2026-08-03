import os
import json
import logging
from typing import Dict, Any
from google import genai
from google.genai.errors import APIError
from backend.config import get_settings
from prompts.templates import SYSTEM_PROMPT, PROJECT_ANALYSIS_PROMPT_TEMPLATE

logger = logging.getLogger("ai_solution_architect")

class GeminiService:
    """
    Service responsible for interacting with the Google Gemini API or generating mock recommendations.
    """

    @classmethod
    async def generate_architecture_recommendation(cls, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generates structured software architecture recommendations based on project data.
        Tries to call Google Gemini API; falls back to mock recommendations if keys are missing or API fails.
        """
        settings = get_settings()
        api_key = settings.GEMINI_API_KEY or os.getenv("GEMINI_API_KEY")
        
        prompt_text = PROJECT_ANALYSIS_PROMPT_TEMPLATE.format(
            name=project_data.get("name", "Unnamed Project"),
            domain=project_data.get("domain", "General"),
            target_platform=project_data.get("target_platform", "Web App"),
            expected_users=project_data.get("expected_users", 100),
            expected_traffic=project_data.get("expected_traffic", "Low"),
            preferred_cloud=project_data.get("preferred_cloud", "Any"),
            team_size=project_data.get("team_size", 3),
            budget=project_data.get("budget", "Limited"),
            deadline=project_data.get("deadline", "Flexible"),
            required_features=project_data.get("required_features", "Standard web pages"),
            availability=project_data.get("availability", "99.9%"),
            scalability=project_data.get("scalability", "Medium"),
            security_level=project_data.get("security_level", "Standard"),
            third_party_integrations=project_data.get("third_party_integrations", "None") or "None",
            description=project_data.get("description", "No description provided.")
        )

        if api_key and api_key != "your_google_gemini_api_key_here" and len(api_key.strip()) > 10:
            try:
                logger.info(f"Invoking Google Gemini API model: {settings.GEMINI_MODEL}...")
                client = genai.Client(api_key=api_key)
                
                # Call Gemini model
                response = client.models.generate_content(
                    model=settings.GEMINI_MODEL,
                    contents=prompt_text,
                    config={
                        "system_instruction": SYSTEM_PROMPT,
                        "response_mime_type": "application/json",
                        "temperature": 0.2
                    }
                )
                
                # Parse and validate JSON output
                json_payload = json.loads(response.text)
                logger.info("Successfully fetched and parsed Gemini AI recommendations.")
                return json_payload
                
            except APIError as ae:
                logger.error(f"Gemini API returned an error: {str(ae)}. Falling back to local Recommendation Engine.")
            except Exception as e:
                logger.error(f"Failed to generate architecture via Gemini API: {str(e)}. Falling back to local Recommendation Engine.")
        else:
            logger.warning("Google Gemini API Key is missing or invalid. Utilizing local Recommendation Engine.")

        # Trigger Mock Engine
        return cls._generate_mock_recommendation(project_data)

    @classmethod
    def _generate_mock_recommendation(cls, project: Dict[str, Any]) -> Dict[str, Any]:
        """
        Fallback recommendation engine returning customized and valid software architecture structures.
        """
        name = project.get("name", "Enterprise System")
        domain = project.get("domain", "SaaS").lower()
        cloud = project.get("preferred_cloud", "AWS")
        if cloud == "Any" or not cloud:
            cloud = "AWS"

        # Determine architecture pattern based on expected traffic
        traffic = project.get("expected_traffic", "Low").lower()
        users = int(project.get("expected_users", 100))
        
        if traffic == "high" or users >= 100000:
            pattern = "Event-Driven Microservices"
            backend = "FastAPI + Go (gRPC Services)"
            database = "PostgreSQL (RDS) + Redis Cache + MongoDB"
            deployment = "Docker on Kubernetes (EKS)"
            devops = "Terraform, Prometheus, Grafana, ELK Stack"
            cicd = "GitHub Actions with AWS ECR & EKS Helm deployment"
        elif "finance" in domain or "health" in domain:
            pattern = "Layered Clean Architecture (SOA)"
            backend = "FastAPI + Spring Boot (Secure Core)"
            database = "PostgreSQL with multi-AZ replication"
            deployment = "AWS ECS Fargate"
            devops = "Terraform, AWS CloudWatch, Datadog"
            cicd = "GitHub Actions with AWS CodeDeploy"
        else:
            pattern = "MVC Monolithic / Modular Monolith"
            backend = "FastAPI"
            database = "PostgreSQL"
            deployment = "AWS App Runner"
            devops = "Docker, AWS CloudWatch"
            cicd = "GitHub Actions"

        # Formulate Mermaid flowchart
        mermaid = f"""flowchart TD
    User["Client Browser (React 19)"] --> CDN["CloudFront CDN"]
    CDN --> LB["Application Load Balancer"]
    LB --> Backend["FastAPI Backend ({backend})"]
    Backend --> DB[("PostgreSQL DB ({database})")]
    Backend --> Cache[("Redis Cache")]
    Backend --> Auth["JWT Auth Guard"]
    Backend --> Cloud["{cloud} Cloud Environment"]
"""

        # Alternatives
        alternatives = [
            {
                "technology_type": "backend",
                "option_1": {"name": "FastAPI (Python)", "performance": "High", "scalability": "High", "learning_curve": "Easy", "cost": "Low", "community": "Strong", "security": "High", "maintainability": "High", "is_chosen": True},
                "option_2": {"name": "Express.js (Node.js)", "performance": "High", "scalability": "Medium", "learning_curve": "Easy", "cost": "Low", "community": "Strong", "security": "Medium", "maintainability": "Medium", "is_chosen": False},
                "option_3": {"name": "Spring Boot (Java)", "performance": "High", "scalability": "High", "learning_curve": "Moderate", "cost": "Medium", "community": "Strong", "security": "High", "maintainability": "High", "is_chosen": False},
                "justification": f"FastAPI was selected for {name} to optimize REST execution performance using asynchronous event routing. While Node.js offers fast bootstrapping, FastAPI provides auto-generated OpenAPI documentation and native Python schema validations which ease integrations. Spring Boot is too heavyweight for the requested scope."
            },
            {
                "technology_type": "database",
                "option_1": {"name": "PostgreSQL", "performance": "High", "scalability": "High", "learning_curve": "Easy", "cost": "Low", "community": "Strong", "security": "High", "maintainability": "High", "is_chosen": True},
                "option_2": {"name": "MySQL", "performance": "High", "scalability": "Medium", "learning_curve": "Easy", "cost": "Low", "community": "Strong", "security": "Medium", "maintainability": "High", "is_chosen": False},
                "option_3": {"name": "MongoDB (NoSQL)", "performance": "Very High", "scalability": "High", "learning_curve": "Easy", "cost": "Medium", "community": "Strong", "security": "Medium", "maintainability": "Medium", "is_chosen": False},
                "justification": f"PostgreSQL is chosen for {name} because it handles structured relational integrity, offers JSONB semi-structured storage support, and matches ACID compliance standards necessary for the {domain} domain."
            }
        ]

        # Sprints
        sprints = [
            {"sprint": "Sprint 1", "goal": "Initialize core auth, environment scaffolding, and database tables.", "backlog": ["Database schema setup", "API register & login endpoints integration", "Frontend landing page implementation"]},
            {"sprint": "Sprint 2", "goal": "Implement primary domain features and backend controllers.", "backlog": ["Project intake forms UI", "FastAPI CRUD requirement routing", "Integration with recommendation logic"]},
            {"sprint": "Sprint 3", "goal": "AI Core recommendation mapping and cost estimators.", "backlog": ["Gemini prompts service", "Mermaid visualizer container", "Timeline generator workflow"]},
            {"sprint": "Sprint 4", "goal": "Document exports, testing, and production builds.", "backlog": ["ReportLab PDF export service", "E2E testing suite", "Docker compose environment launch"]}
        ]

        # Timeline
        timeline = [
            {"week": 1, "milestone": "System Initialization", "deliverables": ["CI/CD pipelines set up", "Auth views built", "API endpoints running"]},
            {"week": 2, "milestone": "Core Domain Scaffolding", "deliverables": ["Requirement capture intake forms", "Database migrations mapping", "Service interfaces defined"]},
            {"week": 3, "milestone": "Recommendation engine integrations", "deliverables": ["Gemini AI parser integration", "Mermaid diagrams engine", "Cost estimator setup"]},
            {"week": 4, "milestone": "PDF reports & Deployment", "deliverables": ["ReportLab PDF renderer", "Docker compose packaging", "UAT validation complete"]}
        ]

        # Cost Analysis
        api_inference_cost = 10.0 if traffic == "low" else 35.0
        server_resource_cost = 15.0 if traffic == "low" else 75.0
        db_resource_cost = 15.0 if traffic == "low" else 60.0
        storage_resource_cost = 5.0
        api_ingress_cost = 10.0
        hosting_cdn_cost = 10.0
        total = api_inference_cost + server_resource_cost + db_resource_cost + storage_resource_cost + api_ingress_cost + hosting_cdn_cost

        cost = {
            "server": {"description": f"Compute resources: App runner instance size (vCPU/RAM) on {cloud}", "monthly_cost": server_resource_cost},
            "database": {"description": f"Managed DB Instance sizing with automatic daily backups on {cloud}", "monthly_cost": db_resource_cost},
            "storage": {"description": "Static media asserts and PDF document storage buckets", "monthly_cost": storage_resource_cost},
            "api": {"description": "Ingress/Egress data charges and DNS configuration hosting", "monthly_cost": api_ingress_cost},
            "ai": {"description": "Estimated Gemini API tokens usage model analysis billing", "monthly_cost": api_inference_cost},
            "hosting": {"description": "Static web pages CDN hosting and TLS certificates", "monthly_cost": hosting_cdn_cost},
            "total_monthly_cost": total
        }

        # Risks
        risks = [
            {"risk_type": "Technical", "description": "High memory footprint during large PDF compilations.", "impact": "Medium", "mitigation": "Offload PDF operations to background task processes and buffer files during rendering."},
            {"risk_type": "Security", "description": "Exposure of Gemini API calls keys in developer code environments.", "impact": "High", "mitigation": "Enforce loading secrets strictly via environment variables, not code files."},
            {"risk_type": "Budget", "description": "Spike in API token costs due to high user request volumes.", "impact": "High", "mitigation": "Integrate local Redis caching of identical inputs to skip API calls."}
        ]

        return {
            "architecture_pattern": pattern,
            "frontend_tech": "React 19 (Vite + Tailwind CSS)",
            "backend_tech": backend,
            "database_tech": database,
            "auth_tech": "JWT Bearer Tokens (HS256)",
            "cloud_platform": cloud,
            "deployment_strategy": deployment,
            "devops_tools": devops,
            "cicd_pipeline": cicd,
            "comparison_data": alternatives,
            "cost_estimation_data": cost,
            "timeline_data": timeline,
            "sprint_plan_data": sprints,
            "risk_analysis_data": risks,
            "diagram_mermaid": mermaid,
            "summary": f"This software architecture utilizes a modular, {pattern} pattern tailored to scale {name} effectively across the {cloud} cloud framework. By coupling a reactive {backend} backend with PostgreSQL, we ensure structured consistency, high concurrency, and compliance with {project.get('security_level', 'Standard')} security constraints."
        }
