# -*- coding: utf-8 -*-

from flask import render_template, redirect, url_for, flash, session, request
from . import main
from .forms import *
from .. import db
from ..static import raw_forms

@main.route('/', methods=['GET', 'POST'])
def index():
    form = DemoForm()
    if form.validate_on_submit():
        session['msg'] = form.msg.data
        return redirect(url_for('.index'))
    return render_template('index.html', form=form, msg=session.get('msg'))

@main.route('/forms')
def forms():
    form_name = request.args.get('form_name', None)
    if not form_name:
        return render_template('allforms.html')
    raw_form = getattr(raw_forms, form_name, None)
    return render_template('rates/' + form_name + '.html', survey=raw_form, route='main.echo')
    
    
@main.route('/echo', methods=['GET', 'POST'])
def echo():
    data = [(attr, request.form.getlist(attr)) for attr in request.form.keys() if attr.startswith('q')]
    return render_template('echo.html', data=data)