# noinspection PyPackageRequirements
import yaml

from reportlab import platypus
from reportlab.lib.styles import getSampleStyleSheet


class Element(yaml.YAMLObject):
    pass


class Flowable(Element):
    __flowable_class__ = None
    __flowable_attributes__ = None

    def to_flowable(self):
        flowable_attributes = {}
        for k, v in self.__flowable_attributes__.items():
            if k in self.__dict__:
                flowable_attributes[k] = self.__dict__[k]
            else:
                flowable_attributes[k] = v

        return self.__flowable_class__(**flowable_attributes)


class Stylable(Flowable):
    __flowable_attributes__ = {'style': getSampleStyleSheet()['Normal']}


class Paragraph(Flowable):
    yaml_tag = '!Paragraph'
    __flowable_class__ = platypus.Paragraph
    __flowable_attributes__ = {'text': '', 'style': Stylable.__flowable_attributes__['style']}


class Spacer(Flowable):
    yaml_tag = '!Spacer'
    __flowable_class__ = platypus.Spacer
    __flowable_attributes__ = {'width': 0, 'height': 0}
