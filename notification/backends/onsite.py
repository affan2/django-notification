from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.contrib.auth.models import User
from django.template import Context
from django.utils.translation import ugettext
from django.utils import translation

from notification import backends


class OnSiteBackend(backends.BaseBackend):
    spam_sensitivity = 0

    def can_send(self, user, notice_type):
        can_send = super(OnSiteBackend, self).can_send(user, notice_type)
        if can_send:
            return True
        return False

    def deliver(self, recipient, sender, notice_type, extra_context):
        from notification.models import Notice

        if 'disallow_notice' in extra_context:
            if 'onsite' in extra_context['disallow_notice']:
                return

        recipient = User.objects.get(id=recipient.id)
        language_code = 'en'
        if 'language_code' in extra_context.keys():
            for language_tuple in settings.LANGUAGES:
                if extra_context['language_code'] in language_tuple:
                    language_code = language_tuple[0]
                    break
        else:
            try:
                language_code = recipient.user_profile.default_language
            except ObjectDoesNotExist:
                language_code = 'en'

        translation.activate(language_code)
        if 'target' in extra_context and hasattr(extra_context['target'], 'translations'):
            from general.utils import switch_language
            target = extra_context['target']
            extra_context['target'] = switch_language(target, language_code)

        if 'pm_message' in extra_context:
            sender = extra_context['pm_message'].sender

        target_url = self.get_target_url(extra_context, sender, recipient)

        context = Context({})
        context.update({
            "recipient": recipient,
            "sender": sender,
            "notice": ugettext(notice_type.past_tense),
            'default_profile_photo': settings.DEFAULT_PROFILE_PHOTO,
            'target_url': target_url,
        })
        context.update(extra_context)

        try:
            messages = self.get_formatted_messages((
                "full.html",
            ), context['app_label'], context)

        except:
            messages = self.get_formatted_messages((
                "full.html",
            ), notice_type.label, context)

        if sender.__class__.__name__ == 'Company':
            sender = sender.admin_primary if sender.admin_primary else sender.created_by

        if settings.PRODUCTION_SETTING and recipient.is_active:
            Notice.objects.create(
                recipient=recipient,
                notice_type=notice_type,
                sender=sender,
                message=messages['full.html'],
                on_site=True,
                target_url=target_url
            )