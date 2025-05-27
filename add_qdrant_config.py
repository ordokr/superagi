#!/usr/bin/env python3
"""
Script to add Qdrant configuration to existing vector database
"""

import sys
sys.path.append('/app')

def add_qdrant_config():
    """Add Qdrant configuration to existing vector database"""
    try:
        from superagi.models.db import connect_db
        from superagi.models.vector_dbs import Vectordbs
        from superagi.models.vector_db_configs import VectordbConfigs
        from superagi.models.vector_db_indices import VectordbIndices
        from superagi.models.organisation import Organisation
        from sqlalchemy.orm import sessionmaker

        print("🔧 Adding Qdrant configuration...")
        
        engine = connect_db()
        Session = sessionmaker(bind=engine)
        session = Session()

        try:
            # Get organization
            org = session.query(Organisation).filter(Organisation.id == 1).first()
            if not org:
                print("❌ Organization not found")
                return
                
            # Get existing Qdrant vector DB
            qdrant_vdb = session.query(Vectordbs).filter(
                Vectordbs.organisation_id == 1,
                Vectordbs.name == 'Qdrant'
            ).first()
            
            if not qdrant_vdb:
                print("❌ Qdrant vector database not found")
                return
                
            print(f"✅ Found Qdrant vector database (ID: {qdrant_vdb.id})")
            
            # Check if config already exists
            existing_config = session.query(VectordbConfigs).filter(
                VectordbConfigs.vector_db_id == qdrant_vdb.id
            ).first()
            
            if existing_config:
                print("✅ Qdrant configuration already exists")
            else:
                # Add Qdrant configuration
                url_config = VectordbConfigs(
                    vector_db_id=qdrant_vdb.id,
                    key="url",
                    value="http://super__qdrant:6333"
                )
                api_key_config = VectordbConfigs(
                    vector_db_id=qdrant_vdb.id,
                    key="api_key",
                    value=""
                )
                
                session.add(url_config)
                session.add(api_key_config)
                session.commit()
                print("✅ Qdrant configuration added")
                
            # Add default collection if it doesn't exist
            existing_index = session.query(VectordbIndices).filter(
                VectordbIndices.vector_db_id == qdrant_vdb.id,
                VectordbIndices.name == 'superagi-collection'
            ).first()
            
            if not existing_index:
                index = VectordbIndices(
                    name='superagi-collection',
                    vector_db_id=qdrant_vdb.id,
                    state='None',
                    dimensions=1536
                )
                session.add(index)
                session.commit()
                print("✅ Default collection 'superagi-collection' added")
            else:
                print("✅ Default collection already exists")
                
            # Verify configuration
            config_check = session.query(VectordbConfigs).filter(
                VectordbConfigs.vector_db_id == qdrant_vdb.id
            ).all()
            
            print(f"📋 Qdrant configuration:")
            for config in config_check:
                print(f"   - {config.key}: {config.value}")
                
        except Exception as e:
            print(f"❌ Error adding Qdrant configuration: {str(e)}")
            import traceback
            traceback.print_exc()
        finally:
            session.close()
            
    except Exception as e:
        print(f"❌ Database connection error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🚀 SuperAGI Qdrant Configuration Setup")
    print("=" * 40)
    add_qdrant_config()
    print()
    print("🎉 Qdrant configuration setup complete!")
    print("📋 Next steps:")
    print("1. Refresh your SuperAGI GUI (http://localhost:3000)")
    print("2. Go to Settings > Database")
    print("3. You should see 'Qdrant' with proper configuration")
    print("4. The URL should be: http://super__qdrant:6333")
