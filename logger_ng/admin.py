#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4
# maintainer: katembu

from django.contrib import admin
from logger_ng.models import LoggedMessage


class LoggedMessageAdmin(admin.ModelAdmin):
    '''
    Custom ModelAdmin to be used for the LoggedMessage field. Enables
    filtering, searching (name and text fields), and the slick built-in
    django date-higherarchy widget.
    '''
    list_display = ('date', '__unicode__')
    list_filter = ['direction', 'date', 'site']
    date_hierarchy = 'date'
    search_fields = ['text']
admin.site.register(LoggedMessage, LoggedMessageAdmin)
