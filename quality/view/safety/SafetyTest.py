# -*- coding:utf-8 -*-
# Author:heliangliang
from django.http.response import JsonResponse
import json, re, requests, ast, datetime
from quality.common.commonbase import commonList
from django.core import serializers
from quality.common.logger import Log
from quality.common.msg import msgMessage, msglogger
from quality.common.msg import loginRequired
import copy, re
log = Log()





