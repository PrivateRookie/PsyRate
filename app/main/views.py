# -*- coding: utf-8 -*-

import os
from flask import render_template, redirect, url_for, flash, session, request
from . import main
from .forms import *
from .. import db
from ..static import raw_forms

rates_path = r'F:\Git\PsyRates\app\templates\rates'

@main.route('/', methods=['GET', 'POST'])
def index():
    rates = [filename.split('.')[0] for filename in os.listdir(rates_path)]
    return render_template('index.html', rates=rates)

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