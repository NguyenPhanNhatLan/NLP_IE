from app.db.mongo import get_database

def get_db():
    db = get_database()
    return db