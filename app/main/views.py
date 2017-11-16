# -*- coding: utf-8 -*-

from flask import render_template, redirect, url_for, flash, session
from . import main
from .forms import *
from .. import db

@main.route('/index', methods=['GET', 'POST'])
def index():
    form = DemoForm()
    if form.validate_on_submit():
        session['msg'] = form.msg.data
        return redirect(url_for('.index'))
    return render_template('index.html', form=form, msg=session.get('msg'))
