import datetime
import importlib
import re
import unittest
from unittest import mock

import qualifier


class T100BasicTests(unittest.TestCase):
    """Tests for the basic requirements."""

    def setUp(self) -> None:
        """Create a new Article instance before running each test."""
        self.title = "The emperor's new clothes"
        self.author = "Hans Christian Andersen"
        self.content = "'But he has nothing at all on!' at last cried out all the people."
        self.publication_date = datetime.datetime(1837, 4, 7, 12, 15, 0)

        self.article = qualifier.Article(
            title=self.title,
            author=self.author,
            content=self.content,
            publication_date=self.publication_date
        )

    def test_101_instantiation(self):
        """The parameters given to __init__ should be assigned to attributes with the same names."""
        for attribute in ("title", "author", "content", "publication_date"):
            with self.subTest(attribute=attribute):
                self.assertTrue(
                    hasattr(self.article, attribute),
                    msg=f"The Article instance has no `{attribute}` attribute"
                )
                self.assertEqual(getattr(self, attribute), getattr(self.article, attribute))

    def test_102_repr(self):
        """The repr should be in a specific format, which includes the title, author, and date."""
        actual_repr = repr(self.article)
        expected_repr = (
            "<Article title=\"The emperor's new clothes\" author='Hans Christian Andersen' "
            "publication_date='1837-04-07T12:15:00'>"
        )
        self.assertEqual(expected_repr, actual_repr)

    def test_103_len(self):
        """Using len(article) should return the article's content's length."""
        self.assertTrue(hasattr(self.article, "__len__"), msg="Article has no `__len__` method.")
        self.assertEqual(len(self.article.content), len(self.article))

    def test_104_short_introduction(self):
        """short_introduction should truncate at a space/newline to at most n_characters."""
        contents = (
            (self.content, "'But he has nothing", 20),
            ("'I know I'm not stupid,' the man thought,", "'I know I'm not stupid,' the", 31),
            ("'Magnificent,' said the two officials already duped", "'Magnificent,'", 15),
            ("see anything.\nHis whole", "see anything.", 16),
        )

        self.assertTrue(
            hasattr(self.article, "short_introduction"),
            msg="Article has no `short_introduction` method."
        )

        for content, expected, n in contents:
            with self.subTest(content=content, expected=expected, n=n):
                self.article.content = content
                actual = self.article.short_introduction(n_characters=n)
                self.assertEqual(expected, actual)

    def test_105_most_common_words(self):
        """most_common_words should return a dictionary of the n_words most common words."""
        contents = (
            (self.content, {"at": 2, "all": 2, "but": 1, "he": 1, "has": 1}, 5),
            ("'I know I'm not stupid,'", {"i": 2, "know": 1, "m": 1}, 3),
            ("'Magnificent,' said the two officials", {"magnificent": 1, "said": 1}, 2),
            ("of his.\nHis whole", {"his": 2, "of": 1}, 2),
            ("Am I a fool?", {}, 0),
            ("All the town",  {"all": 1, "the": 1, "town": 1}, 9372)
        )

        self.assertTrue(
            hasattr(self.article, "most_common_words"),
            msg="Article has no `most_common_words` method."
        )

        for content, expected, n in contents:
            with self.subTest(content=content, expected=expected, n=n):
                self.article.content = content
                actual = self.article.most_common_words(n)
                self.assertEqual(expected, actual)


