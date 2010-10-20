#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from simple_locations.models import Area,Point
from django.conf import settings
from django.utils import simplejson
from django.http import HttpResponse
from django.utils.safestring import mark_safe
from forms import LocationForm
from django.http import HttpResponseRedirect
from mptt.exceptions import InvalidMove
from django.views.decorators.cache import cache_control
from django.template.loader import get_template
from django.template.context import Context

import decimal

#firefox likes to aaggressively cache forms set cache control to false to override this
@cache_control(no_cache=True)
def simple_locations(request):
    form = LocationForm()
    nodes=Area.tree.all()
    return render_to_response(
          'simple_locations/index.html', 
          {'form' : form,
           'nodes':nodes, 
        },
          context_instance=RequestContext(request))

def add_location(req, parent_id=None):
    nodes = Area.tree.all()
    form_errors=True
        
    if req.method == 'POST':
        form = LocationForm(req.POST)
        if form.is_valid():
        
            name = form.cleaned_data['name']
            code = form.cleaned_data['code']
            lat=form.cleaned_data['lat']
            lon=form.cleaned_data['lon']
            target = form.cleaned_data['target']
            position = form.cleaned_data['position']
            
            location=Point(latitude=lat,longitude=lon)
            location.save()
            area=Area(name=name,code=code)
            area.location=location
            area.save()
            if form.cleaned_data['move_choice']:
                try:
                    Area.tree.move_node(area, target, position)
                except InvalidMove:
                    pass 
            form = LocationForm()
            return render_to_response(
        'simple_locations/location_edit.html'
        ,{'form': form, 'nodes': nodes},
        context_instance=RequestContext(req)) 
            
    else:
        if (parent_id):
            default_data = {}            
            parent = get_object_or_404(Area, pk=parent_id)
            default_data['move_choice'] = True
            default_data['target'] = parent.pk
            default_data['position'] = 'last-child'
            form = LocationForm(default_data)
            form_errors=True
            
        else:
            form = LocationForm()

    return render_to_response(
        'simple_locations/location_edit.html'
        ,{'form': form, 'nodes': nodes,'form_errors':form_errors},
        context_instance=RequestContext(req))    
    

def edit_location(req, area_id):
    location = get_object_or_404(Area, pk=area_id)
    if req.method == 'POST':
        form = LocationForm(req.POST)
        if form.is_valid():
            
            area = Area.objects.get(pk=area_id)
            name = form.cleaned_data['name']
            code = form.cleaned_data['code']
            lat=form.cleaned_data['lat']
            lon=form.cleaned_data['lon']
            location=Point(latitude=lat,longitude=lon)
            location.save()
            area.location=location
            area.location.save()
            area.save()
            if form.cleaned_data['move_choice']:
                target = form.cleaned_data['target']
                position = form.cleaned_data['position']
                
                try:
                    Area.tree.move_node(area, target, position)
                except InvalidMove:
                    pass
            return render_to_response("simple_locations/location_edit.html", {"form":LocationForm(), 'nodes':Area.tree.all()}, context_instance=RequestContext(req))
        else:
            return render_to_response("simple_locations/location_edit.html", 
                                      { 'form': form, 'item': location },
                                      context_instance=RequestContext(req))
    else:
        default_data = {}
        default_data['pk'] = location.pk
        default_data['name'] = location.name
        default_data['code'] = location.code
        default_data['move_choice'] = False
        if location.parent:
            default_data['target'] = location.parent
            default_data['position'] = 'last-child'
        if location.location:
            default_data['lat'] = location.location.latitude
            default_data['lon'] = location.location.longitude
        form = LocationForm(default_data)
        return render_to_response("simple_locations/location_edit.html", {'form':form, 'nodes':Area.tree.all(),'item':location}, context_instance=RequestContext(req))



def delete_location(request, area_id):
    node = get_object_or_404(Area, pk=area_id)
    if request.method == 'POST':
        node.delete()

    return HttpResponseRedirect('/simple_locations/render_tree')

@cache_control(no_cache=True)
def render_location(request):
    nodes = Area.tree.all()
    return render_to_response('simple_locations/treepanel.html',{'nodes':nodes})