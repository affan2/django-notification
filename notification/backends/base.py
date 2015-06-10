from django.conf import settings
from django.template import Context
from django.template.loader import render_to_string

from django.contrib.sites.models import Site


class BaseBackend(object):
    """
    The base backend.
    """
    def __init__(self, medium_id, spam_sensitivity=None):
        self.medium_id = medium_id
        if spam_sensitivity is not None:
            self.spam_sensitivity = spam_sensitivity

    def can_send(self, user, notice_type):
        """
        Determines whether this backend is allowed to send a notification to
        the given user and notice_type.
        """
        from notification.models import NoticeSetting
        if notice_type.state < 1:
            return False
        return NoticeSetting.for_user(user, notice_type, self.medium_id).send

    def deliver(self, recipient, sender, notice_type, extra_context):
        """
        Deliver a notification to the given recipient.
        """
        raise NotImplementedError()

    def get_formatted_messages(self, formats, label, context):
        """
        Returns a dictionary with the format identifier as the key. The values are
        are fully rendered templates with the given context.
        """
        format_templates = {}
        for fmt in formats:
            # conditionally turn off autoescaping for .txt extensions in format
            if fmt.endswith(".txt"):
                context.autoescape = False
            format_templates[fmt] = render_to_string((
                "notification/%s/%s" % (label, fmt),
                "notification/%s" % fmt), context_instance=context)
        return format_templates

    def default_context(self):
        default_http_protocol = getattr(settings, "DEFAULT_HTTP_PROTOCOL", "http")
        current_site = Site.objects.get_current()
        base_url = "%s://%s" % (default_http_protocol, current_site.domain)
        return Context({
            "default_http_protocol": default_http_protocol,
            "current_site": current_site,
            "current_site_name": current_site.name,
            "base_url": base_url
        })

    def get_target_url(self, extra_context, sender, recipient):
        target_url = extra_context['target'].url if 'target' in extra_context and hasattr(extra_context['target'],
                                                                                          'url') else sender.get_absolute_url()
        if 'target' in extra_context and recipient == extra_context['target']:
            target_url = sender.get_absolute_url()
        if 'pm_message' in extra_context:
            target_url = extra_context['pm_message'].get_absolute_url()
        if hasattr(target_url, '__call__'):
            target_url = target_url()

        return target_url

