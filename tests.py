
import io
import unittest

from yml2pdf import Template, Label


class TemplateTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def test_draw(self):

        yml = """

        width: 800
        height: 600

        body:
          - !label
            text: 'Lorem Ipsum'
            pos: [10, 20]

        """

        out = io.BytesIO()
        t = Template(yml, out)

        self.assertEqual(t.data['width'], 800)
        self.assertEqual(t.data['height'], 600)
        self.assertIsInstance(t.data['body'][0], Label)
        self.assertEqual(t.data['body'][0].text, 'Lorem Ipsum')

        t.draw()
        self.assertEqual(len(out.getbuffer()) // 100, 15)
