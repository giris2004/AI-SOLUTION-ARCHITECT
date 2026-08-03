import os
import json
import logging
from datetime import datetime, timezone
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from backend.config import get_settings
from models.project import Project
from models.recommendation import Recommendation

logger = logging.getLogger("ai_solution_architect")

class ReportService:
    """
    Service responsible for building professional PDF reports from architecture recommendations.
    """

    @classmethod
    async def generate_pdf_report(cls, project: Project, rec: Recommendation) -> str:
        """
        Generates an executive PDF report and saves it to the disk.
        Returns the absolute filepath of the generated PDF.
        """
        settings = get_settings()
        
        # Ensure output folder exists
        output_dir = os.path.abspath(settings.PDF_OUTPUT_DIR)
        os.makedirs(output_dir, exist_ok=True)
        
        filename = f"architecture_report_{project.id}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
        filepath = os.path.join(output_dir, filename)

        logger.info(f"Rendering executive PDF report for project ID {project.id} to: {filepath}...")
        
        doc = SimpleDocTemplate(
            filepath,
            pagesize=letter,
            rightMargin=54,
            leftMargin=54,
            topMargin=54,
            bottomMargin=54
        )

        styles = getSampleStyleSheet()
        
        # Custom Style Definitions
        title_style = ParagraphStyle(
            name="DocTitle",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=24,
            leading=28,
            textColor=colors.HexColor("#0F172A"),
            spaceAfter=15
        )
        
        subtitle_style = ParagraphStyle(
            name="DocSubTitle",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=12,
            leading=16,
            textColor=colors.HexColor("#64748B"),
            spaceAfter=30
        )

        h1_style = ParagraphStyle(
            name="SectionHeading",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=16,
            leading=20,
            textColor=colors.HexColor("#1E3A8A"),
            spaceBefore=18,
            spaceAfter=10,
            keepWithNext=True
        )

        body_style = ParagraphStyle(
            name="DocBody",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=10,
            leading=14,
            textColor=colors.HexColor("#334155"),
            spaceAfter=8
        )

        code_style = ParagraphStyle(
            name="DocCode",
            parent=styles["Normal"],
            fontName="Courier",
            fontSize=9,
            leading=11,
            textColor=colors.HexColor("#0F172A"),
            backColor=colors.HexColor("#F8FAFC"),
            borderColor=colors.HexColor("#E2E8F0"),
            borderWidth=1,
            borderPadding=8,
            spaceAfter=10
        )

        story = []

        # Cover / Header Banner
        story.append(Paragraph("AI Solution Architect", title_style))
        story.append(Paragraph(f"Enterprise Architecture Recommendation Report: {project.name}", subtitle_style))
        story.append(Spacer(1, 10))

        # Metadata Table
        meta_data = [
            [Paragraph("<b>Project Parameter</b>", body_style), Paragraph("<b>User Requirement Value</b>", body_style)],
            [Paragraph("Project Domain", body_style), Paragraph(project.domain, body_style)],
            [Paragraph("Target Platform", body_style), Paragraph(project.target_platform, body_style)],
            [Paragraph("Expected Active Users", body_style), Paragraph(str(project.expected_users), body_style)],
            [Paragraph("Expected Traffic", body_style), Paragraph(project.expected_traffic, body_style)],
            [Paragraph("Security Sizing Level", body_style), Paragraph(project.security_level, body_style)],
            [Paragraph("Availability Standard", body_style), Paragraph(project.availability, body_style)],
            [Paragraph("Preferred Cloud Provider", body_style), Paragraph(project.preferred_cloud, body_style)],
            [Paragraph("Estimated Timeline Target", body_style), Paragraph(project.deadline or "Flexible", body_style)],
            [Paragraph("Allocated Budget Level", body_style), Paragraph(project.budget or "Flexible", body_style)]
        ]
        
        t = Table(meta_data, colWidths=[2.5 * inch, 4.0 * inch])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#F1F5F9")),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ]))
        story.append(t)
        story.append(Spacer(1, 20))

        # Project Summary
        story.append(Paragraph("Project Summary Description", h1_style))
        story.append(Paragraph(project.description, body_style))
        story.append(Spacer(1, 15))

        # Recommended Tech Stack
        story.append(Paragraph("Proposed Technology Architecture Stack", h1_style))
        tech_data = [
            [Paragraph("<b>Domain Segment</b>", body_style), Paragraph("<b>Recommended Component</b>", body_style)],
            [Paragraph("Architecture Pattern", body_style), Paragraph(rec.architecture_pattern, body_style)],
            [Paragraph("Frontend Technology", body_style), Paragraph(rec.frontend_tech, body_style)],
            [Paragraph("Backend Technology", body_style), Paragraph(rec.backend_tech, body_style)],
            [Paragraph("Database Engine", body_style), Paragraph(rec.database_tech, body_style)],
            [Paragraph("Authentication Provider", body_style), Paragraph(rec.auth_tech, body_style)],
            [Paragraph("Cloud Platform Partner", body_style), Paragraph(rec.cloud_platform, body_style)],
            [Paragraph("Containerization & Hosting", body_style), Paragraph(rec.deployment_strategy, body_style)],
            [Paragraph("DevOps Frameworks", body_style), Paragraph(rec.devops_tools, body_style)],
            [Paragraph("CI/CD Pipeline Engine", body_style), Paragraph(rec.cicd_pipeline, body_style)]
        ]
        t_tech = Table(tech_data, colWidths=[2.5 * inch, 4.0 * inch])
        t_tech.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1E3A8A")),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#94A3B8")),
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ]))
        story.append(t_tech)
        story.append(Spacer(1, 15))

        # Executive Summary
        story.append(Paragraph("Architectural Summary Reasoning", h1_style))
        story.append(Paragraph(rec.summary, body_style))
        
        story.append(PageBreak())

        # Alternative Justification & Comparison
        story.append(Paragraph("Alternative Component Comparisons", h1_style))
        try:
            comparisons = json.loads(rec.comparison_data)
            for comp in comparisons:
                story.append(Paragraph(f"<b>Segment: {comp.get('technology_type', 'System Component').capitalize()}</b>", body_style))
                story.append(Paragraph(f"Justification: {comp.get('justification', '')}", body_style))
                story.append(Spacer(1, 5))
        except Exception:
            story.append(Paragraph(rec.comparison_data, body_style))
        story.append(Spacer(1, 15))

        # Cost Estimation Table
        story.append(Paragraph("Estimated Monthly Cloud Infrastructure Sizing Cost", h1_style))
        try:
            cost = json.loads(rec.cost_estimation_data)
            cost_rows = [
                [Paragraph("<b>Infrastructure Resource</b>", body_style), Paragraph("<b>Usage Description</b>", body_style), Paragraph("<b>Cost/Month</b>", body_style)]
            ]
            for key, val in cost.items():
                if key == "total_monthly_cost":
                    continue
                cost_rows.append([
                    Paragraph(key.capitalize(), body_style),
                    Paragraph(val.get("description", ""), body_style),
                    Paragraph(f"${val.get('monthly_cost', 0.0):.2f}", body_style)
                ])
            cost_rows.append([
                Paragraph("<b>Total Estimated Infrastructure Budget</b>", body_style),
                Paragraph("", body_style),
                Paragraph(f"<b>${cost.get('total_monthly_cost', 0.0):.2f} / month</b>", body_style)
            ])
            t_cost = Table(cost_rows, colWidths=[2.0 * inch, 3.5 * inch, 1.0 * inch])
            t_cost.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#F1F5F9")),
                ('ALIGN', (0,0), (-1,-1), 'LEFT'),
                ('LINEBELOW', (0,-1), (-1,-1), 1.5, colors.HexColor("#1E3A8A")),
                ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
                ('TOPPADDING', (0,0), (-1,-1), 6),
                ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ]))
            story.append(t_cost)
        except Exception:
            story.append(Paragraph(rec.cost_estimation_data, body_style))
        story.append(Spacer(1, 15))

        story.append(PageBreak())

        # Timeline Generator Table
        story.append(Paragraph("Project Implementation Milestone Timeline", h1_style))
        try:
            timeline_items = json.loads(rec.timeline_data)
            time_rows = [
                [Paragraph("<b>Timeline / Milestone</b>", body_style), Paragraph("<b>Planned Actionable Deliverables</b>", body_style)]
            ]
            for step in timeline_items:
                deliv_list = "<br/>".join([f"• {d}" for d in step.get("deliverables", [])])
                time_rows.append([
                    Paragraph(f"<b>Week {step.get('week', '')}: {step.get('milestone', '')}</b>", body_style),
                    Paragraph(deliv_list, body_style)
                ])
            t_time = Table(time_rows, colWidths=[2.5 * inch, 4.0 * inch])
            t_time.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#F1F5F9")),
                ('ALIGN', (0,0), (-1,-1), 'LEFT'),
                ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
                ('TOPPADDING', (0,0), (-1,-1), 6),
                ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ]))
            story.append(t_time)
        except Exception:
            story.append(Paragraph(rec.timeline_data, body_style))
        story.append(Spacer(1, 15))

        # Risk Analysis Table
        story.append(Paragraph("System Risk Register & Mitigation Strategy", h1_style))
        try:
            risks = json.loads(rec.risk_analysis_data)
            risk_rows = [
                [Paragraph("<b>Risk Segment</b>", body_style), Paragraph("<b>Severity</b>", body_style), Paragraph("<b>Mitigation Countermeasure</b>", body_style)]
            ]
            for risk in risks:
                risk_rows.append([
                    Paragraph(f"<b>{risk.get('risk_type', '')}</b><br/>{risk.get('description', '')}", body_style),
                    Paragraph(risk.get("impact", ""), body_style),
                    Paragraph(risk.get("mitigation", ""), body_style)
                ])
            t_risk = Table(risk_rows, colWidths=[2.5 * inch, 1.0 * inch, 3.0 * inch])
            t_risk.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#F1F5F9")),
                ('ALIGN', (0,0), (-1,-1), 'LEFT'),
                ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
                ('TOPPADDING', (0,0), (-1,-1), 6),
                ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ]))
            story.append(t_risk)
        except Exception:
            story.append(Paragraph(rec.risk_analysis_data, body_style))
        story.append(Spacer(1, 15))

        # Diagram Code Block
        story.append(Paragraph("System Architecture Diagrams (Mermaid Script Code)", h1_style))
        story.append(Paragraph(rec.diagram_mermaid.replace("\n", "<br/>"), code_style))

        # Build Document
        doc.build(story)
        logger.info(f"PDF document generated successfully at path: {filepath}")
        return filepath
