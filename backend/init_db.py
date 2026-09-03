import os
from database import engine, Base, SessionLocal
from models import User, RoleEnum
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def init_db():
    print("Creating tables in PostgreSQL...")
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # Check if demo_investigator exists
        demo_user = db.query(User).filter(User.username == "demo_investigator").first()
        if not demo_user:
            demo_user = User(
                username="demo_investigator",
                password_hash=pwd_context.hash("demo-password"),
                role=RoleEnum.investigator,
                organization="SUTRA Demo"
            )
            db.add(demo_user)
            print("Created demo_investigator user.")
        
        # Check if demo_admin exists
        admin_user = db.query(User).filter(User.username == "demo_admin").first()
        if not admin_user:
            admin_user = User(
                username="demo_admin",
                password_hash=pwd_context.hash("demo-password"),
                role=RoleEnum.admin,
                organization="SUTRA Admin"
            )
            db.add(admin_user)
            print("Created demo_admin user.")
            
        db.commit()
    except Exception as e:
        print("Error during database initialization:", e)
        db.rollback()
    finally:
        db.close()
    
    print("Database initialization complete.")

if __name__ == "__main__":
    init_db()
