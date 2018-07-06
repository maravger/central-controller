from __future__ import absolute_import, unicode_literals
from logging import Logger
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from celery import task
from django.db import OperationalError
from django.conf import settings
import logging
import subprocess
import requests
import os
from api.views import optimizer
from api.views import workload_predictor
from django.conf import settings
from api.models import App
from django.core.exceptions import ObjectDoesNotExist


# Get an instance of a logger
logger = logging.getLogger(__name__)  # type: Logger

@task()
def scale_horizontally():
    #TODO find a better way to initiate app creation
    for app_id in settings.GLOBAL_SETTINGS['APPS']:
        try:
            App.objects.get(app_id=app_id)
        except ObjectDoesNotExist:
            temp = App(app_id=app_id)
            temp.save()
    total_combinations = optimizer.permutate()
    print total_combinations
    predicted_workload = workload_predictor.predict()
    print predicted_workload
    selected_combinations = optimizer.optimize(total_combinations, predicted_workload)
    print selected_combinations
