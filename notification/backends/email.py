from django.conf import settings
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.utils.translation import ugettext
from django.utils import translation

from notification import backends


class EmailBackend(backends.BaseBackend):
    spam_sensitivity = 0

    def can_send(self, user, notice_type):
        can_send = super(EmailBackend, self).can_send(user, notice_type)
        if can_send and user.email:
            return True
        return False

    def deliver(self, recipient, sender, notice_type, extra_context):
        # TODO: require this to be passed in extra_context
        #postman stuff
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

        if 'disallow_notice' in extra_context:
            if 'email' in extra_context['disallow_notice']:
                return

        if 'pm_message' in extra_context:
            sender = extra_context['pm_message'].sender

        target_url = self.get_target_url(extra_context, sender, recipient)

        context = self.default_context()
        context.update({
            "recipient": recipient,
            "sender": sender,
            "notice": ugettext(notice_type.past_tense),
            'default_profile_photo': settings.DEFAULT_PROFILE_PHOTO,
            'target_url': target_url,
        })
        context.update(extra_context)

        try:
            messages = self.get_formatted_messages(( "short.txt", "full.txt",), context['app_label'], context)

        except:
            messages = self.get_formatted_messages((
                "short.txt",
                "full.txt",
            ), notice_type.label, context)

        subject = "".join(render_to_string("notification/email_subject.txt", {
            "message": messages["short.txt"],
        }, context).splitlines())

        body = render_to_string("notification/email_body.txt", {
            "message": messages["full.txt"],
        }, context)
        recipients = ['"%s" <%s>' % (recipient.get_full_name(), recipient.email)]

        if settings.PRODUCTION_SETTING:
            send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, recipients)
        else:
            for admin in settings.ADMINS:
                user = User.objects.get(email=admin[1])
                recipients = ['"%s" <%s>' % (user.get_full_name(), user.email)]
                send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, recipients)