#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    DEBUG = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'testing'

    @staticmethod
    def init_app(app):
        pass

config = {'default': Config}
