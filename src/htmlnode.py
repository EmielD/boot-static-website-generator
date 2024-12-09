import re


class HTMLNode():
    def __init__(self, tag:str=None , value:str=None, children=None, props:dict=None):
        self.tag = tag
        self.value = value
        self.children : list[HTMLNode] = children
        self.props = props
    def __repr__(self):
         return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    def __eq__(self, value):
        return self.tag == value.tag and self.value == value.value and self.children == value.children and self.props == value.props

    def to_html(self):
        result = ""
        if self.value != None:
            if self.tag == "ul" or self.tag == "ol":
                items = "".join(f"<li>{line}</li>" for line in self.value.split("\n"))
                result += f"<{self.tag}>{items}</{self.tag}>"
            else:
                result += f"<{self.tag}>{self.value}</{self.tag}>"
        elif self.children != None:
            for child in self.children:
                result += child.to_html()
            
        return result

    def props_to_html(self):
        result = ""
        for key, value in self.props.items():
            result +=f"{key}={value} "
        return result
