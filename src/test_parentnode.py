import unittest

from leafenode import LeafNode
from parentnode import ParentNode


class TestTextNode(unittest.TestCase):
    def test_to_html_output_eq(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )

        self.assertEqual("<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>", node.to_html())

    def test_to_html_output_eq(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
                ParentNode("p",
                [
                    LeafNode("b", "Bold text"),
                ])
            ],
        )

        self.assertEqual("<p><b>Bold text</b>Normal text<i>italic text</i>Normal text<p><b>Bold text</b></p></p>", node.to_html())

    def test_to_html_output_eq(self):
        node = ParentNode(
            "p",
            [],
        )
        
        self.assertEqual("<p></p>", node.to_html())

    def test_to_html_output_eq(self):
        node = ParentNode(
            "p",
            [ParentNode("p", 
                        [ParentNode("p", 
                                    [])])],
        )

        self.assertEqual("<p><p><p></p></p></p>", node.to_html())

if __name__ == "__main__":
    unittest.main()