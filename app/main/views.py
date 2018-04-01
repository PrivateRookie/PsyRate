# -*- coding: utf-8 -*-

import os
import json
from datetime import datetime
from flask import render_template, redirect, url_for, flash, session, request, abort
from flask_login import current_user, login_required
from . import main
from .forms import *
from .. import db, surveymodels, models
from ..static import raw_forms, schema
from ..models import Permission
from ..decorators import permission_required, admin_required
from sqlite3 import IntegrityError

if os.sys.platform.startswith('linux'):
    app_path = '/'.join(os.path.split(os.path.abspath(__file__))[0].split('/')[:-1])
    rates_path = app_path + '/templates/rates'
elif os.sys.platform == 'win32':
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
    for question, selected in zip(questions, record):
        if selected[1] is not None:
            question['selected'] = selected[1]
        else:
            question['selected'] = ''
    return raw_form
    
    
def flat(li):
    if len(li) > 1:
        return ''.join(str(i) for i in li)
    return li[0]
    
def get_progress(progress):
    return {attr:getattr(progress, attr) for attr in dir(progress) if attr.startswith('v')}

@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@main.route('/forms')
def forms():
    form_name = request.args.get('form_name', 'cover')
    status = request.args.get('status', 'v0')
    report_type = request.args.get('report_type', 'self_report')
    # load record if exits
    p_id = json.loads(session.get('patient', "{}")).get('id', 0)
    progress = surveymodels.Progress.query.filter_by(p_id=p_id).first()
    progress = get_progress(progress)
    if form_name is None:
        return render_template('allforms.html')
    elif form_name == 'cover':
        raw_form = getattr(raw_forms, form_name, None)
        patient = json.loads(session.get('patient', "{}"))
        record = models.Patient.query.filter_by(id=patient.get('id', 0)).first()
        previous, next = get_pager(report_type, status, form_name)
        options = dict(survey=raw_form, route='main.patient_regist', status=status, report_type=report_type,
        form_name=form_name, patient=patient, previous=previous, next=next, self_nav=schema.self_nav,
        other_nav=schema.other_nav, progress=progress)
        if record:
            data = dict(q_1=record.code, q_2=record.name, q_3=record.entry_date, q_4=record.doctor)
        else:
            data = dict()
        return render_template('rates/cover.html', data=data, **options)
    elif form_name == 'cover_other':
        raw_form = getattr(raw_forms, form_name, None)
        patient = json.loads(session.get('patient', "{}"))
        previous, next = get_pager(report_type, status, form_name)
        options = dict(survey=raw_form, route='main.recevie', status=status, report_type=report_type,
        form_name=form_name, patient=patient, previous=previous, next=next, self_nav=schema.self_nav,
        other_nav=schema.other_nav, progress=progress)
        return render_template('rates/cover_other.html', **options)
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
        form_name=form_name, patient=patient, previous=previous, next=next, self_nav=schema.self_nav,
        other_nav=schema.other_nav, progress=progress)
        return render_template('rates/{}.html'.format(form_name), **options)

@main.route('/selfreport')
def selfreport():
    status = request.args.get('status', 'v0')
    report_type = request.args.get('report_type', 'self_report')
    p_id = json.loads(session.get('patient', "{}")).get('id', 0)
    raw_form = getattr(raw_forms, 'cover', None)
    patient = json.loads(session.get('patient', "{}"))
    record = models.Patient.query.filter_by(id=patient.get('id', 0)).first()
    previous, next = get_pager(report_type, status, 'cover')
    progress = dict()
    options = dict(survey=raw_form, route='main.patient_regist', status=status, report_type=report_type,
    form_name='cover', patient=patient, previous=previous, next=next, self_nav=schema.self_nav,
    other_nav=schema.other_nav, progress=progress)
    if record:
        data = dict(q_1=record.code, q_2=record.name, q_3=record.entry_date, q_4=record.doctor)
    else:
        data = dict()
    return render_template('rates/cover.html', data=data, **options)
    
@main.route('/ohterreport')
def otherreport():
    form_name = request.args.get('form_name', 'cover_other')
    status = request.args.get('status', 'v0')
    report_type = request.args.get('report_type', 'other_report')
    p_id = json.loads(session.get('patient', "{}")).get('id', 0)
    raw_form = getattr(raw_forms, form_name, None)
    patient = json.loads(session.get('patient', "{}"))
    previous, next = get_pager(report_type, status, form_name)
    progress = dict()
    options = dict(survey=raw_form, route='main.recevie', status=status, report_type=report_type,
    form_name=form_name, patient=patient, previous=previous, next=next, self_nav=schema.self_nav,
    other_nav=schema.other_nav, progress=progress)
    return render_template('rates/cover_other.html', **options)
    
@main.route('/patient_regist', methods=['GET', 'POST'])
def patient_regist():
    if not current_user.is_authenticated:
        abort(403)
    data = [flat(request.form.getlist(attr)) for attr in sorted(request.form.keys()) if attr.startswith('q')]
    data = {k:v for k, v in zip(['code', 'name', 'entry_date', 'doctor'], data)}
    
    p = models.Patient.query.filter_by(code=data['code'], name=data['name'], doctor=data['doctor']).first()
    if p:
        for attr, val in data.items():
            setattr(p, attr, val)
    else:
        p = models.Patient(**data)
        p.recorder = current_user._get_current_object()
    try:
        db.session.add(p)
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
    
    try:
        progress = surveymodels.Progress(p_id=p.id, v0_cover=True)
        db.session.add(progress)
        db.session.commit()
    except IntegrityError as e:
        db.session.rollbakc()
    patient = dict()
    patient['name'] = request.form.get('q_2')
    patient['code'] = request.form.get('q_1')
    patient['id'] = p.id
    patient['writer'] = current_user.username
    session['patient'] = json.dumps(patient)
    return redirect(url_for('main.forms', status='v2', route='main.recevie', report_type='self_report', form_name='followup'))
    
