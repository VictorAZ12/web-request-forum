from app import app, db
import os

if __name__ == '__main__':
    with app.app_context():
        db_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'webapp.db')
        if not os.path.exists(db_path):
            db.create_all()
            print("Database created successfully.")
        else:
            print("Database already exists.")
    app.run(debug=True)
