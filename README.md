# Summer Code Jam 2020: Qualifier

To qualify for the upcoming Summer Code Jam, you'll have to complete a qualifier assignment. In the assignment, you will be asked to write an `Article` class that could be used to represent an article published on a website.

Please read the instructions carefully and submit your solution before the deadline using the sign-up form. Also note that **we've included a test suite** that you can use to test your solution before you submit it.

## Table of Contents

- [Qualifying for the Code Jam](#qualifying-for-the-code-jam)
- [Rules and Guidelines](#rules-and-guidelines)
- [Qualifier Assignment](#qualifier-assignment)
  - [Basic Requirements](#basic-requirements)
  - [Intermediate Requirements](#advanced-requirements)
  - [Advanced Requirements](#advanced-requirements)
- [Test Suite](#test-suite)
  - [Running the Test Suite](#running-the-test-suite)

## Qualifying for the Code Jam
The qualifier assignment has three sections of increasing difficulty:

1. [Basic Requirements](#basic-requirements)
2. [Intermediate Requirements](#advanced-requirements)
3. [Advanced Requirements](#advanced-requirements)

To qualify for the Code Jam, your solution has to **pass the basic requirements**. However, we do want to urge you to at least try the intermediate and/or advanced requirements if you think you can tackle them. We will publish our solution for the qualifier after the deadline has passed.

## Rules and Guidelines

- Your submission will be tested using a Python 3.8.3 interpreter with no additional packages installed. This means that you're allowed to use everything that is included in Python's standard library, but nothing else. Please make sure to include the relevant `import`-statements in the solution you submit.

- Use [`qualifier.py`](qualifier.py) as the base for your solution. It includes stubs for the two classes you need to write: `Article` and `ArticleField`.

- Do not change the **names** of the two classes included in [`qualifier.py`](qualifier.py). The test suite that we will use to judge your submission relies on existence these two classes. Everything else, including the docstring of the classes, may be changed.

- You can leave the `ArticleField` class as-is if you do not wish to tackle the advanced requirements.

- Do not include "debug"-code in your submission. This means that you should remove all debug prints and other debug statements before you submit your solution.

- This qualifier task is supposed to be **an individual challenge.** This means that you should not discuss (parts of) your solution to the qualifier task in public (including our server) and that you should try to solve it individually. Obviously, this does not mean that you can't do research or ask questions about the Python concepts you're using to solve the qualifier, but try to use general examples when you post code during this process.

## Qualifier Assignment

For this assignment, you'll write an `Article` class to represent articles published to a blog. The `Article` objects you can create with this class will have attributes like `title` and `author` and you will write a few methods to work with these objects. We've added a "stub" for your `Article` class in the [`qualifier.py`](qualifier.py) file for you extend.

Please read the requirements below carefully, as it's important that the code you write meets those requirements exactly. Also note that there's a [test suite](#test-suite) available for  you to test your code before you submit it.

For all of the examples below, assume that we've created an instance of `Article` like this:

```py
>>> fairytale = Article(
...     title="The emperor's new clothes",
...     author="Hans Christian Andersen",
...     content="'But he has nothing at all on!' at last cried out all the people. The Emperor was vexed, for he knew that the people were right.",
...     publication_date=datetime.datetime(1837, 4, 7, 12, 15, 0),
... )
```

### Basic Requirements

_The requirements listed in this section only apply to the `Article` class._

1. Write an `__init__` method that stores the arguments for the four parameters as attributes. The attributes should be publicly available using the same names as the parameters:

    ```py
    >>> fairytale.title
    "The emperor's new clothes"
    >>> fairytale.publication_date
    datetime.datetime(1837, 4, 7, 12, 15, 0)
    ```

2. To make debugging easier, implement a `__repr__` method that returns a string representation that matches this format exactly:
    ```py
    >>> print(repr(fairytale))
    <Article title="The emperor's new clothes" author='Hans Christian Andersen' publication_date='1837-04-07T12:15:00'>
    ```
    - The value for `publication_date` is formatted using `datetime.datetime.isoformat()`.
    - Make sure to use the `repr` of the values for `title`, `author`, and `publication_date.isoformat()`.

3. As it's also nice to know how long an article is, implement support for the built-in function `len`. The value it should return is the length of the value for `content`:
    ```py
    >>> fairytale.content
    "'But he has nothing at all on!' at last cried out all the people. The Emperor was vexed, for he knew that the people were right."
    >>> len(fairytale)
    128
    ```

4. Blogs often feature a short section of an article on their frontpage. Write a method called `short_introduction` that takes an `int` as an argument for `n_characters` and returns such a short introduction that contains **at most** `n_characters` from the start of the article's `content`. To not "break-off" awkwardly in the middle of a word, you should find the last space or newline character before you go over `n_characters` and break on that. You may assume that there's always a space or newline character to break on in the first `n_characters`.
    ```py
    >>> fairytale.short_introduction(n_characters=60)
    "'But he has nothing at all on!' at last cried out all the"
    ```
    - The value returned by `Article.short_introduction` should **not** include the space/newline character you used to break up the text.

5. It's often interesting to have some statistics to show on your blog. Write a method called `most_common_words` that takes a single `int` as an argument for `n_words` and returns a dictionary of the `n_words` most common words in the `content` of the article. Words that are tied in frequency should be ordered in the order in which they first appeared in the `content` and you should ignore the case of the words (`"The"` and `"the"` count as the same word).
    ```py
    >>> fairytale.most_common_words(5)
    {'the': 3, 'he': 2, 'at': 2, 'all': 2, 'people': 2}
    >>> fairytale.most_common_words(3)
    {'the': 3, 'he': 2, 'at': 2}
    ```
   - Output the words in lowercase in the dictionary.
   - Every non-alphabet character counts as a space/wordbreak; this means that `"It's"` counts as two "words": `"it"` and `"s"`.

### Intermediate Requirements

_The requirements listed in this section only apply to the `Article` class. Please make sure that the changes you make for the requirements this section don't break any of the requirements listed in the previous section._

1. A common way of uniquely identifying an article is by giving it a unique `id` number. Add a feature to the class that gives each new `Article` that you create a unique `id` number. The numbers should be sequential and, in good Python tradition, the first article should get an `id` of `0`:
    ```py
    >>> article_one = Article(title="PEP-8", author="Guide van Rossum", content="Use snake_case", publication_date=datetime.datetime(2001, 7, 5))
    >>> article_one.id
    0
    >>> article_two = Article(title="Fluent Python", author="Luciano Ramalho", content="Effective Programming", publication_date=datetime.datetime(2015, 8, 20))
    >>> article_two.id
    1
    ```
    - You should not define anything outside of the class definition to accomplish this, so no "global" variables.

2. Making mistakes is human and so is trying to fix them. Keep track of the moment the most recent change to the article's `content` was made with a new attribute, `last_edited`. Each time a new value is set for the `content` attribute, you should automatically keep track of the current date and time by using `datetime.datetime.now()`. To not make a breaking change to the "API" of the class, `content` should still be accessed and changed with normal attribute access. Set the initial value of `last_edited`, before the first edit was made, to `None` in the `__init__`.
    ```py
    >>> fairytale.last_edited
    None
    >>> fairytale.content = "I'm making a change to the content of this article"
    >>> fairytale.last_edited
    datetime.datetime(2020, 5, 26, 19, 41, 10)  # My local time at the time of writing
    ```

3. A common operation on a collection of articles is to sort them by their publication date. Implement support for sorting `Article` objects directly without having to use a `key` function for `sorted` or `list.sort`. The sorting order should be based solely on the `publication_date` attribute and sorting in ascending order (the default) should result in the oldest article first.
    ```py
    >>> articles = [
    ...     Article(..., publication_date=datetime.datetime(2001, 7, 5)),
    ...     Article(..., publication_date=datetime.datetime(1837, 4, 7)),
    ...     Article(..., publication_date=datetime.datetime(2015, 8, 20),
    ... ]
    >>> sorted(articles)
    [<Article ... publication_date="1837-04-07T...">, <Article ... publication_date="2001-07-05T...">, <Article ... publication_date="2015-8-20T...">]
    ```

### Advanced Requirements

_The requirements in this section will ask you to implement the `ArticleField` class. It is not necessary to make changes to the `Article` class, but if you do, make sure that the tests for the requirements in previous sections still pass._

While duck typing is a common practise in Python, the data of to articles will probably have to be saved to a database with a rigid data types scheme. That's why we want to introduce some type checking for attributes to catch errors early rather than late. In this section, you'll implement a simple descriptor that checks if the value we are trying to assign to an attribute has the correct type.

1. Implement a descriptor, `ArticleField`, that checks if the value we are trying to assign to an instance attribute has the correct type. As we want to be able to reuse the same descriptor class for different types, its `__init__` method expects one argument (for `field_type`): the type it should check against. To not be too rigid, the type check should allow instances of subclasses of the type in addition to the type itself.

    If the value has the correct type, the assignment should happen normally; if not, the descriptor should raise a [`TypeError`](https://docs.python.org/3/library/exceptions.html#TypeError):
    ```py
    >>> class Article:
    ...     attribute = ArticleField(field_type=int)
    >>> article = Article(...)
    >>> article.attribute = 10
    >>> article.attribute
    10
    >>> article.attribute = "some string"
    Traceback (most recent call last):
        ...
    TypeError: some message here
    >>> article.attribute
    10
    ```

2. Whenever you raise an exception, it's important to give the developer who will have to deal with the exception enough information to know what's going on. That's why the exception message should include the name of the attribute we're trying to assign something to, the name of type that was expected, and the name of the type that it received instead. If you had not done that already, adjust your descriptor so that it always includes those three pieces of information in the exception message. You should not change the function signature of the `__init__` method to do this (i.e., you can't pass the name of the attribute to `__init__`).
    ```py
    >>> class Article:
    ...     age = ArticleField(field_type=int)
    >>> article = Article(...)
    >>> article.age = "some string"
    Traceback (most recent call last):
        ...
    TypeError: expected an instance of type `int` for attribute `age`, got `str` instead
    ```

## Test Suite
To help you test your solution before submitting it, we've written a basic test suite that tests if your code passes the requirements. In principle, if your solutions passes the basic requirements section in this test suite, you should qualify for the Code Jam.

It's perfectly fine to have a look at the tests that we are going to run (see [test_qualifier.py](test_qualifier.py)), but do note that we will run the tests with different data to ensure that solutions were not written specifically for the included tests.

### Running the Test Suite

To run the test suite, first download and place the files [`test_qualifier.py`](test_qualifier.py) and [`run_test.py`](run_test.py) in the same directory as the file containing your solution. After having done so, open a terminal/command window with that directory as the working directory and run:

```
python run_test.py <your_filename_here>
```

**Note:** You may have to replace `python` with the command you use to run Python from the command line. If you're not sure and are using Windows, try `py` instead of `python` if `python` doesn't work.

The test suite has been tested with Python 3.7 and Python 3.8.
