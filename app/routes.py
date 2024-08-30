# app/routes.py
from flask import render_template, session, redirect, url_for, flash, request
from . import db
from .models import User, Role
from .forms import NameForm
from flask import Blueprint

main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()

    form.role.choices = [(role.id, role.name) for role in Role.query.order_by('name')]

    if form.validate_on_submit():
        role = Role.query.filter_by(id=form.role.data).first()
        user = User.query.filter_by(username=form.name.data).first()

        if user is None:
            user = User(username=form.name.data, role=role)
            db.session.add(user)
            db.session.commit()
            session['known'] = False
        else:
            session['known'] = True

        session['name'] = form.name.data
        session['role'] = role.name
        return redirect(url_for('main.index'))

    users = User.query.all()
    roles = Role.query.all()

    return render_template('index.html', form=form, name=session.get('name'),
                           known=session.get('known', False), user_all=users, roles=roles)

@main.route('/dashboard')
def dashboard():
    users = User.query.all()
    return render_template('dashboard.html', users=users)

@main.route('/admin')
def admin():
    roles = Role.query.all()
    return render_template('admin.html', roles=roles)

@main.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    form = NameForm(obj=user)
    form.role.choices = [(role.id, role.name) for role in Role.query.order_by('name')]

    if form.validate_on_submit():
        user.username = form.name.data
        user.role = Role.query.get(form.role.data)
        db.session.commit()
        flash(f'Usuário {user.username} atualizado com sucesso.')
        return redirect(url_for('main.admin'))

    return render_template('edit_user.html', form=form, user=user)

@main.route('/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash(f'Usuário {user.username} foi excluído com sucesso.')
    return redirect(url_for('main.admin'))

@main.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@main.app_errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500
