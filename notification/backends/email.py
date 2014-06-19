from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.translation import ugettext

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

        context = self.default_context()
        context.update({
            "recipient": recipient,
            "sender": sender,
            "notice": ugettext(notice_type.past_tense),
        })
        context.update(extra_context)
        context.update({'notice_type': notice_type, 'sender': sender})

        target_url = extra_context['target'].url if hasattr(extra_context['target'], 'url') else sender.get_absolute_url
        if recipient == extra_context['target']:
            target_url = sender.get_absolute_url()

        context.update({'target_url': target_url})

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

        recipients = ['%s <%s>' % (recipient.get_full_name(), recipient.email)]
        send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, recipients)
