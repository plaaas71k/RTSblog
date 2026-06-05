from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#чистая база SQLAlchemy
class Base(DeclarativeBase):
  pass

#обертка для Flask (db) - мост который соединяет SQLAlchemy и Flask
db = SQLAlchemy(model_class=Base)
db.init_app(app)
#конкретная таблица,  в которой создается пост пользователя
class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    # username: Mapped[str] = mapped_column(unique=True)
    title: Mapped[str] = mapped_column(db.String(200),nullable=True)
    text: Mapped[str] = mapped_column(db.String(200),nullable=True)

    date: Mapped[datetime] = mapped_column(db.DateTime, default=datetime.now, nullable=True)
    def __repr__(self):
        return f'<User {self.id}>'


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/create_post', methods=['GET', 'POST'])
def posts():
    if request.method == 'POST':
        title = request.form['title']
        text = request.form['text']

        user = User(title=title, text=text)
        try:
            db.session.add(user)
            db.session.commit()
            return redirect('/posts')
        except:
            return('Ошибка добавления')
    else:
        return render_template('create_post.html')


@app.route('/posts')
def posts_page():
    users_posts = User.query.order_by(User.date).all()
    isinstance(users_posts, object)
    return render_template('posts.html', users_posts=users_posts)

@app.route('/posts/<int:post_id>')
def single_post(post_id):
    user = User.query.get(post_id)
    return render_template('post_user.html', user=user)

@app.route('/posts/<int:post_id>/del')
def del_post(post_id):
    user = User.query.get(post_id)
    try:
        db.session.delete(user)
        db.session.commit()
        return redirect('/posts')
    except:
        return 'Произошла ошибка удаления'
    return render_template('post_user.html', user=user)



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(port=5001, debug=True)