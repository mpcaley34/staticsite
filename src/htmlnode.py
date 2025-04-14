class HTMLNode:  # Note: removed the parentheses, though this shouldn't matter
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if self.props is None:
            return ''

        result = ''
        for key, value in self.props.items():
            result += f' {key}="{value}"'

        return result

    def __repr__(self):
        return f'HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})'


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError('LeafNode must have a value')
        if self.tag is None:
            return self.value

        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        # If props is None, convert it to empty dict
        if props is None:
            props = {}

        super().__init__(tag, None, children, props)
        self.children = children

    def to_html(self):
        if self.tag is None:
            raise ValueError('No tag')
        if not self.children:
            raise ValueError('Children has no value')

        # Starts with opening tag
        html = f'<{self.tag}'

        # Add properties if they exist
        if self.props:
            for prop, value in self.props.items():
                html += f' {prop}="{value}"'

        # Close opening tag
        html += '>'

        # Add all children's HTML
        for child in self.children:
            html += child.to_html()

        # Add closing tag
        html += f'</{self.tag}>'

        return html
