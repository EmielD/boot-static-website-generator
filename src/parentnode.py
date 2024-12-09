from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, childeren, props = None):
        super().__init__(tag, childeren, props)
        self.tag = tag
        self.childeren = childeren
        self.props = props

    def to_html(self):
        if self.tag == None:
            raise ValueError("Property 'tag' must have a value")
        if self.childeren == None:
            raise ValueError("Property 'childeren' must have a value")
        
        child_html = ""
        for child in self.childeren:
            child_html += child.to_html()

        props_string = ""
        if self.props is not None:
            props_string = ' '.join(f' {key}="{value}"' for key, value in self.props.items())

        return f"<{self.tag}{props_string}>{child_html}</{self.tag}>"