import unittest

from leafenode import LeafNode


class TestTextNode(unittest.TestCase):
    
    def test_eq(self):
        node = LeafNode("p", "This is a paragraph of text.")
        node2 = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual(node, node2)
    
    def test_not_eq(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        node2 = LeafNode("a", "Click me!")
        self.assertNotEqual(node, node2)

    def test_to_html_output_eq(self):
        p = LeafNode("p", "This is a paragraph of text.")
        a = LeafNode("a", "Click me!", {"href": "https://www.google.com"})

        self.assertTrue(p.to_html() == '<p>This is a paragraph of text.</p>')
        self.assertTrue(a.to_html() == '<a href="https://www.google.com">Click me!</a>')

if __name__ == "__main__":
    unittest.main()