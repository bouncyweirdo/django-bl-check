from django.contrib import admin
from django.contrib import messages
from django.contrib.postgres.fields import JSONField
from django import forms

from .models import *
from .utils import check_ip_status, check_bl
from .widgets import SplitJSONWidget


def update_ip_status(modeladmin, request, queryset):
    for ip in queryset:
        check_ip_status(ip)
    messages.info(request, 'Selected IPs were updated.')
update_ip_status.short_description = "Update ip status"


def update_ip_blacklist(modeladmin, request, queryset):
    for ip in queryset:
        check_bl(ip)
    messages.info(request, 'Selected IPs were updated.')
update_ip_blacklist.short_description = "Update ip blacklist"


class IpAddressAdminForm(forms.ModelForm):
    class Meta:
        model = IpAddress
        fields = '__all__'

    def clean_address(self):
        address = self.cleaned_data['address']
        if IpAddress.objects.filter(address=address).exists():
            raise forms.ValidationError("An entry with same ip already exists.")
        return address


class IpAddressAdmin(admin.ModelAdmin):
    form = IpAddressAdminForm
    list_display = ("address", "hostname", "rdns", "status", "enabled", "blacklisted", "critical_blacklisted")
    search_fields = ["address", "hostname", "rdns"]
    list_filter = ("status", "enabled", "blacklisted", "critical_blacklisted")
    actions = [update_ip_status, update_ip_blacklist]
    formfield_overrides = {
        JSONField: {'widget': SplitJSONWidget},
    }

    def get_queryset(self, request):
        """Limit Pages to those that belong to the request's user."""
        qs = super(IpAddressAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            # It is mine, all mine. Just return everything.
            return qs

        # Now we just add an extra filter on the queryset and
        # we're done. Assumption: Page.owner is a foreignkey
        # to a User.
        return qs.filter(user=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'user':
            kwargs['initial'] = request.user.id
        return super(IpAddressAdmin, self).formfield_for_foreignkey(
            db_field, request, **kwargs
        )


class DnsBlacklistAdminForm(forms.ModelForm):
    class Meta:
        model = DnsBlacklist
        fields = '__all__'

    def clean_dns(self):
        dns = self.cleaned_data['dns']
        if DnsBlacklist.objects.filter(dns=dns).exists():
            raise forms.ValidationError("An entry with same dns already exists.")
        return dns


class DnsBlacklistAdmin(admin.ModelAdmin):
    form = DnsBlacklistAdminForm
    list_display = ['dns', ]


admin.site.register(IpAddress, IpAddressAdmin)
admin.site.register(DnsBlacklist, DnsBlacklistAdmin)
