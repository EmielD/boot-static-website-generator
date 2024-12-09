import unittest

from htmlnode import HTMLNode


class TestTextNode(unittest.TestCase):
    
    def test_eq(self):
        node = HTMLNode("", "", "", dict(href="https://www.google.com", target="_blank"))
        node2 = HTMLNode("", "", "", dict(href="https://www.google.com", target="_blank"))
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = HTMLNode("", "", "", dict(href="https://www.google.com", target="_blank"))
        node2 = HTMLNode("", "", "", dict(href="https://www.boots.dev", target="_blank"))
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()