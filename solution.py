from __future__ import annotations

import collections
import datetime
import itertools
import string
import typing

AnyType = typing.TypeVar("AnyType")


class Article:
    """The `Article` class you need to write for the qualifier."""

    # Class attribute assigned to an instance of `itertools.count` to easily
    # get the next ID for an Article instance during initialization.
    article_id = itertools.count()

    def __init__(self, title: str, author: str, publication_date: datetime.datetime, content: str):
        self.title = title
        self.author = author
        self.publication_date = publication_date

        # Private attribute to allow for property/setter logic. If you did not
        # implement property/setter logic for the Intermediate Requirements, you
        # probably just have `self.content` here.
        self._content = content

        # The attributes below are required for the Intermediate Requirements.
        # Get the next article id
        self.id = next(self.article_id)

        # The initial `last_edited` time is `None`, as specified.
        self.last_edited = None

    def __repr__(self) -> str:
        """
        Return the "official" string representation of an `Article`.

        As the content of articles is often quite long, it's not a good idea to
        include it in the internal representation. That's why we opted to go for
        a representation that should provide enough information to identify the
        article during debugging, but not enough information to be able to
        recreate the article instance directly from the representation.

        To avoid confusion about being able to recreate the object, we followed
        the recommendation in the `Data Model` chapter of the Python Docs and
        used a representation that's wrapped in angle brackets.

        See https://docs.python.org/3/reference/datamodel.html#object.__repr__
        """
        # Dynamically get the name of the class to support subclassing the
        # class without having to override the `__repr__` method.
        cls = self.__class__.__name__

        # Format the publication date using `datetime.datetime.isoformat()`.
        pub_date = self.publication_date.isoformat()

        # The `!r` conversion specifier ensures that we use the `__repr__` of
        # the values for the attributes we include.
        return f"<{cls} title={self.title!r} author={self.author!r} publication_date={pub_date!r}>"

    def __len__(self) -> int:
        """
        Return the length of the article in terms of the length of its content.

        You can use the special method `__len__` to implement support for the
        built-in function `len()`. Whenever you call `len` with an object as the
        argument, `len` will look for this method to get the length.

        In this case, it's very easy to just delegate the work to the `len`
        implementation of the `str` object we use for the content. This is a
        very common pattern in Python, as we often "compose" our own classes
        by using instances of other classes to hold data.

        See: https://docs.python.org/3/reference/datamodel.html#object.__len__
        """
        return len(self._content)

    def short_introduction(self, n_characters: int) -> str:
        """
        Return an introduction of the article that is at most `n_characters` long.

        The method will return up to `n_characters` from the start of the
        content of the Article. If the content is longer than `n_characters`, it
        will look for the rightmost space or newline character it can use to cut
        the content so the introduction is at most `n_characters` long. As
        described in the requirements, this method assumes that such a character
        is always present in the text.
        """
        if len(self._content) <= n_characters:
            # The content is at most `n_characters` long, which means that we
            # can just return it as is.
            return self._content

        # First, we reduce the content down to a slice with a length of
        # `n_characters + 1`. The `+ 1` is important because if that additional
        # character is a space or newline, we can return the first
        # `n_characters` as-is.
        short_content = self._content[:n_characters + 1]

        # Next, we'll find both the rightmost space and newline characters to
        # see which is last. We'll use that one to break on. As `str.rfind`
        # returns `-1` if one of the characters isn't found, this simplifies
        # the comparison later on.
        rightmost_space = short_content.rfind(" ")
        rightmost_newline = short_content.rfind("\n")

        # Determine the separator with greatest index (the rightmost separator).
        rightmost_separator = max((rightmost_space, rightmost_newline))

        # Return a slice of `short_content` using the index we found.
        return short_content[:rightmost_separator]

    def most_common_words(self, n_words: int) -> typing.Dict[str, int]:
        """
        Return the `n_words` most common words with their counts.

        The method uses the order in which words first occurred in the content
        of the Article to break ties. If there are two words with the same
        count, but there's only one spot left in the dictionary, this method
        includes the one that was used first in the Article.

        As mentioned in the requirements, this method ignores the case of words
        and treats all non-alphabet characters as word boundaries. The words
        returned in the dictionary will be returned in lowercase.
        """
        # First, we get rid of the uppercase characters by using `str.lower`.
        lowercase_content = self._content.lower()

        # We don't care about the specific character that separates different
        # words; we just want to split the string up into words later. To do
        # this, we simply replace all non-alphabet characters by a space
        # character. The `str.split()` we use later doesn't care about the
        # string having multiple spaces in a row, so we don't have to worry
        # about that.
        clean_content = "".join(
            char if char in string.ascii_lowercase else " "
            for char in lowercase_content
        )

        # Use `str.split` to split the string up into words
        words = clean_content.split()

        # Use `collections.Counter` to count the occurrences of words.
        word_counts = collections.Counter(words)

        # Use the `most_common` method of `collections.Counter` to get a list
        # of the `n_words` most common words and their counts, and turn the
        # result into a `dict` again.
        most_common_words = dict(word_counts.most_common(n_words))

        return most_common_words

    # Start of the Intermediate Requirements section
    @property
    def content(self) -> str:
        """
        Return the content of the Article.

        This property is implemented so we can use a `setter` method for the
        content attribute as well. This allows us to capture the datetime of the
        last edit that was made to the content.
        """
        return self._content

    @content.setter
    def content(self, new_content: str) -> None:
        """Set a new value for content and capture the `last_edit` datetime."""
        self.last_edited = datetime.datetime.now()
        self._content = new_content

    def __lt__(self, other: Article) -> typing.Union[bool, NotImplemented]:
        """
        Return `True` if this Article was published earlier than the `other` Article.

        The built-in sorting algorithm is guaranteed to use this method to compare
        objects for sorting purposes. That's why implementing this method also adds
        support for `sorted` and `list.sort`. When a rich comparison operator is
        not supported between pairs of objects, this method should return the
        `NotImplemented` singleton. This allows Python to look for the reverse
        operation, `__gt__`, in the `other` object.
        """
        # This method only implements `<` between `Article` instances,
        if not isinstance(other, Article):
            return NotImplemented

        return self.publication_date < other.publication_date


