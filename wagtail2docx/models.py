import logging
from django.db.models import BooleanField, DateField, DecimalField, Model, CharField, ImageField, ForeignKey, \
    DO_NOTHING, CASCADE, URLField, TextField
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
from wagtail.core.models import Page
from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import StreamFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from .block import CodeBlock, myTableBlock, HeadingBlock, ImageBlock, InfoBlock, WarningBlock, DocumentBlock, \
    StartCardDeck, EndCardDeck
from wagtail.core import blocks
from wagtail.snippets.models import register_snippet
from django.db import models
from django.http import HttpResponseRedirect
from wagtail.search import index
from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.documents.models import Document
from wagtail.contrib.forms.models import AbstractFormField
from django.conf import settings

#Logger
logger = logging.getLogger('site')
sf = logging.Formatter('%(message)s')
logger.propagate = True
# for logger ip
def get_client_ip(request):
    """
    To put in util / get client IP
    :param request:
    :return:
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

@register_snippet
class Product(Model):
    name = CharField(max_length=255)
    purchase_date = DateField("Date d'achat")
    vendor_name = CharField(max_length=255)
    price = DecimalField(max_digits=6, decimal_places=2)
    end_of_warranty = DateField("Fin de garantie")
    photo = ImageField(blank=True)
    bill = ForeignKey(Document, on_delete=CASCADE, null=True)

    def __str__(self):
        return "%s - (%s)" % (self.name, self.end_of_warranty)

    class Meta:
        verbose_name = "Produit sous garantie"
        verbose_name_plural = "Produits sous garantie"
        ordering = ('end_of_warranty',)



class ProductAdmin(ModelAdmin):
    model = Product
    menu_label = "Produit - Inventaire"
    menu_icon = "doc-empty"
    menu_order = 300
    add_to_settings_menu = False  # or True to add your model to the SeVttings sub-menu
    exclude_from_explorer = False  # or True to exclude pages of this type from Wagtail's explorer view
    list_display = ('name', 'end_of_warranty', 'vendor_name')
    list_filter = ('name', 'end_of_warranty', 'vendor_name')
    search_fields = ('name', 'vendor_name')


modeladmin_register(ProductAdmin)


class ProductPage(Page):
    intro = models.CharField(max_length=250, default="")
    cover = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full"),
        ImageChooserPanel('cover')
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request)
        products = Product.objects.all().order_by('-end_of_warranty')
        context['products'] = products
        return context


class MeynIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full")
    ]

class MeynRedirectPage(Page):
    redirect_url = URLField(name="redirection", verbose_name="redirections", null=False, blank=False)

    content_panels = Page.content_panels + [
        FieldPanel('redirection'),
    ]

    def serve(self, request):
        logger.info("redirect access to : " + str(self.redirection), extra={"client_ip": get_client_ip(request)})
        return HttpResponseRedirect(self.redirection)

class MeynStreamPage(Page):
    date = DateField("Date de création", auto_now_add=True, null=True)
    modifdate = DateField("Date de modification", auto_now=True, null=True)
    intro = models.CharField(max_length=250)
    cover = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    body = StreamField([
        ('heading', HeadingBlock(classname="Full")),
        ('paragraph', blocks.RichTextBlock()),
        ('code', CodeBlock()),
        ('table', myTableBlock()),
        ('image', ImageBlock()),
        ('info', InfoBlock()),
        ('warning', WarningBlock()),
        ('document', DocumentBlock()),
        ('start_carddeck', StartCardDeck()),
        ('end_carddeck', EndCardDeck())
    ])

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        ImageChooserPanel('cover'),
        FieldPanel('intro'),
        StreamFieldPanel('body'),
    ]

class RevealStreamPage(Page):
    date = DateField("Date de création", auto_now_add=True, null=True)
    modifdate = DateField("Date de modification", auto_now=True, null=True)
    intro = models.CharField(max_length=250)
    cover = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    body = StreamField([
        ('heading', HeadingBlock(classname="Full")),
        ('paragraph', blocks.RichTextBlock()),
        ('code', CodeBlock()),
        ('table', myTableBlock()),
        ('image', ImageBlock()),
        ('info', InfoBlock()),
        ('warning', WarningBlock()),
    ])

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        ImageChooserPanel('cover'),
        FieldPanel('intro'),
        StreamFieldPanel('body'),
    ]
