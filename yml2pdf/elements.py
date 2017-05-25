# noinspection PyPackageRequirements
import yaml

from reportlab import platypus
from reportlab.lib import styles
from reportlab.platypus.tables import TableStyle

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
        self_styles = {to_camel_case(k): v for k, v in self.styles.items()}
        if self_styles is not self.__class__.styles:
            result.update(self_styles)
        return self.__flowable_style_class__(
            name='%s_styles' % self.__class__.__name__,
            **{to_camel_case(k): v for k, v in result.items()}
        )

    # noinspection PyMethodMayBeStatic
    def translate_flowable_params(self):
        result = {}
        params = {
            k: getattr(self, k, v) for k, v in self.__flowable_attributes__.items()
        }

        if 'styles' in params:
            result['style'] = self.create_style()
            del params['styles']

        result.update({to_camel_case(k): v for k, v in params.items()})
        return result

    def to_flowable(self):
        return self.__flowable_class__(**self.translate_flowable_params())


class Paragraph(Flowable):
    yaml_tag = '!Paragraph'
    __flowable_class__ = platypus.Paragraph
    __flowable_attributes__ = {
        'text': '',
        'styles': None
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


class Table(Flowable):
    yaml_tag = '!Table'
    __flowable_class__ = platypus.Table
    __flowable_attributes__ = {
        'data': None,
        'style': None
    }
    __flowable_style_class__ = TableStyle

    header = None
    body = None


def custom_sequence_constructor(loader, node):
    return loader.construct_sequence(node)

yaml.add_constructor('!Column', custom_sequence_constructor)
yaml.add_constructor('!Row', custom_sequence_constructor)
yaml.add_constructor('!Cell', custom_sequence_constructor)
