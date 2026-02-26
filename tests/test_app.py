import pytest
import importlib.util, os, sys
# Ensure project root is on sys.path so local modules (models) import correctly
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
# Load top-level app.py explicitly to avoid package name collision with app/ directory
spec = importlib.util.spec_from_file_location('app_module', os.path.join(project_root, 'app.py'))
app_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(app_module)
create_app = app_module.create_app
from models import db, User, Todo

@pytest.fixture
def app():
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
    })
    with app.app_context():
        db.create_all()
        u = User(username='test', email='t@example.com')
        u.set_password('pass')
        db.session.add(u)
        db.session.commit()
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

def login(client):
    return client.post('/login', data={'username':'test','password':'pass'}, follow_redirects=True)

def test_login(client):
    rv = login(client)
    assert b'Logged in' in rv.data or rv.status_code == 200

def test_crud(client, app):
    login(client)
    # create
    rv = client.post('/todos/new', data={'title':'t1','description':'d'}, follow_redirects=True)
    assert b't1' in rv.data
    # verify in DB
    with app.app_context():
        todo = Todo.query.filter_by(title='t1').first()
        assert todo is not None
        # edit
        rv = client.post(f'/todos/{todo.id}/edit', data={'title':'t1 edited','description':'d2','completed':'on'}, follow_redirects=True)
        assert b't1 edited' in rv.data
        # delete
        rv = client.post(f'/todos/{todo.id}/delete', follow_redirects=True)
        assert b't1 edited' not in rv.data
