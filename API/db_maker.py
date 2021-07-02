"""
File that takes care of creating all tables from models in the database.
Usage: In terminal: python db_maker.py
"""

try:
    from app import app
    from router import db
except Exception as e:
    print("Some modules are missing {} ".format(e))
else:

    with app.app_context():
        db.create_all()

    print("Database created successfully.")
