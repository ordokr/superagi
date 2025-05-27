#!/usr/bin/env python3
"""
Setup script to add Qdrant vector database to SuperAGI
"""

import sys
sys.path.append('/app')

def setup_vector_database():
    """Set up Qdrant vector database"""
    try:
        from superagi.models.db import connect_db
        from superagi.models.vector_dbs import Vectordbs
        from superagi.models.organisation import Organisation
        from sqlalchemy.orm import sessionmaker

        print("🔧 Setting up Qdrant vector database...")
        
        engine = connect_db()
        Session = sessionmaker(bind=engine)
        session = Session()

        try:
            # Get organization
            org = session.query(Organisation).filter(Organisation.id == 1).first()
            if not org:
                print("❌ Organization not found")
                return
                
            # Check if Qdrant vector DB already exists
            existing_vdb = session.query(Vectordbs).filter(
                Vectordbs.organisation_id == 1,
                Vectordbs.name == 'Qdrant'
            ).first()
            
            if existing_vdb:
                print("✅ Qdrant vector database already configured")
            else:
                # Add Qdrant vector database
                qdrant_db = Vectordbs.add_vector_db(session, 'Qdrant', 'Qdrant', org)
                print(f"✅ Qdrant vector database added successfully (ID: {qdrant_db.id})")
                
            # List all vector databases
            vector_dbs = Vectordbs.get_vector_db_from_organisation(session, org)
            print(f"📋 Current vector databases for org 1:")
            for vdb in vector_dbs:
                print(f"   - {vdb.name} ({vdb.db_type}) - ID: {vdb.id}")
                
        except Exception as e:
            print(f"❌ Error setting up vector database: {str(e)}")
        finally:
            session.close()
            
    except Exception as e:
        print(f"❌ Database connection error: {str(e)}")

if __name__ == "__main__":
    print("🚀 SuperAGI Vector Database Setup")
    print("=" * 40)
    setup_vector_database()
    print()
    print("🎉 Vector database setup complete!")
    print("📋 Next steps:")
    print("1. Refresh your SuperAGI GUI (http://localhost:3000)")
    print("2. Go to Settings > Database")
    print("3. You should see 'Qdrant' as an available vector database")
    print("4. Configure it with URL: http://super__qdrant:6333")
