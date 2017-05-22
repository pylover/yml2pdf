# noinspection PyPackageRequirements
import yaml

from reportlab import platypus


class Element(yaml.YAMLObject):
    pass


class Flowable(Element):
    __flowable_class__ = None
    __flowable_attributes__ = None
    __yaml_tag__ = None

    def to_flowable(self):
        return self.__flowable_class__(**{k: v for k, v in self.__dict__.items() if k in self.__flowable_attributes__})


class Stylable(Flowable):
    __flowable_attributes__ = ['style']


class Paragraph(Stylable):
    __flowable_class__ = platypus.Paragraph
    __flowable_attributes__ = Stylable.__flowable_attributes__ + ['text']
    __yaml_tag__ = '!Paragraph'


class Spacer(Element):
    __flowable_class__ = platypus.Spacer
    __flowable_attributes__ = ['width', 'height']
    __yaml_tag__ = '!Spacer'
