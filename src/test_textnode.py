import unittest

from textnode import TextNode, TextType


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


if __name__ == "__main__":
    unittest.main()
