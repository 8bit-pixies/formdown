# generate forms from markdown
# based on the sample spec from [stackoverflow](http://stackoverflow.com/questions/5759661/wiki-or-markdown-like-syntax-for-simple-forms)

"""
Markdown Spec:
    name = _____
    gender = (X) Male () Female
    checklist = [x] item 1 [] item 2 [] item 3
    textbox = [[]]
    selection = {item 1, (item 2), item 3}
    date:datepicker = ________

To generate calendars or anything similar, the appropriate jquery/javascript must be in the website to work.
"""

"""
Usage:
```
print parse_form("A form\nname=____\ndate:datepicker=_____")
```
"""

import re
from functools import partial

class Form:
    def __init__(self, formdown):
        """assumes  markup is valid"""
        if '=' in formdown:
            name, self.input_info = tuple(formdown.split('=', 1))
            raw_name = name.lower().strip()
        else:
            raw_name = formdown
        
        # split name...if var is declared
        if ':' in raw_name:
            self.name, self.vclass = tuple(raw_name.split(':', 1))
        else:
            self.name = raw_name
    
    def get_name(self):           
        return self.name
    
    def get_class(self):
        try:
            return self.vclass.strip()
        except:
            return False
        
    def label(self):
        return "<label>%s</label>" % self.get_name().title()
    
    def add_class(self):
        """
        adds class with the name from get_class. 
        
        This was designed with 'datepicker' in mind.
        """
        if self.get_class():
            return 'class="%s"' % self.get_class()
        else:
            return ''
  
    def input_text(self):
        return """<p>%s<input type="text" name="%s" id="%s" %s/></p>\n""" % (self.label(), self.get_name(), self.get_name(), self.add_class())
        
    def input_radio_check(self, typ="radio"):
        """generate the html for the radio or check input"""
        items = [x.title().strip() for x in re.split(r'([\(\[]x?[\)\]])', self.input_info, flags=re.IGNORECASE) if x.strip() != '']
        items = zip(*[items[0::2], items[1::2]])

        input_string = ''
        for selected, item in items:
            input_string += """<input type="%s" name="%s" value="%s" """ % (typ, self.get_name(), item)
            if selected[1] == 'X':
                input_string += ' checked="checked" '
            input_string += ' /> %s' % item
        return """<p>%s%s</p>""" % (self.label(), input_string)
        
    def input_select(self):
        """generate the html for the select tag"""
        items = self.input_info.strip()[1:-1].split(',') # strip out the braces
        

        select = ''
        for item in items:
            item = item.strip()
            if item[0] == '(' and item[-1] == ')':
                select += """<option value="%s" selected='selected'>%s</option>\n""" % (item[1:-1], item[1:-1]) # strip out the parenthesis
            else:
                select += """<option value="%s" >%s</option>\n""" % (item, item)
        
        return """<p>%s<select name="%s">%s</select></p>""" % (self.label(), self.get_name(), select)
    
    def input_textbox(self):
        return """<p>%s<textarea name="%s" id="%s"></textarea></p>""" % (self.label(), self.get_name(), self.get_name())
    
    def generate_form(self):
        try:
            symbol = self.input_info.strip()        
            if symbol.startswith('[['):
                symbol = '[['
            else:
                symbol = symbol[0]
        except:
            symbol = ''
        
        symbol_map = {'_' : self.input_text,
                      '(' : self.input_radio_check,
                      '[' : partial(self.input_radio_check, typ = 'checkbox'),
                      '{' : self.input_select,
                      '[[' : self.input_textbox}
        return symbol_map.get(symbol, self.label)()


def parse_form(form):
    """parses the form into sections"""    
    return '\n'.join([Form(x).generate_form() for x in form.strip().split('\n')])+"""\n<p><input type="submit" value="Submit"></p>"""

