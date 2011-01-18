simple-locations fork by Alan Viars
===================================

A simple Locations (Area, AreaType, Point) model for Django/RapidSMS applications.

Alan Viars Fork Modifications
==============================
Setup simple_locations and made custom modifications to support iso country codes.

- Built an "auto-slug" maker into the Area Type admin interface.  Also a slight improvement to simple_locations.

-Loaded initial "Area Type" data.  Built a fixture and setup as initial data so this data is loaded automatically when someone has a new database and performs a 'syncdb'.

- Built a tool so we can use an  iso country code tables file and easily convert it into tulple pairs.  This is for dropdowns/verification, etc.  In other words, this means if country codes change it will be trivial to reload them.  I called this 'buildiso.py' and is in the simple-locations.


Dependencies
============

* django-mptt
* `code_generator <http://github.com/yeleman/code_generator>`_
