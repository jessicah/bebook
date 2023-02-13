# BParameterGroup

A {cpp:class}`BParameterGroup` object serves as a logical grouping of
{cpp:class}`BParameter`s. Each {cpp:class}`BParameter` belongs to exactly
one {cpp:class}`BParameterGroup`, and is in fact created by the
{cpp:class}`BParameterGroup` object to which it belongs, via the
{cpp:func}`BParameterWeb::MakeGroup` function.

{cpp:class}`BParameterGroup`s can be nested one inside another.

A {cpp:class}`BParameterGroup` object that's owned by a
{cpp:class}`BParameterWeb` is a logical candidate for a pane in a
multi-pane control panel such as a {cpp:class}`BTabView`, wherein each tab
causes another {cpp:class}`BParameterGroup`'s {cpp:class}`BParameter`s to
be displayed.