@main.route('/logoutpatient')
@login_required
def logoutpatient():
    session['patient'] = "{}"
    flash('你已经退出填写')
    return redirect(url_for('main.get_all_patients'))
    
@main.route('/echo', methods=['GET', 'POST'])
def echo():
    patient = json.loads(session.get('patient', "{}"))
    data = []
    data.append('病人ID:' + str(patient.get('id', '')))
    data.append('随访窗:' + str(request.form.get('status')))
    data.append('量表名:' + str(reqeust.form.get('form_name')))
    answers = [attr + ': ' + flat(request.form.getlist(attr)) for attr in request.form.keys() if attr.startswith('q')]
    asnwers = sorted(answers)
    data.extend(answers)
    return render_template('echo.html', data=data)
    
@main.route('/recevie', methods=['GET', 'POST'])
def recevie():
    if not current_user.is_authenticated:
        abort(403)
    data = {attr:flat(request.form.getlist(attr)) for attr in request.form.keys() if attr.startswith('q')}
    patient = json.loads(session.get('patient', "{}"))
    if patient.get('id') is None:
        flash('请先填写病人信息,然后再填写量表')
        return redirect(url_for('main.forms', status='v0', route='main.recivie', report_type='self_report', form_name='cover'))
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
        for q_id, val in data.items():
            if q_id.startswith('q_'):
                setattr(record, q_id, val)
    try:
        db.session.add(record)
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        
    try:
        progress = surveymodels.Progress.query.filter_by(p_id=patient['id']).first()
        setattr(progress, request.form.get('status') + '_' + request.form.get('form_name'), True)
        db.session.add(progress)
        db.session.commit()
    except IntegrityError as e:
        print(e)
        db.session.rollback()
    data = []
    data.append('病人ID:' + str(patient.get('id', '')))
    data.append('随访窗:' + str(request.form.get('status')))
    data.append('量表名:' + str(request.form.get('form_name')))
    attrs = [attr for attr in request.form.keys() if attr.startswith('q')]
    attrs = sorted(attrs)
    answers = [attr + ': ' + flat(request.form.getlist(attr)) for attr in attrs]
    data.extend(answers)
    return render_template('echo.html', data=data, previous=request.referrer)
    
@main.route('/patients')
@login_required
def get_all_patients():
    patients = current_user.patients
    return render_template('patients.html', patients=patients)
    
@main.route('/editpatient')
@login_required
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
@login_required
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
    progress = surveymodels.Progress.query.filter_by(p_id=p_id).first()
    db.session.delete(patient)
    db.session.delete(progress)
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
    p_finished = p_finished.finished if p_finished else False
    username = u.username
    email = u.email
    project = u.project.name
    return render_template('user.html', u=u, finished=finished, unfinished=unfinished, total=total,
        p_name=p_name, p_code=p_code, p_finished=p_finished, username=username, email=email, project=project)

@main.route('/ajax/delete/<int:id>')
def ajax_delete(id):
    form_name = request.args.get('form_name')
    model = getattr(surveymodels, form_name.upper())
    if model:
        record = model.query.filter_by(id=id).first()
        if record:
            db.session.delete(record)
            db.session.commit()
            return "True"
        else:
            print("删除失败")
            return "False"

@main.route('/ajax/<int:id>', methods=['GET', 'POST'])
def ajax_submit(id):
    form_name = request.form.get('form_name')
    p_id = json.loads(session.get('patient', '{}')).get('id')
    status = request.form.get('status')
    model = getattr(surveymodels, form_name.upper())
    if model:
        record = model.query.filter_by(id=id).first()
        if record:
            for attr in request.form.keys():
                if attr.startswith('q_'):
                    setattr(record, attr, request.form[attr])
        else:
            data = {k:v for k, v in request.form.items() if k.startswith('q_')}
            data['p_id'] = p_id
            data['status'] = status
            record = model(**data)
        db.session.add(record)
        db.session.commit()
        progress = surveymodels.Progress.query.filter_by(p_id=p_id).first()
        setattr(progress, status + '_' + form_name, True)
        db.session.add(progress)
        db.session.commit()
    return str(record.id)
    
@main.route('/ajax/preload/', methods=['GET', 'POST'])
def ajax_preload():
    form_name = request.form.get('form_name')
    status = request.form.get('status')
    p_id = json.loads(session.get('patient', '{}')).get('id')
    records = getattr(surveymodels, form_name.upper()).query.filter_by(p_id=p_id, status=status).all()
    def get_input(record):
        attrs = [attr for attr in dir(record) if attr.startswith('q_')]
        attrs = sorted(attrs, key=lambda item: tuple(int(i) for i in item.split('_')[1:]))
        result = dict()
        result['questions'] = [getattr(record, attr) for attr in attrs]
        result['id'] = record.id
        return result
    records = [get_input(record) for record in records]
    return json.dumps(dict(p_id=p_id, records=records))
