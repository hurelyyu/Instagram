#from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.
# HelloWorld inherent TemplateView
class HelloWorld(TemplateView):
    template_name = 'test.html'

