import unittest
# This imports the HTMLNode class from the htmlnode module
from htmlnode import HTMLNode, LeafNode, ParentNode


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


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_value_none(self):
        node = LeafNode('p', None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_tag_none(self):
        value2 = 'this is plain text'
        node = LeafNode(tag=None, value=value2)
        self.assertEqual(node.to_html(), value2)

    def test_leaf_same_tags(self):
        node = LeafNode('div', 'Hello world')
        self.assertEqual(node.to_html(), '<div>Hello world</div>')


class TestParentNode(unittest.TestCase):

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(),
                         "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_parent_node_with_leaf_children(self):
        # Test a parent with multiple leaf children
        parent = ParentNode("div", [
            LeafNode("span", "Child 1"),
            LeafNode("p", "Child 2")
        ])
        self.assertEqual(parent.to_html(),
                         "<div><span>Child 1</span><p>Child 2</p></div>")

    def test_parent_node_with_props(self):
        # Test with properties
        parent = ParentNode("div", [LeafNode("span", "Child")], {
                            "class": "container", "id": "main"})
        self.assertEqual(
            parent.to_html(), '<div class="container" id="main"><span>Child</span></div>')

    def test_nested_parent_nodes(self):
        # Test nested parent nodes (grandparent > parent > child)
        child = LeafNode("span", "Child text")
        parent = ParentNode("div", [child])
        grandparent = ParentNode("section", [parent])
        self.assertEqual(grandparent.to_html(
        ), "<section><div><span>Child text</span></div></section>")

    def test_parent_node_with_empty_children_list(self):
        # Test with empty children list
        parent = ParentNode("div", [])
        with self.assertRaises(ValueError):
            parent.to_html()

    def test_parent_node_without_tag(self):
        # Test without a tag
        parent = ParentNode(None, [LeafNode("span", "Child")])
        with self.assertRaises(ValueError):
            parent.to_html()


if __name__ == "__main__":
    unittest.main()
