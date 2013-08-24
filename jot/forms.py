from django import forms
from models import (
    OneLiner, Note
)

class OneLinerForm(forms.ModelForm):
    class Meta:
        widgets = {'object_id': forms.Select()}
        model = OneLiner
        
class NoteForm(forms.ModelForm):
    class Meta:
        widgets = {'object_id': forms.Select()}
        model = Note
