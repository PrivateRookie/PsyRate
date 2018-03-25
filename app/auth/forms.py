# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User

class LoginForm(FlaskForm):
    email = StringField('邮箱', validators=[Required(), Length(1, 64), Email()])
    password = PasswordField('密码', validators=[Required()])
    remember_me = BooleanField('保持登录')
    submit = SubmitField('登陆')

class RegisterForm(FlaskForm):
    email = StringField('邮箱', validators=[Required(), Length(1, 64), Email()])
    username = StringField('用户名', validators=[
            Required(), Length(1, 64)])
    password = PasswordField('密码', validators=[Required(),
            EqualTo('password2', message='密码必须相同')])
    password2 = PasswordField('确认密码', validators=[Required()])
    submit = SubmitField('提交')
    
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('该邮箱已经被注册')
    
    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('该用户名已经被使用')