# Python Code Style Guide

This document outlines the Python code style conventions to be followed for consistency across the project, derived from `qlMatchNSumUnivsMain.py`.

## Naming Conventions

*   **Module Name:** `modName.py` (snake_case for file names, though the example shows `modName.py` suggesting PascalCase for the conceptual module name)
*   **Constants:** `MY_CONSTANT` (Uppercase with underscores to separate words)
*   **Function Name:** `funcName` (camelCase)
*   **Function Argument:** `arg_in` (snake_case)
*   **Local Variable:** `localVar` (camelCase)
*   **Class Name:** `MyClass` (PascalCase)
*   **Class Private Variable:** `_classVar` (Leading underscore followed by camelCase)
*   **Class Data Variable:** `self.dataVar` (camelCase)
*   **Class Member Function:** `self.membFunc` (camelCase)

## Example from `qlMatchNSumUnivsMain.py`

```python
"""Code-STYLE
   modName.py
   ----------
   MY_CONSTANT
   ----------
   funcName(arg_in):
    localVar
   ----------
   MyClass
    _classVar, self.dataVar, self.membFunc
    arg_in, localVar
"""
```

## Best Practices

### Implementation
*   **Single-Purpose Functions:** A function should do one thing and do it well.
*   **Pass Regex as Arguments:** Avoid hardcoding regular expression patterns inside functions. Pass them as arguments instead.
*   **Appropriate Data Structures:** Use efficient data structures. For example, use tuples or dictionaries instead of lists of dictionaries where appropriate.
*   **Loop Optimization:** Consider the order of loops for better performance.

### General
*   **Module Imports:** Use `from module import function` syntax.
*   **Main Script Logic:** Isolate the main script logic within the `if __name__ == '__main__':` block.
*   **Package Management:** Install required packages manually. Do not include `try-except` blocks for package installation in the code.

## Anti-patterns to Avoid

### Style
*   **Hardcoded Values:** Avoid hardcoding file names, paths, and other constants.
*   **Numbered Variables:** Do not use numbered variable names (e.g., `item1`, `item2`). Use descriptive names instead.
*   **Ambiguous Names:** Avoid using the same variable name for different concepts.
*   **Excessive Indentation:** Keep the code as flat as possible.
*   **Similar Names:** Avoid using similar names for variables and functions to prevent confusion.
*   **Mixed Code:** Do not mix top-level script logic with function and class definitions.

### Implementation
*   **Redundant Code:** Avoid writing the same block of code multiple times.
*   **Unused Code:** Remove any functions or variables that are not being used.
