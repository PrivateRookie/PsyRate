# -*- coding: utf-8 -*-
from flask import render_template, redirect, request, session, url_for, flash
from flask_login import login_user, logout_user, current_user
from . import auth
from .. import db
from ..models import User
from .forms import LoginForm, RegisterForm

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
            u = User(email=email, username=username, password=password, role=role)
            db.session.add(u)
            db.session.commit()
            flash('你已成功注册')
            return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)
    
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