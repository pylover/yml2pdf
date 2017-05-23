# noinspection PyPackageRequirements
import yaml

from reportlab import platypus
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import styles

from yml2pdf.helpers import to_camel_case


class Element(yaml.YAMLObject):
    pass


class Flowable(Element):
    __flowable_class__ = None
    __flowable_attributes__ = None

    def to_flowable(self):
        flowable_attributes = {}
        for k, v in self.__flowable_attributes__.items():
            if k in self.__dict__:
                flowable_attributes[to_camel_case(k)] = self.__dict__[k]
            else:
                flowable_attributes[to_camel_case(k)] = v

        return self.__flowable_class__(**flowable_attributes)


class ParagraphStyle(Flowable):
    yaml_tag = '!ParagraphStyle'
    yaml_flow_style = False
    __flowable_class__ = styles.ParagraphStyle
    # __flowable_attributes__ = {'style': getSampleStyleSheet()['Normal']}
    __flowable_attributes__ = {'font_size': 10, 'leading': 12}


class Paragraph(Flowable):
    yaml_tag = '!Paragraph'
    __flowable_class__ = platypus.Paragraph
    __flowable_attributes__ = {'text': '', 'style': getSampleStyleSheet()['Normal']}


class Spacer(Flowable):
    yaml_tag = '!Spacer'
    __flowable_class__ = platypus.Spacer
    __flowable_attributes__ = {'width': 0, 'height': 0}
