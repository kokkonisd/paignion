import pytest

from paignion.tools import markdownify, color_message

FULL_MARKDOWN_TEST = """\
# head1
## head2
### head3
#### head4
##### head5
###### head6

this is
the same paragraph

but this is _not_ **the** ~~same~~ `paragraph`

look, a [link](https://github.com/kokkonisd/paignion)

| Table     | Rows  |
| --------- | ----- |
| do tables | work? |

![image](https://github.com/kokkonisd/paignion/raw/master/screenshot.png)\
"""

EXPECTED_HTML_RESULT = """\
<h1>head1</h1>
<h2>head2</h2>
<h3>head3</h3>
<h4>head4</h4>
<h5>head5</h5>
<h6>head6</h6>
<p>this is
the same paragraph</p>
<p>but this is <em>not</em> <strong>the</strong> <del>same</del> <code>paragraph</code></p>
<p>look, a <a href="https://github.com/kokkonisd/paignion">link</a></p>
<table>
<thead>
<tr>
<th>Table</th>
<th>Rows</th>
</tr>
</thead>
<tbody>
<tr>
<td>do tables</td>
<td>work?</td>
</tr>
</tbody>
</table>
<p><img alt="image" src="https://github.com/kokkonisd/paignion/raw/master/screenshot.png" /></p>\
"""


class TestTools:
    def test_markdownify(self):
        # Empty string should return empty string
        assert markdownify("") == ""

        assert markdownify(FULL_MARKDOWN_TEST) == EXPECTED_HTML_RESULT

    def test_colored_string(self):
        res = color_message("hello", color="yellow")
        assert res == "\033[33mhello\033[0m"

        res = color_message("hello", color="orange")
        assert res == "\033[91mhello\033[0m"

        res = color_message("hello", color="red")
        assert res == "\033[31mhello\033[0m"

        # A color that doesn't exist should return the message itself, unchanged
        res = color_message("hello", color="magenta")
        assert res == "hello"
