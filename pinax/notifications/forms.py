from django import forms

from dal import autocomplete

from .models import NoticeSetting, Notice


class NoticeSettingForm(forms.ModelForm):
    class Meta:
        model = NoticeSetting
        widgets = {
            'user': autocomplete.ModelSelect2(
                url='autocomplete:user-autocomplete',
            ),
            'notice_type': autocomplete.ModelSelect2(
                url='autocomplete:noticetype-autocomplete',
            ),
        }
        exclude = ()

