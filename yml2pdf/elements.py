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
        return self.__flowable_style_class__(name='%s_styles' % self.__class__.__name__, **result)

    # noinspection PyMethodMayBeStatic
    def translate_flowable_params(self):
        params = {
            k: getattr(self, k, v) for k, v in self.__flowable_attributes__.items()
        }

        def style_factory(k, v):
            return 'style', self.create_style()

        factories = {
            'styles': style_factory
        }

        return dict([factories[k](k, v) if k in factories else (to_camel_case(k), v) for k, v in params.items()])

    def to_flowable(self):
        return self.__flowable_class__(**self.translate_flowable_params())


class Paragraph(Flowable):
    yaml_tag = '!Paragraph'
    __flowable_class__ = platypus.Paragraph
    __flowable_attributes__ = {
        'text': '',
        'styles': styles.getSampleStyleSheet()['Normal']
    }
    __flowable_style_class__ = styles.ParagraphStyle

    styles = dict(
        fontSize=10,
        leading=12
    )


class Spacer(Flowable):
    yaml_tag = '!Spacer'
    __flowable_class__ = platypus.Spacer
    __flowable_attributes__ = {
        'width': 0,
        'height': 0
    }
