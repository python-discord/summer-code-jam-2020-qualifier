# Summer Code Jam 2020: Qualifier

To qualify for the upcoming Summer Code Jam, you'll have to complete a qualifier assignment. For the assignment, you'll have to write an `Article` class that could be used to represent an article published on a website.

Please read the instructions carefully and submit your solution before the deadline using the [sign-up form](https://forms.gle/RpGCrLXyn8U92c156). Also, note that **we've included a test suite** you can use to test your solution before you submit it.

- **Deadline:** July 22, 2020  
- **Sign-up form:** [https://forms.gle/RpGCrLXyn8U92c156](https://forms.gle/RpGCrLXyn8U92c156)

## Table of Contents

- [Qualifying for the Code Jam](#qualifying-for-the-code-jam)
- [Rules and Guidelines](#rules-and-guidelines)
- [Qualifier Assignment](#qualifier-assignment)
  - [Basic Requirements](#basic-requirements)
  - [Intermediate Requirements](#intermediate-requirements)
  - [Advanced Requirements](#advanced-requirements)
- [Test Suite](#test-suite)
  - [Running the Test Suite](#running-the-test-suite)

## Qualifying for the Code Jam
The qualifier assignment has three sections of increasing difficulty:

1. [Basic Requirements](#basic-requirements)
2. [Intermediate Requirements](#intermediate-requirements)
3. [Advanced Requirements](#advanced-requirements)

To qualify for the Code Jam, your solution has to **pass the basic requirements**. However, we urge you to at least try the intermediate and/or advanced requirements if you think you can tackle them. We will publish our solution for the qualifier after the deadline has passed.

## Rules and Guidelines

- Your submission will be tested using a Python 3.8.3 interpreter without any additional packages installed. You're allowed to use everything included in Python's standard library, but nothing else. Please make sure to include the relevant `import` statements in your submission.

- Use [`qualifier.py`](qualifier.py) as the base for your solution. It includes stubs for the two classes you need to write: `Article` and `ArticleField`.

- Do not change the **names** of the two classes included in [`qualifier.py`](qualifier.py). The test suite we will use to judge your submission relies on these two classes. Everything else, including the docstrings of the classes, may be changed.

- You can leave the `ArticleField` class as-is if you do not wish to tackle the advanced requirements.

- Do not include "debug" code in your submission. You should remove all debug prints and other debug statements before you submit your solution.

- This qualifier task is supposed to be **an individual challenge**, so try to solve it on your own. You should not discuss (parts of) your solution in public (including our server). You are still allowed to do research and ask questions about Python as they relate to your qualifier solution, but try to use general examples if you post code along with your questions.

## Qualifier Assignment

For this assignment, you'll write an `Article` class to represent articles published to a blog. Instances of this class will have attributes like `title` and `author`. You will also write a few methods to work with these classes. We've added a "stub" for your `Article` class in the [`qualifier.py`](qualifier.py) file for you fill in.

Please read the requirements below carefully; it's important for your code to meet those requirements exactly. Also, note that there's a [test suite](#test-suite) available for you to test your code before you submit it.

For all the examples below, assume we've created an instance of `Article` like this:

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

1. Write an `__init__` method that stores the arguments for the four parameters (`title`, `author`, `content`, and `publication_date`) as attributes. The attributes should be publicly available using the same names as the parameters.

    ```py
    >>> fairytale.title
    "The emperor's new clothes"
    >>> fairytale.publication_date
    datetime.datetime(1837, 4, 7, 12, 15, 0)
    ```

2. To make debugging easier, implement a `__repr__` method that returns a string representation of the class. It should exactly match the following format:
    ```py
    >>> print(repr(fairytale))
    <Article title="The emperor's new clothes" author='Hans Christian Andersen' publication_date='1837-04-07T12:15:00'>
    ```
    - The value for `publication_date` is formatted using `datetime.datetime.isoformat()`.
    - Make sure to use the `repr` of the values for `title`, `author`, and `publication_date.isoformat()`.

3. As it's nice to know how long an article is, implement support for the built-in function `len`. It should return the length of `content`.
    ```py
    >>> fairytale.content
    "'But he has nothing at all on!' at last cried out all the people. The Emperor was vexed, for he knew that the people were right."
    >>> len(fairytale)
    128
    ```

4. Blogs often feature a short section of an article on their front page. Write a method called `short_introduction` that has an `int` parameter named `n_characters`. The method should return a short introduction that contains **at most** `n_characters` from the start of the article's `content`. To avoid awkwardly cutting off text in the middle of a word, find and "cut" the text on the last space or newline character within the first `n_characters + 1`. You may assume there's always at least one space or newline character within the first `n_characters + 1`.
    ```py
    >>> fairytale.short_introduction(n_characters=60)
    "'But he has nothing at all on!' at last cried out all the"
    ```
    - The value returned by `Article.short_introduction` should **not** include the space or newline character you used to break up the text.

5. It's often interesting to have some statistics to show on your blog. Write a method called `most_common_words` that has an `int` parameter named `n_words`. The method should return a dictionary of the `n_words` most common words in the `content` of the article. If words have the same frequency, order them in the same order in which they first appeared in the `content`. The method should also be case-insensitive (for example, `"The"` and `"the"` count as the same word).
    ```py
    >>> fairytale.most_common_words(5)
    {'the': 3, 'he': 2, 'at': 2, 'all': 2, 'people': 2}
    >>> fairytale.most_common_words(3)
    {'the': 3, 'he': 2, 'at': 2}
    ```
   - Output the words in lowercase in the dictionary.
   - Every non-alphabet (ASCII only) character counts as a space or word break. For example, `"It's"` counts as two "words": `"it"` and `"s"`.

### Intermediate Requirements

_The requirements listed in this section only apply to the `Article` class. Please make sure the changes you make for the requirements this section don't break any of the requirements listed in the previous section._

1. A common way to uniquely identify an article is to give it a unique number. Add a feature to the class that gives each new `Article` a unique `id` number. The numbers should be sequential and, in good Python tradition, the first article should get an `id` of `0`.
    ```py
    >>> article_one = Article(title="PEP-8", author="Guide van Rossum", content="Use snake_case", publication_date=datetime.datetime(2001, 7, 5))
    >>> article_one.id
    0
    >>> article_two = Article(title="Fluent Python", author="Luciano Ramalho", content="Effective Programming", publication_date=datetime.datetime(2015, 8, 20))
    >>> article_two.id
    1
    ```
    - You should not define anything outside of the class definition to accomplish this; do not use "global" variables.

2. Making mistakes is human and so is trying to fix them. Add a feature to keep track of when the most recent change was made to the article's `content`. Create a new attribute named `last_edited` and set its initial value to `None`. When a change is made to the `content`, obtain the current date and time with `datetime.datetime.now()` and assign it to `last_edited`. To avoid making breaking changes to the class's "API", `content` should still be accessed and changed with normal attribute access.
    ```py
    >>> fairytale.last_edited
    None
    >>> fairytale.content = "I'm making a change to the content of this article"
    >>> fairytale.last_edited
    datetime.datetime(2020, 5, 26, 19, 41, 10)  # My local time at the time of writing
    ```

3. A common operation on a collection of articles is to sort them by their publication date. Add support for sorting `Article` objects directly without having to use a `key` function for `sorted` or `list.sort`. The sorting order should be based solely on the `publication_date` attribute. Sorting in ascending order (the default) should result in the oldest article being first.
    ```py
    >>> articles = [
    ...     Article(..., publication_date=datetime.datetime(2001, 7, 5)),
    ...     Article(..., publication_date=datetime.datetime(1837, 4, 7)),
    ...     Article(..., publication_date=datetime.datetime(2015, 8, 20)),
    ... ]
    >>> sorted(articles)
    [<Article ... publication_date="1837-04-07T...">, <Article ... publication_date="2001-07-05T...">, <Article ... publication_date="2015-8-20T...">]
    ```

### Advanced Requirements

_The requirements in this section will ask you to implement the `ArticleField` class. It is not necessary to make changes to the `Article` class, but if you do, make sure the tests for the requirements in previous sections still pass._

While duck typing is a common practice in Python, type checking can come in handy. For example, articles will probably have to be saved to a database with a rigid data type scheme. The types of the article's attributes can be checked upon assignment to catch type errors early rather than late. In this section, you'll implement a simple descriptor that checks if the value assigned to an attribute has the correct type.

1. Implement a descriptor, `ArticleField`, that checks if the value assigned to an instance attribute has the correct type. To make the descriptor reusable for different types, its `__init__` method should have a `field_type` parameter, which is the type it should check against. To not be too rigid, the type check should allow instances of subclasses of the type in addition to the type itself.

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

2. Whenever you raise an exception, it's important to give the developer enough information to debug the error. Modify your descriptor's exception message to include the name of the attribute being assigned, the name of type that was expected, and the name of the type that was received instead. You should not change the function signature of the `__init__` method to do this; do not pass the name of the attribute to `__init__`. The message should exactly match the following format:
    ```py
    >>> class Article:
    ...     age = ArticleField(field_type=int)
    >>> article = Article(...)
    >>> article.age = "some string"
    Traceback (most recent call last):
        ...
    TypeError: expected an instance of type 'int' for attribute 'age', got 'str' instead
    ```

## Test Suite
We've written a basic test suite that tests if your code passes the requirements above. We strongly suggest you run these tests before you submit your solution. In principle, if your solutions passes the tests for the basic requirements, you should qualify for the Code Jam.

It's perfectly fine to have a look at the tests (see [test_qualifier.py](test_qualifier.py)). This is the same test suite we will use to judge your solution. However, note that we will run the tests with different data to ensure that solutions were not written to only work with the exact data provided.

### Running the Test Suite

To run the test suite, first download the files [`test_qualifier.py`](test_qualifier.py) and [`run_tests.py`](run_tests.py). Place these files in the same directory as the file containing your solution and **make sure the file containing your solution is called `qualifier.py`**. Then, open a terminal/command window and change the current directory to your solution's directory. Finally, run the following command:

```
python run_tests.py
```

**Note:** You may have to replace `python` with the command you use to run Python from the command line. If you're using Windows and `python` doesn't work, try `py` instead. If you're using Linux, you may have to use `python3` instead.

The test suite requires **at least Python 3.7**. It has also been confirmed to work with 3.8.
