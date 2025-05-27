#!/usr/bin/env python3
"""
Setup script to configure LM Studio provider and vector database for SuperAGI
"""

import sys
import os
sys.path.append('/home/tim/SuperAGI')

def setup_lm_studio_provider():
    """Add LM Studio as a model provider"""
    try:
        from superagi.models.db import connect_db
        from superagi.models.models_config import ModelsConfig
        from sqlalchemy.orm import sessionmaker

        print("🔧 Setting up LM Studio provider...")
        
        engine = connect_db()
        Session = sessionmaker(bind=engine)
        session = Session()

        try:
            # Add LM Studio provider for organization ID 1
            result = ModelsConfig.store_api_key(session, 1, 'LM Studio', 'EMPTY')
            print(f"✅ LM Studio provider added: {result}")
            
            # Verify it was added
            providers = session.query(ModelsConfig).filter(ModelsConfig.org_id == 1).all()
            print(f"📋 Current providers for org 1:")
            for provider in providers:
                print(f"   - {provider.provider} (ID: {provider.id})")
                
        except Exception as e:
            print(f"❌ Error adding LM Studio provider: {str(e)}")
        finally:
            session.close()
            
    except Exception as e:
        print(f"❌ Database connection error: {str(e)}")

def setup_vector_database():
    """Set up vector database configuration"""
    try:
        from superagi.models.db import connect_db
        from superagi.models.vector_dbs import VectorDbs
        from sqlalchemy.orm import sessionmaker

        print("🔧 Setting up Qdrant vector database...")
        
        engine = connect_db()
        Session = sessionmaker(bind=engine)
        session = Session()

        try:
            # Check if Qdrant vector DB already exists
            existing_vdb = session.query(VectorDbs).filter(
                VectorDbs.organisation_id == 1,
                VectorDbs.name == 'Qdrant'
            ).first()
            
            if existing_vdb:
                print("✅ Qdrant vector database already configured")
            else:
                # Add Qdrant vector database
                qdrant_config = VectorDbs(
                    name='Qdrant',
                    db_type='Qdrant',
                    organisation_id=1,
                    config={
                        'url': 'http://super__qdrant:6333',
                        'api_key': '',
                        'collection_name': 'superagi_collection'
                    }
                )
                session.add(qdrant_config)
                session.commit()
                print("✅ Qdrant vector database added successfully")
                
            # List all vector databases
            vector_dbs = session.query(VectorDbs).filter(VectorDbs.organisation_id == 1).all()
            print(f"📋 Current vector databases for org 1:")
            for vdb in vector_dbs:
                print(f"   - {vdb.name} ({vdb.db_type}) - ID: {vdb.id}")
                
        except Exception as e:
            print(f"❌ Error setting up vector database: {str(e)}")
        finally:
            session.close()
            
    except Exception as e:
        print(f"❌ Database connection error: {str(e)}")

def test_lm_studio_connection():
    """Test LM Studio connection"""
    try:
        from superagi.llms.lm_studio import LMStudio
        
        print("🔍 Testing LM Studio connection...")
        
        lm_studio = LMStudio(
            api_key='EMPTY',
            end_point='http://192.168.0.144:1234'
        )
        
        # Test connection
        models = lm_studio.get_models()
        print(f"✅ LM Studio connection successful!")
        print(f"📋 Available models: {models}")
        
    except Exception as e:
        print(f"❌ LM Studio connection failed: {str(e)}")

def main():
    print("🚀 SuperAGI Provider Setup Script")
    print("=" * 50)
    
    # Setup LM Studio provider
    setup_lm_studio_provider()
    print()
    
    # Setup vector database
    setup_vector_database()
    print()
    
    # Test LM Studio connection
    test_lm_studio_connection()
    print()
    
    print("🎉 Setup complete!")
    print()
    print("📋 Next steps:")
    print("1. Refresh your SuperAGI GUI (http://localhost:3000)")
    print("2. Go to Settings > Database")
    print("3. You should see 'Qdrant' as an available vector database")
    print("4. Go to Settings > API Keys")
    print("5. You should see 'LM Studio' as an available provider")
    print("6. Go to Models and add LM Studio models")

if __name__ == "__main__":
    main()
