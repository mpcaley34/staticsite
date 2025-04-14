from textnode import TextNode, TextType
from htmlnode import LeafNode


def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode('b', text_node.text)
        case TextType.ITALIC:
            return LeafNode('i', text_node.text)
        case TextType.CODE:
            return LeafNode('code', text_node.text)
        case TextType.LINK:
            props = {"href": text_node.url}
            return LeafNode('a', text_node.text, props)
        case TextType.IMAGE:
            props = {
                "src": text_node.url,
                "alt": text_node.text
            }
            return LeafNode('img', '', props)
        case _:
            raise ValueError(f'Invalid TextType: {text_node.text_type}')


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old in old_nodes:
        if old.text_type != TextType.TEXT:
            new_nodes.append(old)
        else:
            text = old.text
            while delimiter in text:

                # Find opening and closing delimiters
                start_index = text.find(delimiter)
                end_index = text.find(delimiter, start_index + len(delimiter))

                if end_index == -1:
                    # No closing delimiter found
                    raise ValueError(
                        f'No closing delimiter found for {delimiter}')

                # Create three parts
                before_text = text[:start_index]
                between_text = text[start_index + len(delimiter):end_index]
                after_text = text[end_index + len(delimiter):]

                # Create nodes and add to list
                if before_text:
                    new_nodes.append(TextNode(before_text, TextType.TEXT))
                new_nodes.append(TextNode(between_text, text_type))

                # Update text to process the remainder
                text = after_text

                # Add any remaining text

            new_nodes.append(TextNode(text, TextType.TEXT))

    return new_nodes


def main():

    node = TextNode('This is some anchor text',
                    TextType.LINK, "https://www.boot.dev")
    print(node)


if __name__ == '__main__':
    main()
