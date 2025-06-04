from flask import Blueprint, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from .models import db, User, Game
from datetime import datetime

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            return redirect(url_for('main.index'))
        return render_template('login.html', error='Неверные данные')
    return render_template('login.html')

@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        if User.query.filter_by(email=email).first():
            return render_template('register.html', error='Email уже зарегистрирован')
        password_hash = generate_password_hash(password)
        user = User(username=username, email=email, password_hash=password_hash)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('main.login'))
    return render_template('register.html')

@main.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('main.index'))

@main.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        user = User.query.filter_by(email=email).first()
        if user:
            return render_template('password_reset_sent.html', email=email)
        else:
            return render_template('user_not_found.html', email=email)
    return render_template('forgot_password.html')

@main.route('/game/<int:game_id>')
def game_detail(game_id):
    game = Game.query.get_or_404(game_id)
    return render_template('game_detail.html', game=game)

@main.route('/add-game', methods=['GET', 'POST'])
def add_game():
    if 'user_id' not in session:
        return redirect(url_for('main.login'))
    if request.method == 'POST':
        # Дата (input type="date") приходит как 'YYYY-MM-DD'
        date_str = request.form.get('release_date', '')
        release_date = datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else None

        access_vision = request.form.get('access_vision', 'none')
        vision_detail = request.form.get('vision_detail', '') if access_vision == 'partial' else None

        game = Game(
            title=request.form['title'],
            genre=request.form['genre'],
            release_date=release_date,
            store_link=request.form['store_link'],
            access_vision=access_vision,
            vision_detail=vision_detail,
            issues=request.form.get('issues', ''),
            solutions=request.form.get('solutions', ''),
            added_by=session['user_id']
        )
        db.session.add(game)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('add_game.html')

@main.route('/edit-game/<int:game_id>', methods=['GET', 'POST'])
def edit_game(game_id):
    game = Game.query.get_or_404(game_id)
    if session.get('user_id') != game.added_by:
        return redirect(url_for('main.index'))
    if request.method == 'POST':
        game.title = request.form['title']
        game.genre = request.form['genre']
        # Дата (input type="date") приходит как 'YYYY-MM-DD'
        date_str = request.form.get('release_date', '')
        game.release_date = datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else None
        game.store_link = request.form['store_link']
        game.access_vision = request.form.get('access_vision', 'none')
        game.vision_detail = request.form.get('vision_detail', '') if game.access_vision == 'partial' else None
        game.issues = request.form.get('issues', '')
        game.solutions = request.form.get('solutions', '')
        db.session.commit()
        return redirect(url_for('main.game_detail', game_id=game.id))
    return render_template('edit_game.html', game=game)

@main.route('/delete-game/<int:game_id>', methods=['POST'])
def delete_game(game_id):
    game = Game.query.get_or_404(game_id)
    if session.get('user_id') == game.added_by:
        db.session.delete(game)
        db.session.commit()
    return redirect(url_for('main.index'))
@main.route('/games', methods=['GET', 'POST'])
def games():
    query = ''
    games = []
    if request.method == 'POST':
        query = request.form.get('search', '').strip()
        if query:
            games = Game.query.filter(Game.title.ilike(f'%{query}%')).all()
        else:
            games = Game.query.all()
    else:
        games = Game.query.all()
    return render_template('games.html', games=games, search=query)
