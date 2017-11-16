# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required

class DemoForm(FlaskForm):
    msg = StringField('给自己写段消息吧', validators=[Required()])
    submit = SubmitField('提交')