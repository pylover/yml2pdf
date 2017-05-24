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
        self_styles = {to_camel_case(k): v for k, v in self.styles.items()}
        if self_styles is not self.__class__.styles:
            result.update(self_styles)
        return self.__flowable_style_class__(
            name='%s_styles' % self.__class__.__name__,
            **{to_camel_case(k): v for k, v in result.items()}
        )

    def create_data(self):
        result = []

        header_row = []
        for c in self.header:
            flowable_columns = []
            for p in c:
                flowable_columns.append(p.to_flowable())
            header_row.append(flowable_columns)
        result.append(header_row)

        for r in self.body:
            body_row = []
            for c in r:
                flowable_cells = []
                for p in c:
                    flowable_cells.append(p.to_flowable())
                body_row.append(flowable_cells)
            result.append(body_row)

        return result

    # noinspection PyMethodMayBeStatic
    def translate_flowable_params(self):
        params = {
            k: getattr(self, k, v) for k, v in self.__flowable_attributes__.items()
        }

        def style_factory(k, v):
            return 'style', self.create_style()

        def data_factory(k, v):
            return 'data', self.create_data()

        factories = {
            'styles': style_factory,
            'data': data_factory
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


class Table(Flowable):
    yaml_tag = '!Table'
    __flowable_class__ = platypus.Table
    __flowable_attributes__ = {
        'data': [['No Data For Table']]
    }


def custom_sequence_constructor(loader, node):
    return loader.construct_sequence(node)

yaml.add_constructor('!Column', custom_sequence_constructor)
yaml.add_constructor('!Row', custom_sequence_constructor)
yaml.add_constructor('!Cell', custom_sequence_constructor)

