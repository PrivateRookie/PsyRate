# -*- coding: utf-8 -*-
import os
from app import create_app, db

app = create_app(os.getenv('FLASK_CONFIG'))