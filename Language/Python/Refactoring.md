# Imports
```python
# Correct:
import os
import sys
```
```python
# Correct:
from subprocess import Popen, PIPE
```
```python
# Wrong:
import sys, os
```

# Indentation

```python
# Correct:

# Aligned with opening delimiter.
foo = long_function_name(var_one, var_two,
                         var_three, var_four)

# Add 4 spaces (an extra level of indentation) to distinguish arguments from the rest.
def long_function_name(
        var_one, var_two, var_three,
        var_four):
    print(var_one)

# Hanging indents should add a level.
foo = long_function_name(
    var_one, var_two,
    var_three, var_four)
# Wrong:

# Arguments on first line forbidden when not using vertical alignment.
foo = long_function_name(var_one, var_two,
    var_three, var_four)

# Further indentation required as indentation is not distinguishable.
def long_function_name(
    var_one, var_two, var_three,
    var_four):
    print(var_one)
```

# When to Use Trailing Commas
```python
# Correct:
FILES = ('setup.cfg',)
```
```python
# Wrong:
FILES = 'setup.cfg',
```

# Programming Recommendations
## Exceptions
```python
# Correct:
try:
    value = collection[key]
except KeyError:
    return key_not_found(key)
else:
    return handle_value(value)
```
```python
# Wrong:
try:
    # Too broad!
    return handle_value(collection[key])
except KeyError:
    # Will also catch KeyError raised by handle_value()
    return key_not_found(key)
```

## Connections
```python
# Correct:
with conn.begin_transaction():
    do_stuff_in_transaction(conn)
```
```python
# Wrong:
with conn:
    do_stuff_in_transaction(conn)
```
