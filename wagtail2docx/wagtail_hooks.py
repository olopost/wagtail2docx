from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register, ModelAdminGroup
from django.views.generic.base import TemplateView
from django.urls import reverse
from django.http import HttpResponse
from django.conf.urls import url
from django.contrib.auth.models import Permission
from wagtail.admin.menu import MenuItem

class SettingView(TemplateView):
    """
    Letter DL format pdf generation
    """

    template_name = "setting.html"

    def post(self, request, *args, **kwargs):
        response = HttpResponse(content_type='application/pdf')
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def will_modify_explorer_page_queryset(self):
        return False

    def get_admin_urls_for_registration(self):
        urls = (url(r'^wagtail2docx/$', SettingView.as_view(), name='view_env'),)
        return urls

    def get_menu_item(self, order=None):
        return MenuItem('W2D - Setting', reverse("view_env"), classnames='icon icon-cog', order=10000)

    def get_permissions_for_registration(self):
        return Permission.objects.none()

class W2D_Group(ModelAdminGroup):
    """
    SME Admin menu
    """
    menu_label = "Wagtail2Docx"
    items = (SettingView,)

modeladmin_register(W2D_Group)
