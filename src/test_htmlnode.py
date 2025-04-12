import unittest
# This imports the HTMLNode class from the htmlnode module
from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_none(self):
        # Test with no props
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), '')

    def test_props_to_html_one_prop(self):
        # Test with one prop
        node = HTMLNode(props={"href": "https://google.com"})
        self.assertEqual(node.props_to_html(), ' href="https://google.com"')

    def test_props_to_html_multiple_props(self):
        # Test with multiple props
        node = HTMLNode(
            props={"href": "https://google.com", "target": "_blank"})
        result = node.props_to_html()
        self.assertIn(' href="https://google.com"', result)
        self.assertIn(' target="_blank"', result)
        self.assertEqual(len(result.split()), 2)  # Should have two props


if __name__ == "__main__":
    unittest.main()
