import io

# noinspection PyPackageRequirements
import yaml
from reportlab.platypus import SimpleDocTemplate

from yml2pdf.helpers import to_camel_case


class Document:
    _default_properties = {
        'width': 595,  # A4 width
        'height': 842,  # A4 height
        'right_margin': 10,
        'left_margin': 10,
        'top_margin': 10,
        'bottom_margin': 10
    }

    def __init__(self, yml, out_file=None):
        self.data = yaml.load(yml)
        self.outfile = out_file or io.BytesIO()
        self.doc = SimpleDocTemplate(
            self.outfile,
            **{to_camel_case(k): v for k, v in self.properties.items()}
        )

    @property
    def body(self):
        return self.data.get('body')

    @property
    def properties(self):
        result = self._default_properties.copy()
        result.update(self.data.get('document'))
        return result

    def build(self):
        self.doc.build([element.to_flowable() for element in self.body])
