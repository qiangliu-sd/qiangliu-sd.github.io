# Enforced Dynamic-Range Tkinter-Validating with JSON

If you use Python Tkinter to design a GUI to obtain user inputs, you’d better validate the inputs entered by users. With the `Entry` widget, you can do so by configuring three options, namely `validate`, `validatecommand`, and invalidcommand, such as:
```
vCmd = (self.register(self.validatePositive), '%P')
ivCmd = (self.register(self.invalidatePositive), '%P')
uEntry.config(validate='focusout', validatecommand=vCmd, invalidcommand=ivCmd)
```
where the member function (method) validatePositive checks whether the user input is a positive number, and invalidatePositive executes if validatePositive returns false (or the user input is invalid or not positive).

Note that the option invalidcommand is unnecessary because, in most cases, invalidatePositive merely alerts the user that the input is invalid, which can be included in validatecommand.

Online examples of Tkinter-validating lack two features at least. First, the **validation is not enforced**. When users click another widget (or focus is out), an invalid input is kept without further notice. Second, you may have **dynamic bounds for different Entries** to validate. For example, you may have one valid Entry between 0 and 1, but another between 5 and 10. Clearly, it would be a bad idea to hardcode the bounds [0,1] and [5,10] in your implementation.

### Enforced Validating

You can enforce an Entry widget’s validation by returning the focus to the widget, given that the input is invalid. You can do this by `nametowidget(widget_name).focus_set()`, if you know the widget’s name. Fortunately, the widget name is available via the substitution code '%W'. Therefore, we have:
```
vCmd = (self.register(self.validatePositive), '%P', '%W')
uEntry.config(validate='focusout', validatecommand=vCmd)

def validatePositive(self, g_input, widget_name):    
        if re.match(r"^[0-9]*\.?[0-9]+$", g_input) and float(g_input)>0.0: return True
        mb.showerror("BAD Input", f"{g_input}: NOT positive")
        self.nametowidget(widget_name).focus_set()
        return False
```

You may think that you are done with enforced validating. Unfortunately, you are not quite there yet. If a user clicks a `Button`, the “focus-out” event of Entry is not triggered. Consequently, the validation is not bulletproof. And you need to make the validation better.

### Bulletproof Enforced Validating

You will have to check for any invalid input after Button is clicked. With tens of user inputs, you could check each input one by one. Instead, it is better to add a class variable, `_inputValid`, to store the valid-status by setting it to true (false) inside validatePositive.

Then, you only have to check _inputValid inside Button click. That sounds great, right? Unfortunately, again, you can modify input to an invalid one without triggering the focus-out event (and thus failing to set `_inputValid` to false), by immediately clicking a Button! Therefore, you must force a focus-out event as the first step inside Button click.

Ideally, you want to **force a focus-out event** (and set the valid-status to false), but you do **not want to bother the user noticeably with additional message boxes**. You can use an independent timed window to achieve this effect, which **pops up after being called and automatically disappears**. Interestingly, at least [20 milliseconds is necessary](#Note) for the GUI to work correctly (see [fleetingPopup](ql_md_template.html?my.md=coding/proglangs/py_free-msg-box.md) and [TkinterGUI.bSaveClicked](https://github.com/qiangliu-sd/enforcedDynaPyTkValid)).

### Dynamic-Range Validating

JSON would be a good choice for dynamic validating, since users can specify the necessary validations in json. For example, a flexible json for GUI can be defined as:
```
{ key: [caption, value, < tooltip, <validate-code> >] }
```
where tooltip or validate-code is optional.
Sample json entries look like this:
```
"cvt_notice_period": ["Convert notice period (days)",  "0"],
"par_nominal": ["Conv-bond par", "100","positive","plus"],
"maturity": ["CB mature date", "3/2/2026", "date_fmt","date_us"],
"convert_cash": ["Cash amount in convert", "0", "not_neg","non_minus"],
"afv_eta":["Ratio of stock price jump at default (AFV)", "0", "afv_eta", "btw_0_1"],
```
You can pass in the validate-code, btw_0_1, as valid_code and extract the bound [0,1] inside as:
```
def validateInBtw(self, g_input, widget_name, valid_code):   
        """Args [valid_code] by client: 
            dynamic-range [3,7] coded as btw_3_7 in JSON
        """
        x,lowB,highB = valid_code.split("_")   # lowB: low-bound
        if self.isNonNegative(g_input):
            if float(lowB) <= float(g_input) and float(g_input) <= float(highB):  
                self.setValid(True)
                return True
                
        mb.showerror("BAD Input", f"{g_input}: NOT between {lowB} and {highB}")
        self.nametowidget(widget_name).focus_set()
        self.setValid(False)
        return False
```
and register validateInBtw as follows:
```
vCmd = (self.register(self.validateInBtw), '%P', '%W', valid_code)
```
For the full implementation, check out TkinterGui.py and LableEntryGrid.py in [my GitHub Repo](https://github.com/qiangliu-sd/enforcedDynaPyTkValid).

### Note:
<a name="Note"></a>
In the first run of TkinterGui.py, enforced validating may fail with a 10-milliseconds fleetingPopup. It’s believed that the compiling (into bytecode) time messes up the execution sequence of the Python statements.