import unittest

from markdown import extract_markdown_images, extract_markdown_links


class TestMarkdownFunctions(unittest.TestCase):
    def test_extract_markdown_images(self):
        text = "![cat](https://example.com/cat.png) and ![dog](https://example.com/dog.png)"
        expected = [("cat", "https://example.com/cat.png"),
                    ("dog", "https://example.com/dog.png")]
        result = extract_markdown_images(text)
        self.assertListEqual(expected, result)

    def test_extract_markdown_links(self):
        text = "[Google](https://google.com) and [Boot.dev](https://boot.dev)"
        expected = [("Google", "https://google.com"),
                    ("Boot.dev", "https://boot.dev")]
        result = extract_markdown_links(text)
        self.assertListEqual(expected, result)

    def test_extract_markdown_images_no_matches(self):
        text = "This is a sentence without any markdown images."
        expected = []
        result = extract_markdown_images(text)
        self.assertListEqual(expected, result)

    def test_extract_markdown_images_empty_alt_text(self):
        text = "![](https://example.com/emptyalt.png)"
        expected = [("", "https://example.com/emptyalt.png")]
        result = extract_markdown_images(text)
        self.assertListEqual(expected, result)

    def test_extract_markdown_images_empty_url(self):
        text = "![empty_url]()"
        expected = [("empty_url", "")]
        result = extract_markdown_images(text)
        self.assertListEqual(expected, result)

    def test_extract_markdown_images_malformed_syntax(self):
        text = "![broken_image](https://example.com/image.png"
        expected = []
        result = extract_markdown_images(text)
        self.assertListEqual(expected, result)


if __name__ == "__main__":
    unittest.main()
