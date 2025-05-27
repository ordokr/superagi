#!/usr/bin/env python3
"""
Test script to verify file writing works correctly with directory creation
"""

import sys
import os
sys.path.append('/app')

def test_file_writing():
    """Test file writing with directory creation"""
    try:
        from superagi.resource_manager.file_manager import FileManager
        from superagi.models.db import connect_db
        from superagi.models.agent import Agent
        from superagi.models.agent_execution import AgentExecution
        from sqlalchemy.orm import sessionmaker

        print("🧪 Testing file writing with directory creation...")
        
        engine = connect_db()
        Session = sessionmaker(bind=engine)
        session = Session()

        try:
            # Get the latest agent execution
            execution = session.query(AgentExecution).order_by(AgentExecution.id.desc()).first()
            if not execution:
                print("❌ No agent execution found")
                return
                
            agent = session.query(Agent).filter(Agent.id == execution.agent_id).first()
            if not agent:
                print("❌ No agent found")
                return
                
            print(f"✅ Using agent: {agent.name} (ID: {agent.id})")
            print(f"✅ Using execution: {execution.name} (ID: {execution.id})")
            
            # Create file manager
            file_manager = FileManager(session, agent.id, execution.id)
            
            # Test writing files to various directories
            test_files = [
                ("src/main.rs", "fn main() {\n    println!(\"Hello, World!\");\n}"),
                ("src/lib.rs", "pub mod utils;\n"),
                ("tests/integration_test.rs", "#[test]\nfn test_basic() {\n    assert_eq!(2 + 2, 4);\n}"),
                ("docs/README.md", "# Project Documentation\n\nThis is a test project."),
                ("config/settings.toml", "[app]\nname = \"test-app\"\nversion = \"1.0.0\""),
                ("scripts/build.sh", "#!/bin/bash\necho \"Building project...\"\ncargo build"),
                ("assets/style.css", "body { font-family: Arial, sans-serif; }"),
                ("examples/example.rs", "fn main() {\n    println!(\"Example code\");\n}")
            ]
            
            for file_path, content in test_files:
                result = file_manager.write_file(file_path, content)
                print(f"📝 {file_path}: {result}")
                
            print("\n🔍 Verifying created files...")
            
            # Check if files were created
            from superagi.helper.resource_helper import ResourceHelper
            base_path = ResourceHelper.get_agent_write_resource_path("", agent, execution)
            
            for file_path, _ in test_files:
                full_path = os.path.join(base_path, file_path)
                if os.path.exists(full_path):
                    print(f"✅ {file_path} - Created successfully")
                else:
                    print(f"❌ {file_path} - Not found")
                    
            print(f"\n📁 Files created in: {base_path}")
            
        except Exception as e:
            print(f"❌ Error testing file writing: {str(e)}")
            import traceback
            traceback.print_exc()
        finally:
            session.close()
            
    except Exception as e:
        print(f"❌ Database connection error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🚀 SuperAGI File Writing Test")
    print("=" * 40)
    test_file_writing()
    print()
    print("🎉 File writing test complete!")
    print("📋 This test verifies that:")
    print("1. Directories are created automatically")
    print("2. Files can be written to subdirectories")
    print("3. Proper project structure is maintained")
