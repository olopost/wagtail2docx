from django.utils.safestring import mark_safe
from django.utils.html import format_html

from pygments import highlight
from pygments.formatters import get_formatter_by_name
from pygments.lexers import get_lexer_by_name

from wagtail.core.fields import RichTextField, StreamBlock, StreamField
from wagtail.core import blocks
from wagtail.contrib.table_block.blocks import TableBlock, DEFAULT_TABLE_OPTIONS
from wagtail.images.blocks import ImageChooserBlock
from wagtail.documents.blocks import DocumentChooserBlock

class ImageBlock(blocks.StructBlock):
    """
    Custom `StructBlock` for utilizing images with associated caption and
    attribution data
    """
    image = ImageChooserBlock(required=True)
    caption = blocks.CharBlock(required=False)
    attribution = blocks.CharBlock(required=False)

    class Meta:
        icon = 'image'
        template = "block/imageblock.html"

new_table_options = {
    'minSpareRows': 0,
    'startRows': 6,
    'startCols': 3,
    'colHeaders': True,
    'rowHeaders': False,
    'contextMenu': True,
    'editor': 'text',
    'language': 'fr',
    'renderer': 'text',
    'filter': 'true',
    'licenseKey': "c1584-308e7-abdd4-64504-6de49",
}


class myTableBlock(blocks.StructBlock):
    table = TableBlock(table_options=new_table_options)

    class Meta:
        icon = "table"
        template = "block/table.html"



class InfoBlock(blocks.StructBlock):
    class Meta:
        icon = "help"
        template = "block/infoblock.html"
    info = blocks.RichTextBlock()

class WarningBlock(blocks.StructBlock):
    class Meta:
        icon = "warning"
        template = "block/warningblock.html"
    warning = blocks.RichTextBlock()

class StartCardDeck(blocks.StructBlock):
    class Meta:
        icon = "card"
        template = 'block/startcard.html'

class EndCardDeck(blocks.StructBlock):
    class Meta:
        icon = "card"
        template = 'block/endcard.html'

class HeadingBlock(blocks.CharBlock):
    class Meta:
        template = 'block/heading.html'

class DocumentBlock(blocks.StructBlock):
    document = DocumentChooserBlock(required=True)
    comment = blocks.RichTextBlock()
    image = ImageChooserBlock(required=False)

    class Meta:
        icon = "doc-full"
        template = 'block/document.html'

class CodeBlock(blocks.StructBlock):
    """
    Code Highlighting Block
    """
    LANGUAGE_CHOICES = (
        ('python', 'Python'),
        ('bash', 'Shell'),
        ('html', 'HTML'),
        ('css', 'CSS'),
        ('json', 'JSON'),
        ('js', 'javaScript'),
        ('jinja', 'jinja'),
        ('INI', 'ini'),
    )

    STYLE_CHOICES = (
        ('monokai', 'monokai'),
    )

    language = blocks.ChoiceBlock(choices=LANGUAGE_CHOICES)
    #style = blocks.ChoiceBlock(choices=STYLE_CHOICES, default='default')
    code = blocks.TextBlock()

    class Meta:
        icon = 'code'

    def render(self, value, context=None):
        src = value['code'].strip('\n')
        lang = value['language']
        lexer = get_lexer_by_name(lang)
        #css_classes = ['highlight', value['style']]
        css_classes = ['highlight', 'monokai rounded']

        formatter = get_formatter_by_name(
            'html',
            linenos='inline',
            cssclass=' '.join(css_classes),
            noclasses=False,
        )
        return mark_safe(highlight(src, lexer, formatter))

