from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseForbidden


def get_objects_for_fk(request, ct_id=None):
    if request.user.is_authenticated() and request.is_ajax() and ct_id:
        ct = ContentType.objects.get_for_id(ct_id)
        data = {'options': ct.get_all_objects_for_this_type()}

        return render(request, 'admin/options.html', data)
    else:
        return HttpResponseForbidden()
