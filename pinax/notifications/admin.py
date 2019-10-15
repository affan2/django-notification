from django.contrib import admin

from .models import NoticeType, NoticeSetting, Notice, NoticeQueueBatch
from .forms import NoticeSettingForm


class NoticeTypeAdmin(admin.ModelAdmin):
    list_display = ["label", "display", "past_tense", "description", "state", "default", ]
    list_editable = ('state', )

    search_fields = ('label', )


class NoticeSettingAdmin(admin.ModelAdmin):
    list_display = ["id", "get_user", "get_notice_type", "medium", "send"]
    search_fields = ('user__email', 'user__first_name', 'notice_type__label', )
    form = NoticeSettingForm

    exclude = ('scoping_content_type', 'scoping_object_id', 'scoping', )

    def get_user(self, obj):
        return obj.user
    get_user.short_description = 'user'

    def get_notice_type(self, obj):
        return obj.notice_type
    get_notice_type.short_description = 'notice_type'


class NoticeAdmin(admin.ModelAdmin):
    list_display = ["message", "recipient", "sender", "notice_type", "added", "unseen", "archived", "on_site"]

    autocomplete_fields = ('recipient', 'sender', 'notice_type', )


admin.site.register(NoticeQueueBatch)
admin.site.register(NoticeType, NoticeTypeAdmin)
admin.site.register(NoticeSetting, NoticeSettingAdmin)
admin.site.register(Notice, NoticeAdmin)
