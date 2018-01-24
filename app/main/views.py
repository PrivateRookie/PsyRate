# -*- coding: utf-8 -*-

import os
import json
from datetime import datetime
from flask import render_template, redirect, url_for, flash, session, request
from flask_login import current_user, login_required
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
        if report_type == 'self_report':
            next = dict(endpoint='main.forms', report_type='other_report', form_name='cover_other', status='v0')
        else:
            next = dict(endpoint='main.get_all_patients')
    else:
        status, form_name = report_schema[index + 1].split('|')
        next = dict(endpoint='main.forms', report_type=report_type,
        form_name=form_name, status=status)
    
    return pre, next
    
def prerender(raw_form, record):
    def sort_key(item):
        sequence = item[0].split('_')[1:]
        sequence = [int(i) for i in sequence]
        return sequence

    questions = raw_form['questions']
    record = [(attr, getattr(record, attr)) for attr in dir(record) if attr.startswith('q_')]
    record = sorted(record, key=sort_key)
    print(record)
    for question, selected in zip(questions, record):
        if selected[1]:
            question['default'] = selected[1]
        else:
            question['default'] = ''
    return raw_form
    
    
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
    # load record if exits
    p_id = json.loads(session.get('patient', "{}")).get('id', 0)

    if form_name is None:
        return render_template('allforms.html')
    elif form_name in ['cover', 'cover_other']:
        raw_form = getattr(raw_forms, form_name, None)
        patient = json.loads(session.get('patient', "{}"))
        previous, next = get_pager(report_type, status, form_name)
        options = dict(survey=raw_form, route='main.recevie', status=status, report_type=report_type,
        form_name=form_name, patient=patient, previous=previous, next=next)
        return render_template('rates/{}.html'.format(form_name), **options)
    else:
        model  = getattr(surveymodels, form_name.upper())
        # special case for followup
        if form_name == 'followup':
            record = model.query.filter_by(p_id=p_id, type=report_type).first()
        else:
            record = model.query.filter_by(p_id=p_id, status=status).first()
        raw_form = getattr(raw_forms, form_name, None)
        rendered_form = prerender(raw_form, record)
        patient = json.loads(session.get('patient', "{}"))
        previous, next = get_pager(report_type, status, form_name)
        options = dict(survey=rendered_form, route='main.recevie', status=status, report_type=report_type,
        form_name=form_name, patient=patient, previous=previous, next=next)
        return render_template('rates/{}.html'.format(form_name), **options)

@main.route('/selfreport')
def selfreport():
    previous, next = get_pager('self_report', 'v0', 'cover')
    patient = json.loads(session.get('patient', "{}"))
    return render_template('rates/cover.html', status='v0', route='main.patient_regist',
    previous=previous, next=next, patient=patient, report_type='self_report', form_name='cover')
    
@main.route('/ohterreport')
def otherreport():
    previous, next = get_pager('other_report', 'v0', 'cover')
    patient = json.loads(session.get('patient', "{}"))
    return render_template('rates/cover.html', status='v0', route='main.recevie',
    previous=previous, next=next, patient=patient, report_type='other_report', form_name='cover')
    
@main.route('/patient_regist', methods=['GET', 'POST'])
def patient_regist():
    data = [flat(request.form.getlist(attr)) for attr in request.form.keys() if attr.startswith('q')]
    data = {k:v for k, v in zip(['code', 'name', 'entry_date', 'doctor'], data)}
      
    p = models.Patient(**data)
    p.recorder = current_user._get_current_object()
    try:
        db.session.add(p)
        db.session.commit()
        patient = dict()
        patient['name'] = request.form.get('q_2')
        patient['code'] = request.form.get('q_1')
        patient['id'] = p.id
        patient['writer'] = current_user.username
        session['patient'] = json.dumps(patient)
    except Exception as e:
        print(e)
    return redirect(url_for('main.forms', status='v2', route='main.recevie', report_type='self_report', form_name='followup'))
    
@main.route('/logoutpatient')
def logoutpatient():
    session['patient'] = "{}"
    flash('你已经退出填写')
    return redirect(url_for('main.get_all_patients'))
    
@main.route('/echo', methods=['GET', 'POST'])
def echo():
    data = {attr:flat(request.form.getlist(attr)) for attr in request.form.keys() if attr.startswith('q')}
    return render_template('echo.html', data=data)
    
@main.route('/recevie', methods=['GET', 'POST'])
def recevie():
    data = {attr:flat(request.form.getlist(attr)) for attr in request.form.keys() if attr.startswith('q')}
    patient = json.loads(session.get('patient', "{}"))
    model = getattr(surveymodels, request.form.get('form_name').upper())
    data['p_id'] = patient.get('id', '')
    # special case for followup
    if request.form.get('form_name') != 'followup':
        data['status'] = request.form.get('status')
        record = model.query.filter_by(p_id=data['p_id'], status=data['status']).first()
    else:
        data['type'] = request.form.get('report_type')
        record = model.query.filter_by(p_id=data['p_id'], type=request.form['report_type']).first()
    if not record:
        record = model(**data)
    else:
        for attr, val in ((attr, getattr(record, attr)) for attr in dir(record) if attr.startswith('q_')):
            setattr(record, attr, val)
    db.session.add(record)
    db.session.commit()
    return render_template('echo.html', data=data)
    
@main.route('/patients')
def get_all_patients():
    patients = current_user.patients
    return render_template('patients.html', patients=patients)
    
@main.route('/editpatient')
def editpatient():
    id = request.args.get('id', 0)
    p = models.Patient.query.filter_by(id=id).first()
    if p is None:
        flash('该患者不存在')
        return redirect(url_for('main.get_all_patients'))
    else:
        patient = dict()
        patient['name'] = p.name
        patient['code'] = p.code
        patient['writer'] = p.recorder.username
        patient['id'] = p.id
        session['patient'] = json.dumps(patient)
        return redirect(url_for('main.selfreport'))

@main.route('/status')
def change_status():
    id = request.args.get('id')
    if id is None:
        flash("无此病人，请重新选择")
        return redirect(url_for("main.get_all_patients"))
    p = models.Patient.query.filter_by(id=id).first()
    p.finished = not p.finished
    try:
        db.session.add(p)
        db.session.commit()
        flash("修改成功")
        return redirect(url_for('main.logoutpatient'))
    except Exception as e:
        print(e)
        flash('修改失败')
        return redirect(url_for('main.get_all_patients'))
        
@main.route('/delete/patient')
@login_required
def delete():
    p_id = request.args.get('id')
    patient = models.Patient.query.filter_by(id=p_id).first()
    db.session.delete(patient)
    db.session.commit()
    return redirect(url_for('main.get_all_patients'))
        
@main.route('/user')
@permission_required(Permission.SELFREPORT)
def user():
    u = current_user._get_current_object()
    finished = models.Patient.query.filter_by(finished=True).filter_by(recorder=u).count()
    unfinished = models.Patient.query.filter_by(finished=False).filter_by(recorder=u).count()
    total = finished + unfinished
    p = json.loads(session.get('patient', "{}"))
    p_name = p.get('name', '')
    p_code = p.get('code', '')
    p_id = p.get('id')
    p_finished = models.Patient.query.filter_by(id=p.get('id')).first()
    username = u.username
    email = u.email
    return render_template('user.html', u=u, finished=finished, unfinished=unfinished, total=total,
        p_name=p_name, p_code=p_code, p_finished=p_finished, username=username, email=email)