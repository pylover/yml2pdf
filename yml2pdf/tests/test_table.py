from os.path import dirname, abspath, join, exists
from os import mkdir
import io
import unittest

from yml2pdf.documents import Document
from yml2pdf.elements import Paragraph, Spacer


class TemplateTestCase(unittest.TestCase):
    def setUp(self):
        self.temp_dir = abspath(join(dirname(__file__), 'temp'))
        if not exists(self.temp_dir):
            mkdir(self.temp_dir)

    def test_basic_elements(self):
        out_filename = join(self.temp_dir, 'test_basic_elements.pdf')

        yml = """

        document:
          width: 595
          height: 842 

        body:
          - !Spacer
            height: 50

          - !Paragraph
            text: 'This should be a green text with font size 15. Top margin is 50.'
            styles:
              text_color: '#00FF00'
              font_size: 15
              
          - !Table
            header:
              - !Column
                - !Paragraph
                  text: 'header1'
              - !Column
                - !Paragraph
                  text: 'header2'
            body:
              - !Row
                - !Cell
                  - !Paragraph
                    text: 'value1'
                - !Cell
                  - !Paragraph
                    text: 'value2'
              - !Row
                - !Cell
                  - !Paragraph
                    text: 'value3/1'
                  - !Paragraph
                    text: 'value3/2'
                - !Cell
                  - !Paragraph
                    text: 'value4'

        """

        out = io.BytesIO()
        doc = Document(yml, out)

        ctx = dict(
            temp=self.temp_dir,
        )

        doc.build()
        out.seek(0)

        with open(out_filename, 'wb') as f:
            f.write(out.read())

        file_length = len(out.getbuffer())
        self.assertTrue(file_length // 100 >= 15)


if __name__ == '__main__':
    unittest.main()
