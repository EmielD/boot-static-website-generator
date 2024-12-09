from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag:str, value:str, props:dict = None):
        super().__init__(tag, value, props)
        self.tag = tag
        self.value = value
        self.props = props
    
    def to_html(self):
        if self.value == None:
            raise ValueError
        if self.tag == None:
            return self.value
        
        props_string = ""
        if self.props is not None:
            props_string = ' '.join(f' {key}="{value}"' for key, value in self.props.items())

        return f"<{self.tag}{props_string}>{self.value}</{self.tag}>"

