from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from parler.admin import TranslatableAdmin
from domestique.models import Client, Provider, Admin, Service, Request, Response

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone', 'is_active', 'created_at')
    search_fields = ('first_name', 'last_name', 'email')
    list_filter = ('is_active',)
    actions = ['activate_users', 'deactivate_users']

    def activate_users(self, request, queryset):
        queryset.update(is_active=True)
    activate_users.short_description = _("Activate selected users")

    def deactivate_users(self, request, queryset):
        queryset.update(is_active=False)
    deactivate_users.short_description = _("Deactivate selected users")

@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone', 'is_approved', 'is_active', 'created_at')
    search_fields = ('first_name', 'last_name', 'email')
    list_filter = ('is_approved', 'is_active')
    filter_horizontal = ('skills',)
    actions = ['approve_providers', 'deactivate_providers']

    def approve_providers(self, request, queryset):
        queryset.update(is_approved=True)
    approve_providers.short_description = _("Approve selected providers")

    def deactivate_providers(self, request, queryset):
        queryset.update(is_active=False)
    deactivate_providers.short_description = _("Deactivate selected providers")

@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone', 'is_superuser', 'created_at')
    search_fields = ('first_name', 'last_name', 'email')

@admin.register(Service)
class ServiceAdmin(TranslatableAdmin):
    list_display = ('name', 'category')
    search_fields = ('translations__name', 'category')
    list_filter = ('category',)

@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ('client', 'service', 'status', 'price', 'created_at')
    list_filter = ('status', 'service')
    search_fields = ('client__first_name', 'client__last_name')
    actions = ['cancel_request']

    def cancel_request(self, request, queryset):
        queryset.update(status='CANCELLED')
    cancel_request.short_description = _("Cancel selected requests")

@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    list_display = ('request', 'provider', 'proposed_price', 'created_at')
    search_fields = ('provider__first_name', 'provider__last_name')
    list_filter = ('request__status',)