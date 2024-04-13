---
title: Hello world
---

# Hello World


## Example 1

This code will be displayed as a code block (with syntax highlighting):

```python
print("hello world")
```

## Example 2

This markdown element will load an HTMX:

```
{< htmx:request >}
```

{< htmx:request >}

**NB:**

 - The component to the file `request.py` within the root directory
 - The function `get` will be called

Other examples:

```
{< htmx:hello/world >}  // will look for hello/world.py
```

## Example 3

We can build forms this way, by implementing the `post` function and using HTMX:

{< htmx:form >}
