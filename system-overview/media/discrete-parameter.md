# BDiscreteParameter

The {cpp:class}`BDiscreteParameter` class represents a parameter that is
set to one of a discrete set of values, and is usually used for non-linear
values such as color spaces, multiplexers, and mutes or enables.

Each discrete value has a name that's displayed to the user by
applications that draw a user interface for the node.

The default system theme renders these as {cpp:class}`BCheckBox` controls,
{cpp:class}`BRadioButton` groups, or {cpp:class}`BMenuField` controls,
depending on the parameter kind. Other themes might implement these
differently.
