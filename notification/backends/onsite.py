from notification import backends
from notification.models import Notice
from django.utils.translation import ugettext

class OnSiteBackend(backends.BaseBackend):

    def can_send(self, user, notice_type):
        can_send = super(EmailBackend, self).can_send(user, notice_type)
        if can_send:
            return True
        return False

    def deliver(self, recipient, sender, notice_type, extra_context):
        Notice.objects.create(recipient=recipient,
                                           notice_type=notice_type,
                                           sender=sender,
                                           message=ugettext(notice_type.display),
                                           on_site=True)