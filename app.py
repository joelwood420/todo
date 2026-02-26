from flask import Flask, render_template, redirect, url_for, request, flash, abort
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User, Todo


def create_app(test_config=None):
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dev-secret-change-me'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Apply test/runtime overrides before initializing extensions
    if test_config:
        app.config.update(test_config)

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register auth blueprint
    # Register auth blueprint (import from top-level auth_routes module)
    from auth_routes import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='')

    # Ensure database tables exist on startup
    with app.app_context():
        db.create_all()

    @app.route('/')
    def index():
        return redirect(url_for('todos'))

    @app.route('/login', methods=['GET','POST'])
    def login():
        from auth_forms import LoginForm
        form = LoginForm(request.form)
        if request.method == 'POST' and form.validate():
            username = form.username.data
            password = form.password.data
            user = User.query.filter_by(username=username).first()
            if user and user.check_password(password):
                login_user(user)
                flash('Logged in successfully.', 'success')
                return redirect(url_for('todos'))
            flash('Invalid credentials.', 'danger')
        return render_template('login.html', form=form)

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        flash('Logged out.', 'info')
        return redirect(url_for('login'))

    @app.route('/todos')
    @login_required
    def todos():
        page = request.args.get('page', 1, type=int)
        per_page = 5
        pagination = Todo.query.filter_by(owner_id=current_user.id).order_by(Todo.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
        return render_template('todos.html', todos=pagination)

    @app.route('/todos/new', methods=['GET','POST'])
    @login_required
    def new_todo():
        if request.method == 'POST':
            title = request.form.get('title')
            description = request.form.get('description')
            completed = True if request.form.get('completed') == 'on' else False
            if not title:
                flash('Title is required.', 'danger')
                return render_template('todo_form.html', action='Create')
            t = Todo(title=title, description=description, completed=completed, owner_id=current_user.id)
            db.session.add(t)
            db.session.commit()
            flash('Todo created.', 'success')
            return redirect(url_for('todos'))
        return render_template('todo_form.html', action='Create')

    @app.route('/todos/<int:todo_id>/edit', methods=['GET','POST'])
    @login_required
    def edit_todo(todo_id):
        t = Todo.query.get_or_404(todo_id)
        if t.owner_id != current_user.id:
            abort(404)
        if request.method == 'POST':
            title = request.form.get('title')
            description = request.form.get('description')
            completed = True if request.form.get('completed') == 'on' else False
            if not title:
                flash('Title is required.', 'danger')
                return render_template('todo_form.html', action='Edit', todo=t)
            t.title = title
            t.description = description
            t.completed = completed
            db.session.commit()
            flash('Todo updated.', 'success')
            return redirect(url_for('todos'))
        return render_template('todo_form.html', action='Edit', todo=t)

    @app.route('/todos/<int:todo_id>/delete', methods=['POST'])
    @login_required
    def delete_todo(todo_id):
        t = Todo.query.get_or_404(todo_id)
        if t.owner_id != current_user.id:
            abort(404)
        db.session.delete(t)
        db.session.commit()
        flash('Todo deleted.', 'info')
        return redirect(url_for('todos'))

    return app


if __name__ == '__main__':
    create_app().run(debug=True)
