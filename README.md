# Summarify

**Summarify** is a small Python library to extract a title and description from a Web page.

```python
import summarify

summary = summarify.from_url("https://github.com/")

print(summary.title)
print(summary.description)
print(summary.picture)
```
Output:
```text
The world's leading software development platform · GitHub
GitHub is where people build software. More than 27 million people use GitHub to discover, fork, and contribute to over 75 million projects.
https://assets-cdn.github.com/images/modules/open_graph/github-octocat.png
```

## Install

    pip3 install summarify

## Usage

```python
import summarify

summary = summarify.from_url("https://...")

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

You can also export a summary as a `dict` for e.g. JSON serialization:

```python
dict(my_summary)  # -> {"url": "...", "title": "..."}
```

Be aware that only the non-`None` attributes are included in that dictionnary.
