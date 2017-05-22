
from os.path import dirname, abspath, join, exists
from os import mkdir
import io
import unittest

from yml2pdf.documents import Document
from yml2pdf.elements import ParagraphElement, SpacerElement


class TemplateTestCase(unittest.TestCase):

    def setUp(self):
        self.temp_dir = abspath(join(dirname(__file__), 'temp'))
        self.stuff_dir = abspath(join(dirname(__file__), 'test_stuff'))
        if not exists(self.temp_dir):
            mkdir(self.temp_dir)

    def test_basic_elements(self):
        out_filename = join(self.temp_dir, 'test_basic_elements.pdf')

        yml = """
        
        fonts:
          default: tahoma
          tahoma: '%(stuff)s/tahoma.ttf'
          tahoma-bold: '%(stuff)s/tahoma-bold.ttf'
        
        document:
          width: 595
          height: 842  

        body:
          - !Spacer
            height: 50

          - !Paragraph
            text: 'Lorem Ipsum'
            styles:
              text_color: '#FF2222'
              font_size: 20


        """

        out = io.BytesIO()
        doc = Document(yml, out)

        ctx = dict(
            stuff=self.stuff_dir,
            temp=self.temp_dir,
        )

        doc.register_fonts(ctx)

        self.assertEqual(doc.data['width'], 595)
        self.assertEqual(doc.data['height'], 842)
        self.assertIsInstance(doc.data['body'][0], SpacerElement)
        self.assertIsInstance(doc.data['body'][1], ParagraphElement)
        self.assertEqual(doc.data['body'][1].text, 'Lorem Ipsum')

        doc.build()
        out.seek(0)

        with open(out_filename, 'wb') as f:
            f.write(out.read())

        file_length = len(out.getbuffer())
        self.assertTrue(file_length // 100 >= 15)


if __name__ == '__main__':
    unittest.main()
