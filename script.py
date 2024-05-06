from sqlalchemy.orm import sessionmaker
from models import User, Sector, Source, Subcategory
from werkzeug.security import generate_password_hash
from database import db, get_db_uri

Session = sessionmaker()
engine = db.create_engine(get_db_uri())
Session.configure(bind=engine)


session = Session()
users = [
    {"email": "user1@example.com", "password": "password1", "deleted": False},
    {"email": "user2@example.com", "password": "password2", "deleted": False},
    {"email": "user3@example.com", "password": "password3", "deleted": True},
    {"email": "user4@example.com", "password": "password4", "deleted": True},
]

sectors = [
    {"name": "Consumer Health", "deleted": False}, 
    {"name": "Beauty", "deleted": False},
    {"name": "Tech", "deleted": False},
    {"name": "Consumer Goods", "deleted": True},
    {"name": "Services", "deleted": True},
    {"name": "Basic Materials", "deleted": True}
]

sources = [
    {"name": "Social Media", "deleted": False},
    {"name": "News", "deleted": False},
    {"name": "Web", "deleted": False},
    {"name": "Admin", "deleted": False},
    {"name": "App", "deleted": False},
    {"name": "Blog", "deleted": True},
    {"name": "Forum", "deleted": True}
]

subcategories = [
    {"name": "Product Launches", "deleted": False},
    {"name": "New Product Releases", "deleted": False},
    {"name": "Mergers and Acquisitions", "deleted": False},
    {"name": "Rumors", "deleted": False},
    {"name": "Earnings", "deleted": False},
    {"name": "Financial Reports", "deleted": True},
    {"name": "Stock Market", "deleted": True},
    {"name": "Investments", "deleted": True},
    {"name": "Economy", "deleted": True},
    {"name": "Business", "deleted": True}
]

# Create users
for user_data in users:
    hashed_password = generate_password_hash(user_data["password"])
    user = User(email=user_data["email"], password=hashed_password, deleted_at=db.func.now() if user_data["deleted"] else None)
    session.add(user)

# Create sectors
for sector_data in sectors:
    sector = Sector(name=sector_data["name"], deleted_at=db.func.now() if sector_data["deleted"] else None)
    session.add(sector)

# Create sources
for source_data in sources:
    source = Source(name=source_data["name"], deleted_at=db.func.now() if source_data["deleted"] else None)
    session.add(source)

# Create subcategories
for subcategory_data in subcategories:
    subcategory = Subcategory(name=subcategory_data["name"], deleted_at=db.func.now() if subcategory_data["deleted"] else None)
    session.add(subcategory)

session.commit()