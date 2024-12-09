import unittest

from textnode import *


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
        self.assertNotEqual(node, node2)

    def test_text_node_to_html_node_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertIsNotNone(text_node_to_html_node(node))
        node = TextNode("This is a text node", TextType.LINK, "https://www.boot.dev")
        self.assertIsNotNone(text_node_to_html_node(node))
        node = TextNode("This is a text node", TextType.IMAGE, "https://www.boot.dev")
        self.assertIsNotNone(text_node_to_html_node(node))



if __name__ == "__main__":
    unittest.main()