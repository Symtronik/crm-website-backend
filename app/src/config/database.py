from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from app.src.config.settings import get_settings
from passlib.context import CryptContext

settings = get_settings()

if settings.DATABASE_URL.startswith('postgres://'):
    settings.DATABASE_URL = settings.DATABASE_URL.replace('postgres://', 'postgresql://')

engine = create_engine(
    url=settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_size=100,
    max_overflow=50,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

DBBase = declarative_base()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def initialize_database():
    from app.src.module.users.models import Role, User  # Przenieś import do wnętrza funkcji
    """
    Inicjalizuje bazę danych, tworzy domyślne role oraz admina, jeśli nie istnieją.
    """
    DBBase.metadata.create_all(bind=engine)

    # Stwórz sesję
    db = SessionLocal()

    # Sprawdź, czy role są już stworzone, jeśli nie, to je stwórz
    admin_role = db.query(Role).filter_by(name="admin").first()
    user_role = db.query(Role).filter_by(name="user").first()

    if not admin_role:
        admin_role = Role(name="admin")
        db.add(admin_role)

    if not user_role:
        user_role = Role(name="user")
        db.add(user_role)

    db.commit()

    # Sprawdź, czy istnieje użytkownik admin, jeśli nie, stwórz go
    admin_role = db.query(Role).filter(Role.name == "admin").first()
    if not admin_role:
        raise Exception("Admin role does not exist.")

    admin_user = db.query(User).filter(User.role_id == admin_role.id).first()
    if not admin_user:
        hashed_password = pwd_context.hash("admin")
        admin_user = User(
            username="admin11",
            hashed_password=hashed_password,
            name="Admin",
            surname="Admin",
            email="admi11n1@example.com",
            role_id=admin_role.id
        )
        db.add(admin_user)
        db.commit()

    db.close()


