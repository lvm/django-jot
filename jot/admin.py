from django import VERSION as django_version
from django.contrib import admin
from django.contrib import messages
from django.template.defaultfilters import (
    linebreaksbr, removetags
)
from django.contrib.humanize.templatetags.humanize import naturalday
from django.contrib.contenttypes.models import ContentType
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from django import forms
from django.conf import settings
from itertools import chain
from operator import attrgetter
from models import (
    OneLiner, Note, JOT_MESSAGE_LEVEL
)
from forms import (
    OneLinerForm, NoteForm
)

def notify_if_not_duplicate(request, item):
    the_message_content = mark_safe("""<strong><a title='{dismiss_title}' 
                                href='{dismiss_url}'>&times;</a></strong>
                                <small><em>{date}</em></small>,
                                <strong>{created_by}</strong>:
                                {message}""".format(
                    created_by=item.created_by,
                    date=naturalday(item.date),
                    message=linebreaksbr(removetags(item.content,'script')),
                    dismiss_title=_('Dismiss'),
                    dismiss_url=item.get_delete_url()
                    ))

    jot_messages = [msg for msg in messages.get_messages(request) \
                        if msg.level == JOT_MESSAGE_LEVEL]
    in_jot_messages = [msg for msg in jot_messages \
                           if msg.message == the_message_content]

    if not in_jot_messages:
        messages.add_message(request, JOT_MESSAGE_LEVEL,
                             the_message_content, fail_silently=True)

def jot_notifications(request, ModelContentType, obj_id):
    filter_by = {'content_type':ModelContentType,
                 'object_id':obj_id
                 }

    oneliners = OneLiner.objects.filter(**filter_by)
    notes = Note.objects.filter(**filter_by)
    items = sorted(chain(oneliners, notes), 
                   key=attrgetter('date'))

    for item in items:
        if item.personal:
            if item.created_by == request.user:
                notify_if_not_duplicate(request, item)
        else:
            notify_if_not_duplicate(request, item)
            

    return {'jot_notifications': "{n} items".format(n=len(items))}

class JotNotifications(admin.options.BaseModelAdmin):
    def change_view(self, request, object_id, form_url='', extra_context=None):
        ct = ContentType.objects.get_for_model(self.model)
        jot_notifications(request, ct, object_id)
        return super(JotNotifications, self).change_view(request, object_id,
                                                   form_url, 
                                                   extra_context)

class NoteAdmin(JotNotifications, admin.ModelAdmin):
    form = NoteForm
    change_form_template = 'admin/change_form_jot.html'

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['jot_ajax_error_msg'] = _('Oops, something went wrong loading child objects')
        return super(type(self), self).change_view(request, object_id,
                                                   form_url,
                                                   extra_context)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "created_by":
            kwargs["initial"] = request.user

        return super(type(self), self).formfield_for_foreignkey(db_field,
                                                                request, **kwargs)

    class Media:
        # FIXME:TODO:TOREVIEW
        # crappy version comparison
        if django_version <= (1,6):
            js = ('{static}/js/jquery.js'.format(static=settings.STATIC_URL),
                  '{static}/js/jot.forms.js'.format(static=settings.STATIC_URL),
                  )
        else:
            js = ('{static}/js/jot.forms.js'.format(static=settings.STATIC_URL))

class OneLinerAdmin(JotNotifications, admin.ModelAdmin):
    form = OneLinerForm
    change_form_template = 'admin/change_form_jot.html'


    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "created_by":
            kwargs["initial"] = request.user

        return super(type(self), self).formfield_for_foreignkey(db_field,
                                                                request, **kwargs)

    class Media:
        # FIXME:TODO:TOREVIEW
        # crappy version comparison
        if django_version <= (1,6):
            js = ('{static}/js/jquery.js'.format(static=settings.STATIC_URL),
                  '{static}/js/jot.forms.js'.format(static=settings.STATIC_URL),
                  )
        else:
            js = ('{static}/js/jot.forms.js'.format(static=settings.STATIC_URL))

admin.site.register(OneLiner, OneLinerAdmin)
admin.site.register(Note, NoteAdmin)
