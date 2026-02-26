from app import create_app
from models import db, User, Todo

app = create_app()
with app.app_context():
    if not User.query.filter_by(username='demo').first():
        u = User(username='demo', email='demo@example.com')
        u.set_password('password')
        db.session.add(u)
        db.session.commit()
        t1 = Todo(title='Buy milk', description='2 liters of milk', owner_id=u.id)
        t2 = Todo(title='Read book', description='Finish reading chapter 4', owner_id=u.id)
        db.session.add_all([t1, t2])
        db.session.commit()
        print('Seeded demo user and todos')
    else:
        print('Demo user already exists')
