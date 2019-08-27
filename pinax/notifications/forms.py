from old_dal.widgets import ChoiceWidget

from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import NoticeSetting

MEDIUM_TYPES = (
    ('', ''),
    (0, _('Email')),
    (1, _('On Site')),
)


class NoticeSettingForm(forms.ModelForm):

    class Meta(object):
        model = NoticeSetting
        widgets = {
            'user': ChoiceWidget('UserAdminAutocomplete'),
        }
        exclude = ()
