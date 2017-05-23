# noinspection PyPackageRequirements
import yaml

from reportlab import platypus
from reportlab.lib import styles

from yml2pdf.helpers import to_camel_case


class Element(yaml.YAMLObject):
    pass


class Flowable(Element):
    __flowable_class__ = None
    __flowable_attributes__ = None
    __flowable_style_class__ = None

    styles = {}

    def create_style(self):
        result = self.__class__.styles.copy()
        if self.styles is not self.__class__.styles:
            result.update(self.styles)
        return self.__flowable_style_class__(**result)

    def __getattr__(self, item):
        if item == 'styles':
            return self.create_style()
        return object.__getattribute__(self, item)

    def to_flowable(self):
        return self.__flowable_class__(**{
            to_camel_case(k): getattr(self, k, v) for k, v in self.__flowable_attributes__.items()
        })


class Paragraph(Flowable):
    yaml_tag = '!Paragraph'
    __flowable_class__ = platypus.Paragraph
    __flowable_attributes__ = {
        'text': '',
        'styles': styles.getSampleStyleSheet()['Normal']
    }
    __flowable_style_class__ = styles.ParagraphStyle

    styles = dict(

    )

class Spacer(Flowable):
    yaml_tag = '!Spacer'
    __flowable_class__ = platypus.Spacer
    __flowable_attributes__ = {
        'width': 0,
        'height': 0
    }
