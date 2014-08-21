from django.contrib.admin import sites
from django.contrib.admin.actions import delete_selected


class AdminSite(sites.AdminSite):
    """
    Represents the administration, where only authorized users have access.
    """
    def __init__(self, *args, **kwargs):
        super(AdminSite, self).__init__(*args, **kwargs)
        self.disable_action('delete_selected')
        self.add_action(self._delete_selected, 'delete_selected')

    @staticmethod
    def _delete_selected(modeladmin, request, queryset):
        _delete_qs = queryset.delete

        def delete():
            for obj in queryset:
                modeladmin.delete_model(request, obj)
            _delete_qs()

        queryset.delete = delete
        return delete_selected(modeladmin, request, queryset)

    def index(self, request, extra_context=None):
        response = super(AdminSite, self).index(request, extra_context)
        response.context_data['title'] = 'Adminstration Site'

        return response

    def app_index(self, request, app_label, extra_context=None):
        response = super(AdminSite, self).app_index(request, app_label, extra_context)

        return response


class PublicSite(sites.AdminSite):
    """
    Is the public part of the site where the plugins will make the necessary adjustments in the content.
    """

    def index(self, request, extra_context=None):
        response = super(PublicSite, self).index(request, extra_context)

        response.template_name = ['admin_index.html']
        response.context_data['title'] = 'Public site'

        return response

    def app_index(self, request, app_label, extra_context=None):
        response = super(PublicSite, self).app_index(request, app_label, extra_context)

        return response