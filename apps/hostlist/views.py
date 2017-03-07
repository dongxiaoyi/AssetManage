#_*_encoding:utf-8_*_
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.backends import  ModelBackend
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse,HttpResponseRedirect
from django.views.generic.base import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt
from . import core, models, asset_handle, utils,tables,adminx
from .dashboard import  AssetDashboard
from django.contrib.auth.decorators import login_required
from users.utils.mixin_utils import LoginRequiredMixin
import json,logging
import xadmin
from .models import Dzhuser, DataCenter, AccHostList

