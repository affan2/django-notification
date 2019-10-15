from django import forms
from django.utils.translation import ugettext_lazy as _

from dal import autocomplete

from .models import NoticeSetting

MEDIUM_TYPES = (
    ('', ''),
    (0, _('Email')),
    (1, _('On Site')),
)


class NoticeSettingForm(forms.ModelForm):
    class Meta:
        model = NoticeSetting
        widgets = {
            'user': autocomplete.ModelSelect2(
                url='user-autocomplete',
            ),
            'notice_type': autocomplete.ModelSelect2(
                url='noticetype-autocomplete',
            ),
        }
        exclude = ()
