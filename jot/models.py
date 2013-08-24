from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.conf import settings

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')
JOT_MESSAGE_LEVEL = 23

class JotGenericRelationModel(models.Model):
    date = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now_add=True, editable=False)
    created_by = models.ForeignKey(AUTH_USER_MODEL)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey("content_type", "object_id")
    personal = models.BooleanField(_('Is Personal?'), default=False)

    class Meta:
        abstract = True

class OneLiner(JotGenericRelationModel):
    content = models.CharField(_('Content'), max_length=255)

    def get_delete_url(self):
        return reverse('admin:jot_oneliner_delete', args=(self.id,))

    def get_absolute_url(self):
        return reverse('admin:jot_oneliner_change', args=(self.id,))

    def __unicode__(self):
        return u"{cont_type}: {content}".format(
            cont_type = self.content_type,
            content = self.content
            )

    class Meta:
        ordering = ["date"]
        verbose_name = _('One Liner')
        verbose_name_plural = _('One Liners')
        permissions = (
            ("view_oneliner", _("Can view One Liner")),
            )

class Note(JotGenericRelationModel):
    content = models.TextField(_('Content'))

    def get_delete_url(self):
        return reverse('admin:jot_note_delete', args=(self.id,))

    def get_absolute_url(self):
        return reverse('admin:jot_note_change', args=(self.id,))

    def __unicode__(self):
        return u"{cont_type}: {content}".format(
            cont_type = self.content_type,
            content = self.content
            )

    class Meta:
        ordering = ["date"]
        verbose_name = _('Note')
        verbose_name_plural = _('Notes')
        permissions = (
            ("view_note", _("Can view Notes")),
            )
