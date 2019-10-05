from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register, ModelAdminGroup
from django.views.generic.base import TemplateView
from django.urls import reverse
from django.http import HttpResponse
from django.conf.urls import url
from django.contrib.auth.models import Permission
from wagtail.core.models import Page
from django.conf import settings
from docxtpl import DocxTemplate, RichText, Subdoc
from wagtail.core.blocks.base import BoundBlock
import os
from wagtail.admin.menu import MenuItem
from bs4 import BeautifulSoup
import bs4

class SettingView(TemplateView):
    """
    Setting view
    """

    template_name = "setting.html"

    def html2sb(self, html, doc):
        ret = doc.new_subdoc()
        p = ret.add_paragraph()
        soup = BeautifulSoup(html, 'html.parser')
        for i in soup.descendants:
            if type(i) is bs4.element.NavigableString:
                if i.parent.name == 'i':
                    p.add_run(str(i)).italic = True
                elif i.parent.name == 'b':
                    p.add_run(str(i)).bold = True
                else:
                    p.add_run(str(i))
            if i.name == 'div':
                p = ret.add_paragraph()
        return ret

    def get_page(self, id, doc):
        context = {}
        try:
            id = int(id)
        except:
            return context.update({'error': 'id value is not int'})
        page = Page.objects.filter(id=id)
        if len(page) <= 0:
            return context.update({'error': f'Page {id} not found'})
        lpage = page[0]
        if lpage.content_type.name.replace(' ', '') == 'meynstreampage':
            lpage = getattr(lpage, lpage.content_type.name.replace(' ', '')).body
            lblock = []
            for block in lpage:
                pass
                if block.block_type in ('heading'):
                    lblock.append({'type': block.block_type, 'value': block.value})
                elif block.block_type in ('paragraph'):
                    lblock.append({'type': block.block_type, 'value': self.html2sb(str(block.value), doc)})
                else:
                    subdoc_dir  = os.path.join(settings.STATICFILES_DIRS[0], "template/other.docx")
                    doc = DocxTemplate(subdoc_dir)
                    subdoc = doc.new_subdoc().add_paragraph('un paragraphe')
                    lblock.append({'type': 'other', 'value': doc.build_xml({})})

            context.update({'blocks': lblock})
        return context

    def post(self, request, *args, **kwargs):
        tpl_dir = os.path.join(settings.STATICFILES_DIRS[0], "template/order_tpl.docx")
        doc = DocxTemplate(tpl_dir)
        print(request.POST)
        # context = {'title': request.POST['filename']}
        context = self.get_page(request.POST['id'], doc)
        print(context)
        doc.render(context)
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        response['Content-Disposition'] = f"attachment; filename={request.POST['filename']}.docx"
        doc.save(response)
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Génération des documents'
        context['pages'] = Page.objects.live()
        # for page in Page.get_root_nodes():
        #     print(f"{type(page)}({page.id})-{page.content_type}")
        #     for item in page.get_children():
        #         print(f"->{type(item)}({item.id})-{item.content_type}")
        #         for subpage in item.get_children():
        #             print(f"-->{type(subpage)}({subpage.id})-{subpage.content_type}")
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
