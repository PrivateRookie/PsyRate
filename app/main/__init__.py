# -*- coding: utf-8 -*-
from flask import Blueprint

main = BluePrint('main', __name__)

from . import views, errors

