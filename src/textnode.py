from enum import Enum
from leafenode import LeafNode

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self,text, text_type, url=""):
        self.text = text
        self.text_type = text_type
        self.url = url
    def __eq__(self, value):
        return self.text == value.text and self.url == value.url and self.text_type == value.text_type
    def __repr__(self):
        if self.url != "":
            return f'Textnode("{self.text}", TextType.{self.text_type.name}, "{self.url}")'
        else:
            return f'Textnode("{self.text}", TextType.{self.text_type.name})'

def text_node_to_html_node(text_node:TextNode):
    match(text_node.text_type):
        case TextType.TEXT:
            return LeafNode("", text_node.text).to_html()
        case TextType.BOLD:
            return LeafNode("b", text_node.text).to_html()
        case TextType.ITALIC:
            return LeafNode("i", text_node.text).to_html()
        case TextType.CODE:
            return LeafNode("code", text_node.text).to_html()
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url}).to_html()
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text}).to_html()
