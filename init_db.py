from sqlalchemy import inspect
from app.extensions import engine, Base, check_database_connection


from app.models import User, CallSession, CallRating


def create_all_tables():
    print("=" * 60)
    print("🚀 SpeakU v2 - Database Initialization")
    print("=" * 60)
    
    # Step 1: Check database connection
    print("\n📡 Step 1: Checking database connection...")
    if not check_database_connection():
        print("❌ Cannot connect to database. Check your .env file!")
        return False
    
    # Step 2: Show what will be created
    print("\n📋 Step 2: Models to create:")
    print("   • User (users table)")
    print("   • CallSession (call_sessions table)")
    print("   • CallRating (call_ratings table)")
    
    # Step 3: Create tables
    print("\n🔨 Step 3: Creating tables...")
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Tables created successfully!")
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        return False
    

    print("\n🔍 Step 4: Verifying tables in database...")
    inspector = inspect(engine)
    existing_tables = inspector.get_table_names()
    
    expected_tables = ["users", "call_sessions", "call_ratings"]
    
    for table in expected_tables:
        if table in existing_tables:
            
            columns = inspector.get_columns(table)
            indexes = inspector.get_indexes(table)
            foreign_keys = inspector.get_foreign_keys(table)
            
            print(f"\n   ✅ {table}")
            print(f"      Columns: {len(columns)}")
            print(f"      Indexes: {len(indexes)}")
            print(f"      Foreign Keys: {len(foreign_keys)}")
        else:
            print(f"   ❌ {table} NOT FOUND!")
            return False
    
    
    print("\n" + "=" * 60)
    print("🎉 SUCCESS! Database initialized successfully!")
    print("=" * 60)
    print("\n📊 Summary:")
    print(f"   Total tables created: {len(expected_tables)}")
    print(f"   Database: Supabase PostgreSQL")
    print(f"   Status: Ready for use ✅")
    print("\n💡 Next Steps:")
    print("   1. Go to Supabase Dashboard → Table Editor")
    print("   2. You should see all 3 tables there!")
    print("   3. Continue with API development")
    print("=" * 60)
    
    return True


def drop_all_tables():
    print("⚠️  WARNING: This will DELETE all tables and data!")
    confirmation = input("Type 'YES DELETE' to confirm: ")
    
    if confirmation == "YES DELETE":
        print("🗑️  Dropping all tables...")
        Base.metadata.drop_all(bind=engine)
        print("✅ All tables dropped")
    else:
        print("❌ Cancelled - no changes made")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--drop":
        drop_all_tables()
    else:
        create_all_tables()