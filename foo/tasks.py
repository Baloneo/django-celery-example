# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task

from celerypro.celery import app


@app.task
def foo():
    print('hello')

@app.task
def per_foo():
    print('per hello')

