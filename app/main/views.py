# -*- coding: utf-8 -*-

import os
from datetime import datetime
from flask import render_template, redirect, url_for, flash, session, request
from flask_login import current_user
from . import main
from .forms import *
from .. import db, surveymodels, models
from ..static import raw_forms, schema
from ..models import Permission
from ..decorators import permission_required, admin_required

app_path = '\\'.join(os.path.split(os.path.abspath(__file__))[0].split('\\')[:-1])
rates_path = app_path + '\\templates\\rates'

def get_pager(report_type, current_status, current_form_name):
    report_schema = getattr(schema, report_type, None)
    index_min, index_max = 0, len(report_schema) - 1
    index = report_schema.index(current_status + '|' + current_form_name)
    if index - 1 < index_min:
        pre = dict(endpoint='main.forms', report_type=report_type)
    else:
        status, form_name = report_schema[index - 1].split('|')
        pre = dict(endpoint='main.forms', report_type=report_type,
        form_name=form_name, status=status)
    if index + 1 > index_max:
        next = dict(endpoint='main.forms', report_type=report_type)
    else:
        status, form_name = report_schema[index + 1].split('|')
        next = dict(endpoint='main.forms', report_type=report_type,
        form_name=form_name, status=status)
    
    return pre, next
    
def flat(li):
    if len(li) > 1:
        return ''.join(str(i) for i in li)
    return li[0]

@main.route('/', methods=['GET', 'POST'])
def index():
    rates = [filename.split('.')[0] for filename in os.listdir(rates_path)]
    return render_template('index.html', rates=rates)

@main.route('/forms')
@permission_required(Permission.SELFREPORT)
def forms():
    form_name = request.args.get('form_name', None)
    status = request.args.get('status', 'v9')
    report_type = request.args.get('report_type', 'dev_report')
    if form_name is None:
        return render_template('allforms.html')
    raw_form = getattr(raw_forms, form_name, None)
    previous, next = get_pager(report_type, status, form_name)
    options = dict(survey=raw_form, route='main.recevie', status=status, report_type=report_type,
    previous=previous, next=next)
    return render_template('rates/{}.html'.format(form_name), **options)

@main.route('/selfreport')
def selfreport():
    previous, next = get_pager('self_report', 'v0', 'cover')
    return render_template('rates/cover.html', status='v0', route='main.recevie',
    previous=previous, next=next, report_type='self_report')
    
@main.route('/ohterreport')
def otherreport():
    previous, next = get_pager('other_report', 'v0', 'cover')
    return render_template('rates/cover.html', status='v0', route='main.recevie',
    previous=previous, next=next, report_type='other_report')
    
@main.route('/echo', methods=['GET', 'POST'])
def echo():
    data = {attr:flat(request.form.getlist(attr)) for attr in request.form.keys() if attr.startswith('q')}
    return render_template('echo.html', data=data)
    
@main.route('/recevie', methods=['GET', 'POST'])
def recevie():
    """
    patient_info = session.get('patient_info', None)
    
    if patient_info is None:
        patient_info = dict()
        patient_info['name'] = request.form.get('q_2')
        patient_info['code'] = request.form.get('q_1')
        patient_info['writer'] = current_user.username
        # 提交新患者信息
        data = [flat(request.form.getlist(attr)) for attr in request.form.keys() if attr.startswith('q')]
        data = {k:v for k, v in zip(['code', 'name', 'entry_date', 'doctor'], data)}
        #data['entry_date'] = datetime.strptime(data['entry_date'], '%Y-%m-%d')
        data['entry_date'] = datetime.now()
        data['recorder_id'] = current_user.id
        p = models.Patient(**data)
        db.session.add(p)
        db.session.commit()
        patient_info['patient_id'] = p.id
        session['patient_info'] = patient_info
    
    model = getattr(surveymodels, request.args['form_name'].uppercase())
    data = {attr:flat(request.form.getlist(attr)) for attr in request.form.keys() if attr.startswith('q')}
    data['p_id'] = patient_info['patient_id']
    data['status'] = request.args['status']
    record = model(**data)
    db.session.add(record)
    db.session.commit()
    return render_template('echo.html', data=data)
    """
    data = {attr:flat(request.form.getlist(attr)) for attr in request.form.keys() if attr.startswith('q')}
    patient_info = session.get('patient_info', None)
    data.update(patient_info)
    return render_template('echo.html', data=data)
        
        
    
    
@main.route('/test')
def test():
    return render_template('js.html')