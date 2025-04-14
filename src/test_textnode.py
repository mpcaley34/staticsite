import unittest

from textnode import TextNode, TextType, split_nodes_image, split_nodes_link
from htmlnode import LeafNode
from main import text_node_to_html_node, split_nodes_delimiter


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_text(self):
        node = TextNode("This is node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_text_type(self):
        node = TextNode('This is node', TextType.BOLD)
        node2 = TextNode('This is node', TextType.CODE)
        self.assertNotEqual(node, node2)

    def test_different_url(self):
        node = TextNode("Same text", TextType.LINK, "https://example.com")
        node2 = TextNode("Same text", TextType.LINK, "https://boot.dev")
        self.assertNotEqual(node, node2)

    def test_url_none_equality(self):
        node = TextNode("Same text", TextType.BOLD)  # url defaults to None
        node2 = TextNode("Same text", TextType.BOLD,
                         None)  # url explicitly None
        self.assertEqual(node, node2)


class TestTextNodeToHtmlNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("BOLD text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'b')
        self.assertEqual(html_node.value, "BOLD text")

    def test_italic(self):
        node = TextNode('ITALIC text', TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'i')
        self.assertEqual(html_node.value, 'ITALIC text')

    def test_code(self):
        node = TextNode('CODE text', TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'code')
        self.assertEqual(html_node.value, 'CODE text')

    def test_link(self):
        node = TextNode('Click me', TextType.LINK, "https://example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'a')
        self.assertEqual(html_node.value, 'Click me')
        self.assertEqual(html_node.props, {"href": "https://example.com"})

    def test_image(self):
        node = TextNode('Alt text', TextType.IMAGE, "https://example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'img')
        self.assertEqual(html_node.value, '')
        self.assertEqual(html_node.props, {
            "src": "https://example.com",
            "alt": "Alt text"
        })


class TestSplitNodeDelimiter(unittest.TestCase):
    def test_split_nodes_delimiter_simple(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        assert len(new_nodes) == 3
        assert new_nodes[0].text == "This is text with a "
        assert new_nodes[0].text_type == TextType.TEXT
        assert new_nodes[1].text == "code block"
        assert new_nodes[1].text_type == TextType.CODE
        assert new_nodes[2].text == " word"
        assert new_nodes[2].text_type == TextType.TEXT

    def test_split_nodes_delimiter_multiple(self):
        node = TextNode(
            "Text with `code` and more `code blocks`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        assert len(new_nodes) == 5
        # Check each node's text and text_type

    def test_split_nodes_delimiter_none(self):
        node = TextNode("Plain text with no delimiters", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        assert len(new_nodes) == 1
        assert new_nodes[0].text == "Plain text with no delimiters"
        assert new_nodes[0].text_type == TextType.TEXT


class TestSplitNodesImageAndLink(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE,
                         "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ],
            new_nodes,
        )

    def test_split_images_empty(self):
        # Test with no images
        node = TextNode("This is text with no images", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)

    def test_split_images_multiple_nodes(self):
        # Test with multiple nodes in the input list
        nodes = [
            TextNode("Text before", TextType.TEXT),
            TextNode("![image](https://example.com/image.png)", TextType.TEXT),
            TextNode("Text after", TextType.TEXT),
        ]
        new_nodes = split_nodes_image(nodes)
        self.assertListEqual(
            [
                TextNode("Text before", TextType.TEXT),
                TextNode("image", TextType.IMAGE,
                         "https://example.com/image.png"),
                TextNode("Text after", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_images_non_text_nodes(self):
        # Test with nodes that aren't TEXT type
        nodes = [
            TextNode("Regular text", TextType.TEXT),
            TextNode("Bold text", TextType.BOLD),
            TextNode(
                "Text with ![image](https://example.com/img.png)", TextType.TEXT),
        ]
        new_nodes = split_nodes_image(nodes)
        self.assertListEqual(
            [
                TextNode("Regular text", TextType.TEXT),
                TextNode("Bold text", TextType.BOLD),
                TextNode("Text with ", TextType.TEXT),
                TextNode("image", TextType.IMAGE,
                         "https://example.com/img.png"),
            ],
            new_nodes,
        )


if __name__ == "__main__":
    unittest.main()
