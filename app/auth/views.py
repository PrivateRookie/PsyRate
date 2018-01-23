# -*- coding: utf-8 -*-
from flask import render_template, redirect, request, session, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from . import auth
from .. import db
from ..models import User
from ..email import send_email
from .forms import LoginForm, RegisterForm

@auth.before_app_request
def before_request():
    if current_user.is_authenticated and not current_user.confirmed \
    and request.endpoint[:5] != 'auth.' and request.endpoint != 'static':
        return redirect(url_for('auth.unconfirmed'))

@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        password = form.password.data
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(password):
            login_user(user, form.remember_me.data)
            flash("你已成功登陆")
            return redirect(url_for('main.user'))
        else:
            flash("用户们或密码错误")
    return render_template('login.html',form=form)

@auth.route('/logout')
def logout():
    logout_user()
    session['patient'] = "{}"
    flash('你已退出登陆')
    return redirect(url_for('main.index'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data
        username = form.username.data
        password = form.password.data
        invite_code = form.invite_code.data
        role = User.verify_invite_code(invite_code)
        if role is None:
            return render_template('register.html', form=form)
        else:
            user = User(email=email, username=username, password=password, role=role)
            db.session.add(user)
            db.session.commit()
            flash('你已成功注册,请打开注册邮箱点击链接激活账号')
            token = user.generate_confirmation_token()
            send_email(user.email, '确认账户', 'auth/email/confirm', user=user, token=token)
            return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)
    
@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        current_user.confirmed = True
        db.session.add(current_user._get_current_object())
        db.session.commit()
        flash('你已成功激活账户')
    else:
        flash('确认链接无效或已过期')
    return redirect(url_for('main.index'))
    
@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, '确认账户', 'auth/email/confirm', user=current_user, token=token)
    flash('确认邮件已发送至你的注册邮箱')
    return redirect(url_for('main.index'))
    
@auth.route('/profile/username', methods=["GET", "POST"])
def change_username():
    user = current_user._get_current_object()
    user.username = request.form.get('username')
    try:
        db.session.add(user)
        db.session.commit()
        flash("账户修改成功")
    except Exception as e:
        flash("账户修改失败")
        print(e)
    return redirect(url_for('main.user'))

@auth.route('/profile/password', methods=["GET", "POST"])
def change_password():
    user = current_user._get_current_object()
    old_password = request.form.get('old_password')
    new_password = request.form.get('new_password')
    confirm_password = request.form.get('confirm_password')
    if user.verify_password(old_password) and new_password == confirm_password:
        user.password = new_password
    else:
        flash("旧密码错误或密码确认错误")
    try:
        db.session.add(user)
        db.session.commit()
        flash("账户修改成功")
    except Exception as e:
        flash("账户修改失败")
        print(e)
    return redirect(url_for('main.user'))
    
@auth.route('delete')
def delete():
    u = current_user._get_current_object()
    db.session.delete(u)
    db.session.commit()
    return redirect(url_for('auth.register'))