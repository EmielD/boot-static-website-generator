from enum import Enum
import re

from htmlnode import HTMLNode
from textnode import TextNode, TextType



class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def extract_title(markdown):
    for item in markdown.split("\n"):
        if "# " in item:
            return (item.strip("# "))
        
def convert_nested_elements(text):
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)  # Bold
    text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)  # Italics
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text) # Code
    text = re.sub(r'!\[([^\[\]]*)\]\(([^\(\)]*)\)', r'<image alt="\1" src="\2"/>', text) # Images
    text = re.sub(r'(?<!\!)\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', text) # Links
    
    return text

def markdown_to_html_node(markdown):
    parent = HTMLNode(tag="div")
    parent.children = []

    blocks = markdown_to_blocks(markdown)

    for block in blocks:
        block_info = block_to_block_type(block)
        content = clean_content(block, block_info)

        if isinstance(block_info, tuple) and block_info[0] == BlockType.HEADING:
            heading_count = block_info[1]
            tag = f"h{heading_count}"
            parent.children.append(HTMLNode(tag, block[heading_count + 1:].strip()))
        
        elif block_info == BlockType.CODE:
            parent.children.append(HTMLNode("code", content))
        elif block_info == BlockType.ORDERED_LIST:
            parent.children.append(HTMLNode("ol", content))
        elif block_info == BlockType.UNORDERED_LIST:
            parent.children.append(HTMLNode("ul", content))
        elif block_info == BlockType.PARAGRAPH:
            parent.children.append(HTMLNode("p", content))
        elif block_info == BlockType.QUOTE:
            parent.children.append(HTMLNode("blockquote", content))

    return parent


def clean_content(block, block_type):
    if isinstance(block_type, tuple) and block_type[0] == BlockType.HEADING:
        heading_count = block_type[1]
        return block[heading_count + 1:].strip()

    if block_type == BlockType.CODE:
        return block.strip("`").strip()

    if block_type == BlockType.ORDERED_LIST:
        return "\n".join(line.lstrip("0123456789. ") for line in block.splitlines()).strip()

    if block_type == BlockType.UNORDERED_LIST:
        return "\n".join(line.lstrip("*- ") for line in block.splitlines()).strip()

    if block_type == BlockType.QUOTE:
        return "\n".join(line.lstrip("> ") for line in block.splitlines()).strip()

    if block_type == BlockType.PARAGRAPH:
        return block.strip()

    return block

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_nodes_with_delimiter(text, delimiter):

    if delimiter == "" or None:
        return  None

    if delimiter == "**":
        delimiter = "\\*\\*"

    if delimiter == "`":
        delimiter = "\\`"

    if delimiter == "*":
        delimiter = "\\*"

    return re.findall(r"" + delimiter + "([^*]*)" + delimiter, text)

def split_nodes_image(old_nodes):
    result = []
    for node in old_nodes:
        images = extract_markdown_images(node.text)
        if not images:
            result.append(node)
        else:
            for image in images:
                split_text = node.text.split(f"![{image[0]}]({image[1]})")
                before_text = split_text[0]
                node.text = split_text[1]

                if before_text != "":
                    result.append(TextNode(before_text, TextType.TEXT))
                
                result.append(TextNode(image[0], TextType.IMAGE, image[1]))

            if node.text != "":
                result.append(TextNode(node.text, TextType.TEXT))

    print("??")
    print(result)

    return result

def split_nodes_link(old_nodes):
    result = []
    for node in old_nodes:
        links = extract_markdown_links(node.text)
        if not links:
            result.append(node)
        else:
            for link in links:
                split_text = node.text.split(f"[{link[0]}]({link[1]})")
                before_text = split_text[0]
                node.text = split_text[1]

                if before_text != "":
                    result.append(TextNode(before_text, TextType.TEXT))
                
                result.append(TextNode(link[0], TextType.LINK, link[1]))

            if node.text != "":
                result.append(TextNode(node.text, TextType.TEXT))

    return result

def split_nodes_delimiter(old_nodes:list, delimiter:str, text_type:TextType):
    new_nodes = []
    for node in old_nodes:

        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        delimited_text = extract_markdown_nodes_with_delimiter(node.text, delimiter)
        
        # If no delimited text found, keep the node as is
        if not delimited_text:
            new_nodes.append(node)
            continue

        if delimiter == "" or delimiter == None:
            new_nodes.append(node)
            continue

        split_text = node.text.split(delimiter)
        for text in split_text:
            if text in delimited_text:
                    new_nodes.append(TextNode(text, text_type))
            else:
                new_nodes.append(TextNode(text, TextType.TEXT))

    return new_nodes


def text_to_textnodes(text):
    text_node = [TextNode(text, TextType.TEXT)]

    #First get all the images:
    nodes = split_nodes_image(text_node)
    
    #Get all links:
    nodes = split_nodes_link(nodes)

    #Get bold nodes
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)

    #Get italic nodes
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)

    #Get code nodes
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)

    return nodes

#####

def is_unordered_list(block):
    return all(line.startswith("* ") or line.startswith("- ") for line in block.split("\n"))

def is_ordered_list(block):   
    return all(line.split(". ")[0].isdigit() for line in block.split("\n"))

def is_quote(block):
    return block.startswith("> ")

def is_code(block):
    return block.startswith("```") and block.endswith("```")

def is_heading(block):
    heading_count = 0
    for char in block[:6]:
        if char == '#':
            heading_count += 1
        else:
            break

    if(len(block) > heading_count):
        if heading_count > 0 and heading_count <= 6 and block[heading_count] == " ":
            return True, heading_count
    return False, None

def block_to_block_type(block):
    if block is None or block == "":
        return None

    if is_ordered_list(block):
        return BlockType.ORDERED_LIST
    if is_unordered_list(block):
        return BlockType.UNORDERED_LIST
    if is_quote(block):
        return BlockType.QUOTE
    if is_code(block):
        return BlockType.CODE
    
    is_heading_block, heading_count = is_heading(block)
    if is_heading_block:
        return BlockType.HEADING, heading_count

    return BlockType.PARAGRAPH

def markdown_to_blocks(markdown):
    return list(filter(None, markdown.split("\n\n")))