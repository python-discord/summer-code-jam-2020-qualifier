import datetime
import unittest

from qualifier import Article


class BasicTests(unittest.TestCase):
    """Tests for the basic requirements."""

    def setUp(self) -> None:
        """Create a new Article instance before running each test."""
        self.title = "The emperor's new clothes"
        self.author = "Hans Christian Andersen"
        self.content = "'But he has nothing at all on!' at last cried out all the people."
        self.publication_date = datetime.datetime(1837, 4, 7, 12, 15, 0)

        self.article = Article(
            title=self.title,
            author=self.author,
            content=self.content,
            publication_date=self.publication_date
        )

    def test_instantiation(self):
        """The parameters given to __init__ should be assigned to attributes with the same names."""
        self.assertEqual(self.title, self.article.title)
        self.assertEqual(self.author, self.article.author)
        self.assertEqual(self.content, self.article.content)
        self.assertEqual(self.publication_date, self.article.publication_date)

    def test_repr(self):
        """The repr should be in a specific format, which includes the title, author, and date."""
        actual_repr = repr(self.article)
        expected_repr = (
            "<Article title=\"The emperor's new clothes\" author='Hans Christian Andersen' "
            "publication_date='1837-04-07T12:15:00'>"
        )
        self.assertEqual(expected_repr, actual_repr)
