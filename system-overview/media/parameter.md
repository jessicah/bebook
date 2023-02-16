# BParameter

The {cpp:class}`BParameter` class is the superclass from which all
controls representing configurable parameters within a
{cpp:class}`BControllable` node are derived.

:::{admonition} Note
:class: note
The word "parameter," in terms of the Media Kit, refers to a point at
which the data manipulation performed by a {cpp:class}`BControllable` node
can be configured, and doesn't actually refer to a user interface object.
{cpp:class}`BParameter`-derived objects don't implement a user interface.
See the {cpp:class}`BMediaTheme` class for information on how to create a
user interface for a {cpp:class}`BControllable` node.
:::

The {cpp:class}`BParameter` class is an abstract class; you'll normally
use the {cpp:func}`MakeNullParameter()
<BParameterGroup::MakeNullParameter>`, {cpp:func}`MakeDiscreteParameter()
<BParameterGroup::MakeDiscreteParameter>`, and
{cpp:func}`MakeContinuousParameter()
<BParameterGroup::MakeContinuousParameter>` functions in the
{cpp:class}`BParameterGroup` class to actually create parameters and add
them to a {cpp:class}`BParameterWeb`. For more detailed information on
parameters and how to create a {cpp:class}`BParameterWeb`, see the
{cpp:class}`BParameterGroup` and {cpp:class}`BParameterWeb` classes.
