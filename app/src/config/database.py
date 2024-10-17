from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from app.src.config.settings import get_settings
from passlib.context import CryptContext

settings = get_settings()

# Ustawienie odpowiedniego URL dla PostgreSQL
if settings.DATABASE_URL.startswith('postgres://'):
    settings.DATABASE_URL = settings.DATABASE_URL.replace('postgres://', 'postgresql://')

# Konfiguracja bazy danych
engine = create_engine(
    url=settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_size=100,
    max_overflow=50,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Deklaracja bazy
DBBase = declarative_base()

# Konfiguracja kontekstu hashowania
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def initialize_database():
    from app.src.module.users.models import Role, User, Permission

    DBBase.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        edit_documents_permissions = db.query(Permission).filter_by(name="edit_documents").first()
        view_user_info_permissions = db.query(Permission).filter_by(name="view_user_info").first()
        super_admin_role = db.query(Role).filter_by(name="super_admin").first()
        admin_role = db.query(Role).filter_by(name="admin").first()
        user_role = db.query(Role).filter_by(name="user").first()


        if not super_admin_role:
            super_admin_role = Role(name="super_admin")
            db.add(super_admin_role)

        if not admin_role:
            admin_role = Role(name="admin")
            db.add(admin_role)

        if not user_role:
            user_role = Role(name="user")
            db.add(user_role)

        if not edit_documents_permissions:
            edit_documents_permissions= Permission(name="edit_documents")
            db.add(edit_documents_permissions)

        if not view_user_info_permissions:
            view_user_info_permissions = Permission(name="view_user_info")
            db.add(view_user_info_permissions)

        if edit_documents_permissions not in super_admin_role.permissions:
            super_admin_role.permissions.append(edit_documents_permissions)


        if view_user_info_permissions not in super_admin_role.permissions:
            super_admin_role.permissions.append(view_user_info_permissions)

        db.commit()

        # Sprawdzenie, czy użytkownik admin istnieje
        super_admin_user = db.query(User).filter(User.role_id == super_admin_role.id).first()
        if not super_admin_user:
            hashed_password = pwd_context.hash(settings.ADMIN_PASSWORD)  # Hasło z pliku settings
            admin_user = User(
                username=settings.ADMIN_USERNAME,  # Nazwa użytkownika z pliku settings
                hashed_password=hashed_password,
                name="Admin",
                surname="Admin",
                email=settings.ADMIN_EMAIL,  # E-mail z pliku settings
                role_id=super_admin_role.id
            )
            db.add(admin_user)
            db.commit()

    finally:
        db.close()



