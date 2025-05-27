#!/usr/bin/env python3
"""
Script to fix workspace directory structure for agent file operations
"""

import os
import sys
sys.path.append('/app')

def create_workspace_structure():
    """Create proper workspace directory structure"""
    try:
        from superagi.models.db import connect_db
        from superagi.models.agent_execution import AgentExecution
        from superagi.models.agent import Agent
        from sqlalchemy.orm import sessionmaker
        from superagi.helper.resource_helper import ResourceHelper

        print("🔧 Setting up workspace directory structure...")
        
        engine = connect_db()
        Session = sessionmaker(bind=engine)
        session = Session()

        try:
            # Get all agent executions
            executions = session.query(AgentExecution).all()
            
            for execution in executions:
                agent = session.query(Agent).filter(Agent.id == execution.agent_id).first()
                if agent:
                    # Get the resource path for this execution
                    resource_path = ResourceHelper.get_agent_write_resource_path("", agent, execution)
                    
                    # Create common project directories
                    directories_to_create = [
                        os.path.join(resource_path, "src"),
                        os.path.join(resource_path, "tests"),
                        os.path.join(resource_path, "docs"),
                        os.path.join(resource_path, "assets"),
                        os.path.join(resource_path, "config"),
                        os.path.join(resource_path, "scripts"),
                        os.path.join(resource_path, "lib"),
                        os.path.join(resource_path, "bin"),
                        os.path.join(resource_path, "examples")
                    ]
                    
                    for directory in directories_to_create:
                        try:
                            os.makedirs(directory, exist_ok=True)
                            print(f"✅ Created directory: {directory}")
                        except Exception as e:
                            print(f"⚠️  Could not create {directory}: {e}")
                            
            # Also create structure for future executions
            base_workspace = "/app/workspace"
            template_dirs = [
                os.path.join(base_workspace, "template", "src"),
                os.path.join(base_workspace, "template", "tests"),
                os.path.join(base_workspace, "template", "docs"),
                os.path.join(base_workspace, "template", "assets"),
                os.path.join(base_workspace, "template", "config"),
                os.path.join(base_workspace, "template", "scripts"),
                os.path.join(base_workspace, "template", "lib"),
                os.path.join(base_workspace, "template", "bin"),
                os.path.join(base_workspace, "template", "examples")
            ]
            
            for directory in template_dirs:
                try:
                    os.makedirs(directory, exist_ok=True)
                    print(f"✅ Created template directory: {directory}")
                except Exception as e:
                    print(f"⚠️  Could not create template {directory}: {e}")
                    
        except Exception as e:
            print(f"❌ Error setting up workspace structure: {str(e)}")
            import traceback
            traceback.print_exc()
        finally:
            session.close()
            
    except Exception as e:
        print(f"❌ Database connection error: {str(e)}")
        import traceback
        traceback.print_exc()

def fix_existing_executions():
    """Fix existing agent execution directories"""
    workspace_base = "/app/workspace/output"
    
    if os.path.exists(workspace_base):
        for agent_dir in os.listdir(workspace_base):
            agent_path = os.path.join(workspace_base, agent_dir)
            if os.path.isdir(agent_path):
                for execution_dir in os.listdir(agent_path):
                    execution_path = os.path.join(agent_path, execution_dir)
                    if os.path.isdir(execution_path):
                        # Create src directory if it doesn't exist
                        src_dir = os.path.join(execution_path, "src")
                        if not os.path.exists(src_dir):
                            os.makedirs(src_dir, exist_ok=True)
                            print(f"✅ Created src directory: {src_dir}")
                            
                        # Move main.rs to src/ if it exists in root
                        main_rs_root = os.path.join(execution_path, "main.rs")
                        main_rs_src = os.path.join(src_dir, "main.rs")
                        
                        if os.path.exists(main_rs_root) and not os.path.exists(main_rs_src):
                            try:
                                import shutil
                                shutil.move(main_rs_root, main_rs_src)
                                print(f"✅ Moved main.rs to src/: {main_rs_src}")
                            except Exception as e:
                                print(f"⚠️  Could not move main.rs: {e}")

if __name__ == "__main__":
    print("🚀 SuperAGI Workspace Structure Fix")
    print("=" * 40)
    create_workspace_structure()
    print()
    print("🔧 Fixing existing execution directories...")
    fix_existing_executions()
    print()
    print("🎉 Workspace structure setup complete!")
    print("📋 Benefits:")
    print("1. Agents can now write to src/, tests/, docs/, etc.")
    print("2. Proper project structure for code generation")
    print("3. Better organization of generated files")
