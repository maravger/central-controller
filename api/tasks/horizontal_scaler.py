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

