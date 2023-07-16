from django.forms import ModelForm

from TODO.models import TODO

class TODOForm(ModelForm):
    class Meta:
        model=TODO
        fields=['title','status','priority']