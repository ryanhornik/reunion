from django.contrib import admin
from django.utils.html import format_html

from reunionsite.models import Person, Email, Marriage


class PersonAdmin(admin.ModelAdmin):
    fields = ('first_name', 'last_name', 'email_addresses', 'spouse')
    readonly_fields = ('email_addresses', 'spouse')
    list_display = ('first_name', 'last_name')

    def email_addresses(self, obj):
        html = '<table>' \
               '<thead><tr><th>Address</th></tr></thead>' \
               '<tbody>'
        for e in obj.email_addresses.all():
            html += format_html('<tr><td><a href="/admin/reunionsite/email/{}/change">{}</a></td></tr>',
                                e.pk, e.email_address)
        html += '</tbody></table>'
        return format_html(html)


class EmailAdmin(admin.ModelAdmin):
    list_display = ('email_address', 'owner')
    list_filter = ('owner',)
    search_fields = ('owner__first_name', 'owner__last_name')


class MarriageAdmin(admin.ModelAdmin):
    list_display = ('pk', 'spouse_a', 'spouse_b', 'status')


admin.site.register(Person, PersonAdmin)
admin.site.register(Email, EmailAdmin)
admin.site.register(Marriage, MarriageAdmin)
