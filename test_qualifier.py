import datetime
import sys
import unittest
from typing import Type
from unittest import mock

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

    def test_len(self):
        """Using len(article) should return the article's content's length."""
        self.assertEqual(len(self.article.content), len(self.article))

    def test_short_introduction(self):
        """Should return content truncated at a space/newline to at most n_characters."""
        contents = (
            (self.content, "'But he has nothing", 20),
            ("'I know I'm not stupid,' the man thought,", "'I know I'm not stupid,' the", 31),
            ("'Magnificent,' said the two officials already duped", "'Magnificent,'", 15),
            ("see anything.\nHis whole", "see anything.", 16),
        )

        for content, expected, n in contents:
            with self.subTest(content=content, expected=expected, n=n):
                self.article.content = content
                actual = self.article.short_introduction(n_characters=n)
                self.assertEqual(expected, actual)

    def test_most_common_words(self):
        """Should return a dictionary of the n_words most common words in the content."""
        contents = (
            (self.content, {"at": 2, "all": 2, "but": 1, "he": 1, "has": 1}, 5),
            ("'I know I'm not stupid,'", {"i": 2, "know": 1, "m": 1}, 3),
            ("'Magnificent,' said the two officials", {"magnificent": 1, "said": 1}, 2),
            ("of his.\nHis whole", {"his": 2, "of": 1}, 2),
            ("Am I a fool?", {}, 0),
            ("All the town",  {"all": 1, "the": 1, "town": 1}, 9372)
        )

        for content, expected, n in contents:
            with self.subTest(content=content, expected=expected, n=n):
                self.article.content = content
                actual = self.article.most_common_words(n)
                self.assertEqual(expected, actual)


class IntermediateTests(unittest.TestCase):
    """Tests for the intermediate requirements."""

    @staticmethod
    def get_reset_article() -> Type[Article]:
        """Re-import the qualifier module to reset any class attributes of the Article."""
        # https://stackoverflow.com/a/27604236/5717792
        try:
            del sys.modules['qualifier']
        except KeyError:
            pass

        from qualifier import Article
        return Article

    def test_unique_id(self):
        """New Articles should be assigned a unique, sequential ID starting at 0."""
        Article = self.get_reset_article()
        articles = []

        for _ in range(5):
            article = Article(title="a", author="b", content="c", publication_date=mock.Mock())
            articles.append(article)

        # Assert in a separate loop to ensure that new articles didn't affect previous IDs.
        for expected_id, article in enumerate(articles):
            self.assertEqual(expected_id, article.id)

    @mock.patch("qualifier.datetime")
    def test_last_edited(self, local_datetime):
        """Attribute should update to the current time when the content changes."""
        article = Article(title="a", author="b", content="c", publication_date=mock.Mock())
        self.assertIsNone(article.last_edited, "Initial value of last_edited should be None")

        # Set twice to account for both "import datetime" and "from datetime import datetime"
        side_effects = ("first datetime", "second datetime")
        local_datetime.now.side_effect = side_effects
        local_datetime.datetime.now.side_effect = side_effects

        article.content = "'I know I'm not stupid,' the man thought,"
        self.assertEqual(side_effects[0], article.last_edited)

        article.content = "'Magnificent,' said the two officials"
        self.assertEqual(side_effects[1], article.last_edited)

    def test_sort(self):
        """Articles should be inherently sortable by their publication date."""
        kwargs = {"title": "a", "author": "b", "content": "c"}
        articles = [
            Article(**kwargs, publication_date=datetime.datetime(2001, 7, 5)),
            Article(**kwargs, publication_date=datetime.datetime(1837, 4, 7)),
            Article(**kwargs, publication_date=datetime.datetime(2015, 8, 20)),
            Article(**kwargs, publication_date=datetime.datetime(1837, 4, 7)),
        ]

        expected = [articles[1], articles[3], articles[0], articles[2]]
        actual = sorted(articles)
        self.assertSequenceEqual(expected, actual)
