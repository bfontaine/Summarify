# Summarify

**Summarify** is a small Python library to extract a title and description from
a Web page.

```python
import summarify

summary = summarify.from_url("https://github.com/")

print("#", summary.title)
print(summary.description)
print("%s (%s)" % (summary.url, summary.language))
prin(summary.picture)
```
Output:
```text
# The world's leading software development platform · GitHub
GitHub is where people build software. More than 27 million people use GitHub to discover, fork, and contribute to over 75 million projects.
https://github.com/ (en)
https://assets-cdn.github.com/images/modules/open_graph/github-octocat.png
```

Work in progress: the main features are implemented but the code is still
missing unit tests.

## Install

    pip3 install summarify

## Usage

```python
import summarify

summary = summarify.from_url(YOUR_URL_HERE)

# If you already have the HTML:
# summary = summarify.from_html("...")
```

The `Summary` object returned from `summarify.from_url` has the following
attributes:

* `title` (`str` or `None`)
* `description` (`str` or `None`)
* `url` (`str` or `None`): The URL you passed as an argument. If you used
  `summary.from_markup`, it’ll try to guess it from the markup.
* `picture` (`str` or `None`): Picture URL
* `author` (`str` or `None`)
* `publisher` (`str` or `None`)
* `excerpt`: Always `None` for now