class T200IntermediateTests(unittest.TestCase):
    """Tests for the intermediate requirements."""

    def test_201_unique_id(self):
        """New Articles should be assigned a unique, sequential ID starting at 0."""
        importlib.reload(qualifier)
        articles = []

        for _ in range(5):
            article = qualifier.Article(
                title="a", author="b", content="c", publication_date=mock.Mock(datetime.datetime)
            )
            articles.append(article)

        # Assert in a separate loop to ensure that new articles didn't affect previous IDs.
        for expected_id, article in enumerate(articles):
            self.assertTrue(hasattr(article, "id"), msg="`Article` object has no `id` attribute")
            self.assertEqual(expected_id, article.id)

    @mock.patch("qualifier.datetime")
    def test_202_last_edited(self, local_datetime):
        """last_edited attribute should update to the current time when the content changes."""
        article = qualifier.Article(
            title="a", author="b", content="c", publication_date=mock.Mock(datetime.datetime)
        )

        self.assertTrue(
            hasattr(article, "last_edited"),
            msg="`Article` object has no `last_edited` attribute"
        )

        self.assertIsNone(article.last_edited, "Initial value of last_edited should be None")

        # Set twice to account for both "import datetime" and "from datetime import datetime"
        side_effects = (
            datetime.datetime(2020, 7, 2, 15, 3, 10),
            datetime.datetime(2020, 7, 2, 16, 3, 10),
        )
        local_datetime.now.side_effect = side_effects
        local_datetime.datetime.now.side_effect = side_effects

        article.content = "'I know I'm not stupid,' the man thought,"
        self.assertEqual(side_effects[0], article.last_edited)

        article.content = "'Magnificent,' said the two officials"
        self.assertEqual(side_effects[1], article.last_edited)

    def test_203_sort(self):
        """Articles should be inherently sortable by their publication date."""
        kwargs = {"title": "a", "author": "b", "content": "c"}
        articles = [
            qualifier.Article(**kwargs, publication_date=datetime.datetime(2001, 7, 5)),
            qualifier.Article(**kwargs, publication_date=datetime.datetime(1837, 4, 7)),
            qualifier.Article(**kwargs, publication_date=datetime.datetime(2015, 8, 20)),
            qualifier.Article(**kwargs, publication_date=datetime.datetime(1837, 4, 7)),
        ]

        expected = [articles[1], articles[3], articles[0], articles[2]]
        try:
            actual = sorted(articles)
        except TypeError:
            self.fail("`Article` does not support sorting.")
        self.assertSequenceEqual(expected, actual)


NOT_A_DESCRIPTOR = "The `ArticleField` class is not a data descriptor."


@unittest.skipUnless(hasattr(qualifier.ArticleField, "__set__"), reason=NOT_A_DESCRIPTOR)
class T300AdvancedTests(unittest.TestCase):
    """Tests for the advanced requirements."""

    minimal_descriptor = hasattr(qualifier.ArticleField, "__set__")

    def setUp(self) -> None:
        """Before running each test, instantiate some classes which use an ArticleField."""
        class TestArticle:
            """Test class which uses an ArticleField."""
            attribute = qualifier.ArticleField(field_type=int)

        self.article = TestArticle()
        self.article_2 = TestArticle()

    def test_301_descriptor_properly_validates_values(self):
        """The ArticleField descriptor successfully get and set a value of a valid type."""
        class CustomInt(int):
            """int subclass used to test that the descriptor considers subclasses valid."""

        values = (10, CustomInt(20))
        for value in values:
            with self.subTest(value=value):
                self.article.attribute = value
                self.assertEqual(
                    value,
                    self.article.attribute,
                    msg="The attribute value is not equal to the value that was assigned to it."
                )

    def test_302_descriptor_raises_type_error(self):
        """Setting a value with an invalid type should raise a TypeError."""
        with self.assertRaises(TypeError, msg="Setting an incorrect type should raise a TypeError"):
            self.article.attribute = "some string"

    def test_303_descriptor_values_are_separate(self):
        """Should store a separate value for each instance of a class using the descriptor."""
        self.article.attribute = 10
        self.article_2.attribute = 20

        self.assertEqual(10, self.article.attribute)
        self.assertEqual(20, self.article_2.attribute)

    def test_304_descriptor_type_error_message(self):
        """Should include the attribute's name, the expected type, and the received type."""
        msg = "expected an instance of type 'int' for attribute 'attribute', got 'str' instead"
        with self.assertRaisesRegex(TypeError, re.escape(msg)):
            self.article.attribute = "some string"
