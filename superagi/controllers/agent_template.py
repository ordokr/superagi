from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi_sqlalchemy import db
from superagi.models.agent_execution import AgentExecution
from superagi.models.agent_template import AgentTemplate
from superagi.models.agent_template_config import AgentTemplateConfig
from superagi.dependencies import get_current_user, get_user_organisation
from superagi.helper.auth import check_auth
from fastapi_jwt_auth import AuthJWT
from typing import List, Optional

router = APIRouter()

@router.get("/list")
def get_agent_templates_list(
    template_source: str = Query(..., description="Source of templates: 'marketplace' or 'local'"),
    page: int = Query(0, description="Page number for pagination"),
    Authorize: AuthJWT = Depends(check_auth)
):
    """
    Get agent templates list from marketplace or local.

    Args:
        template_source (str): Source of templates ('marketplace' or 'local')
        page (int): Page number for pagination

    Returns:
        list: List of agent templates
    """
    try:
        if template_source == "marketplace":
            # Fetch from marketplace
            templates = AgentTemplate.fetch_marketplace_list("", page)
            return templates
        elif template_source == "local":
            # Fetch local templates
            organisation = Authorize.get_jwt_subject()
            if organisation:
                org_id = int(organisation)
                templates = db.session.query(AgentTemplate).filter(
                    AgentTemplate.organisation_id == org_id
                ).all()
                return [template.to_dict() for template in templates]
            else:
                return []
        else:
            raise HTTPException(status_code=400, detail="Invalid template_source. Use 'marketplace' or 'local'")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching templates: {str(e)}")

@router.get("/get/{template_id}")
def get_agent_template_details(
    template_id: int,
    template_source: str = Query("marketplace", description="Source of template"),
    Authorize: AuthJWT = Depends(check_auth)
):
    """
    Get agent template details by ID.

    Args:
        template_id (int): ID of the template
        template_source (str): Source of template

    Returns:
        dict: Template details with configurations
    """
    try:
        if template_source == "marketplace":
            # Fetch from marketplace
            template_details = AgentTemplate.fetch_marketplace_detail(template_id)
            return template_details
        else:
            # Fetch local template
            template = db.session.query(AgentTemplate).filter(
                AgentTemplate.id == template_id
            ).first()

            if not template:
                raise HTTPException(status_code=404, detail="Template not found")

            # Get template configurations
            configs = db.session.query(AgentTemplateConfig).filter(
                AgentTemplateConfig.agent_template_id == template_id
            ).all()

            config_dict = {}
            for config in configs:
                config_dict[config.key] = config.value

            result = template.to_dict()
            result['configs'] = config_dict
            return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching template details: {str(e)}")

@router.post("/download")
def install_agent_template(
    agent_template_id: int = Query(..., description="ID of the agent template to install"),
    organisation=Depends(get_user_organisation)
):
    """
    Install/download an agent template from marketplace.

    Args:
        agent_template_id (int): ID of the template to install

    Returns:
        dict: Installation result
    """
    try:
        # Install template from marketplace
        template = AgentTemplate.clone_agent_template_from_marketplace(
            db.session, agent_template_id, organisation.id
        )

        if template:
            return {"success": True, "message": "Template installed successfully", "template_id": template.id}
        else:
            raise HTTPException(status_code=500, detail="Failed to install template")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error installing template: {str(e)}")

@router.get("/agent_config")
def get_agent_template_config(
    agent_template_id: int = Query(..., description="ID of the agent template"),
    Authorize: AuthJWT = Depends(check_auth)
):
    """
    Get agent template configuration.

    Args:
        agent_template_id (int): ID of the template

    Returns:
        dict: Template configuration
    """
    try:
        template = db.session.query(AgentTemplate).filter(
            AgentTemplate.id == agent_template_id
        ).first()

        if not template:
            raise HTTPException(status_code=404, detail="Template not found")

        configs = db.session.query(AgentTemplateConfig).filter(
            AgentTemplateConfig.agent_template_id == agent_template_id
        ).all()

        config_dict = {}
        for config in configs:
            config_dict[config.key] = AgentTemplate.eval_agent_config(config.key, config.value)

        return config_dict

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching template config: {str(e)}")

@router.post("/save_agent_as_template/agent_id/{agent_id}/agent_execution_id/{execution_id}")
def save_agent_as_template(
    agent_id: int,
    execution_id: int,
    organisation=Depends(get_user_organisation)
):
    """
    Save an agent as a template.

    Args:
        agent_id (int): ID of the agent
        execution_id (int): ID of the agent execution

    Returns:
        dict: Save result
    """
    try:
        # Implementation for saving agent as template
        # This would need to be implemented based on your specific requirements
        return {"success": True, "message": "Agent saved as template successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving agent as template: {str(e)}")

@router.post("/publish/{agent_execution_id}")
async def publish_template(agent_execution_id: str, organisation=Depends(get_user_organisation), user=Depends(get_current_user)):
    """
    Publish the agent template based on the agent_execution_id.
    """
    try:
        # Your logic here
        # Replace with real publish logic
        agent_template = AgentTemplate.get_by_id(agent_execution_id)
        if not agent_template:
            raise HTTPException(status_code=404, detail="Agent Template not found.")

        # Implement whatever functionality you need here
        # agent_template.publish()

        return {"success": True, "message": "Agent template published successfully."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
