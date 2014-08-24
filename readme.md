Readme
======

`formdown` is a markdown inspired markup language for html forms. It is based on the proposed markup on [stackoverflow](http://stackoverflow.com/questions/5759661/wiki-or-markdown-like-syntax-for-simple-forms).

Testing
-------

The tests (incomplete) can be run by typing:

```
nosetests
```

Installation
------------

To install it in your Python installation run:

```python
python setup.py install
```

Format Specification
--------------------

Using the specification as defined below, we can generate the forms.

*   `text = _____`
*   `gender = (X) Male () Female`
*   `checklist = [x] item 1 [] item 2 [] item 3`
*   `textbox = [[]]`
*   `selection = {item 1, (item 2), item 3}`
*   `date:datepicker = ________`

```python
print formdown.parse_form("name=____\ndate:datepicker=_____")
```

Output:

```html
<p><label>Name</label><input type="text" name="name" id="name" /></p>
<p><label>Date</label><input type="text" name="date" id="date" class="datepicker"/></p>
<p><input type="submit" value="Submit"></p>
```

Usage with Datepicker
---------------------

To use this with datepicker, simply follow the information contained on the [homepage](http://jqueryui.com/datepicker/). Remember to change the script since `"datepicker"` is not an `id` but a `class` in `formdown`.

i.e.

```js
$(function() {
  $( ".datepicker" ).datepicker();
});
```

Copyright and license
---------------------

Code and documentation copyright 2014 Chapman Siu. Code released under [the MIT license](https://github.com/chappers/formdown/blob/master/license.md). 
