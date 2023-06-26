from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.models import Page


class HomePage(Page):
    pass


class ImageTestingPage(Page):
    images = StreamField(
        [("image", ImageChooserBlock())],
        use_json_field=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("images"),
    ]
