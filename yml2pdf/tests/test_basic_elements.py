
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
          left_margin: 100

        body:
          - !Spacer
            height: 50
            
          - !Paragraph
            text: 'This should be a green text with font size 15. Top margin is 50.'
            styles:
              text_color: '#00FF00'
              font_size: 15

          - !Paragraph
            text: 'This should be a red text with font size 20'
            styles:
              text_color: 'red'
              font_size: 20
          
          - !Spacer
            height: 50
          
          - !Paragraph
            text: 'Default style for paragraph. Document has 100 left margin.'

        """

        out = io.BytesIO()
        doc = Document(yml, out)

        ctx = dict(
            temp=self.temp_dir,
        )

        self.assertEqual(doc.data['document']['width'], 595)
        self.assertEqual(doc.data['document']['height'], 842)
        self.assertIsInstance(doc.data['body'][0], Spacer)
        self.assertIsInstance(doc.data['body'][1], Paragraph)
        self.assertIsInstance(doc.data['body'][2], Paragraph)
        self.assertEqual(doc.data['body'][1].text, 'This should be a green text with font size 15. Top margin is 50.')
        self.assertEqual(doc.data['body'][2].text, 'This should be a red text with font size 20')

        doc.build()
        out.seek(0)

        with open(out_filename, 'wb') as f:
            f.write(out.read())

        file_length = len(out.getbuffer())
        self.assertTrue(file_length // 100 >= 15)


if __name__ == '__main__':
    unittest.main()
