from django.contrib.admin import sites

# ---------------------------------------------------------------------------------------------------------------------
class AdminSite(sites.AdminSite):
    """
    Represents the administration, where only authorized users have access.
    """

    def index(self, request, extra_context=None):
        response = super(AdminSite, self).index(request, extra_context)
        response.context_data['title'] = 'Adminstration Site'

        return response

    def app_index(self, request, app_label, extra_context=None):
        response = super(AdminSite, self).app_index(request, app_label, extra_context)

        return response

# ---------------------------------------------------------------------------------------------------------------------
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