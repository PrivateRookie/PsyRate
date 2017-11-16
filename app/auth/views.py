# -*- coding: utf-8 -*-
from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user
from . import auth
from .. import db
from ..models import User
from .forms import LoginForm, RegisterForm

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None:
            user.password = form.password.data
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('你已成功登陆')
    return render_template('login.html',form=form)

@auth.route('/logout')
def logout():
    logout_user()
    flash('你已退出登陆')
    return redirect(url_for('main.index'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data
        username = form.username.data
        password = form.password.data
        u = User(email=email, username=username, password=password)
        db.session.add(u)
        db.session.commit()
        flash('你已成功注册')
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)