class ArticleField:
    """The `ArticleField` class for the Advanced Requirements."""

    def __init__(self, field_type: typing.Type[typing.Any]):
        self.field_type = field_type
        self.attribute_name = None

    def __repr__(self) -> str:
        """Return the 'official' string representation of the descriptor."""
        cls_name = self.__class__.__name__
        return f"<{cls_name} descriptor with field_type={self.field_type!r}>"

    def __set_name__(self, owner: typing.Type[typing.Any], name: str) -> None:
        """
        Capture the fully qualified name assigned to the descriptor instance.

        As Python allows you to alias the descriptor instance by assigning another
        class attribute to the descriptor instance, we only capture the name the
        first time `__set_name__` runs.

        This is similar to what happens when creating function objects: The `__name__`
        attribute of the function object is only assigned when the function object is
        first created. Subsequent aliasing of the function by assigning another name
        to it does not change the `__name__` attribute.

        >>> def foo(): pass
        >>> foo.__name__
        'foo'
        >>> bar = foo
        >>> bar.__name__
        'foo'
        """
        if self.attribute_name is None:
            self.attribute_name = name

    def __get__(self, obj: typing.Optional[AnyType], owner: typing.Type[AnyType]) -> typing.Any:
        """Get the value from `obj.__dict__` using `self.attribute_name`."""
        # If the attribute is accessed via the `owner` class object, we return
        # the descriptor itself. This allows for easier introspection of the
        # descriptor.
        if obj is None:
            return self

        # Try to get the actual value from `obj.__dict__`. Since this raises
        # a KeyError, not an AttributeError, when no value was set yet, we
        # catch the exception and raise an AttributeError instead.
        try:
            value = obj.__dict__[self.attribute_name]
        except KeyError:
            cls_name = owner.__name__
            raise AttributeError(
                f"{cls_name!r} object has no attribute {self.attribute_name!r}"
            ) from None

        return value

    def __set__(self, obj: typing.Optional[AnyType], new_value: typing.Any) -> None:
        """Store the new value for attribute in obj.__dict__ after validating its type."""
        if not isinstance(new_value, self.field_type):
            # Get the names of the expected type and the actual type of the new_value
            expected_type = self.field_type.__name__
            actual_type = type(new_value).__name__

            # Raise a type error to indicate that actual type did not validate.
            raise TypeError(
                f"expected an instance of type {expected_type!r} for attribute "
                f"{self.attribute_name!r}, got {actual_type!r} instead."
            )

        obj.__dict__[self.attribute_name] = new_value
