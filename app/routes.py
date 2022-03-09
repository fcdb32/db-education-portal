import base64
import locale

from flask import render_template, request, url_for, flash, redirect

from app import app, db
from .models import Post

locale.setlocale(locale.LC_ALL, "ru_RU.UTF-8")
allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}


@app.route('/')
def index():
    posts = db.session.query(Post).order_by(Post.created.desc()).all()
    db.session.close()
    return render_template('index.html', posts=posts)


@app.route('/<int:post_id>')
def post(post_id):
    post = db.session.query(Post).filter_by(id=post_id).first_or_404()
    db.session.close()
    rendered_image = base64.b64encode(post.image).decode('ascii')
    return render_template('post.html', post=post, image=rendered_image)


@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        image_file = request.files['image']
        if not title:
            flash('Укажите заголовок статьи')
        elif image_file.filename and image_file.filename.split('.')[1] not in allowed_extensions:
            flash(f'Неподдерживаемое расширение изображения. Поддерживаемые форматы: {", ".join(allowed_extensions)}')
        else:
            db.session.add(Post(title=title, content=content, image=image_file.read()))
            db.session.commit()
            db.session.close()
    return render_template('index.html')


@app.route('/<int:post_id>/edit', methods=('GET', 'POST'))
def edit(post_id):
    post = db.session.query(Post).filter_by(id=post_id).first_or_404()
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        image_file = request.files['image']
        if not title:
            flash('Укажите заголовок статьи')
        elif image_file.filename and image_file.filename.split('.')[1] not in allowed_extensions:
            flash(f'Неподдерживаемое расширение изображения. Поддерживаемые форматы: {", ".join(allowed_extensions)}')
        else:
            post.title = title
            post.content = content
            image = image_file.read()
            if image:
                post.image = image
            db.session.commit()
            db.session.close()
            return redirect(url_for('index'))
    return render_template('edit.html', post=post)


@app.route('/<int:post_id>/delete', methods=('POST',))
def delete(post_id):
    post = db.session.query(Post).filter_by(id=post_id).first_or_404()
    db.session.delete(post)
    db.session.commit()
    db.session.close()
    flash(f'Статья "{post.title}" была успешно удалена')
    return redirect(url_for('index'))


@app.route('/about')
def about():
    return render_template('about.html')

