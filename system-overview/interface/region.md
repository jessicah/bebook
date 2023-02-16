# BRegion

A {cpp:class}`BRegion` object comprises a set of rectangles in a
two-dimensional coordinate system. The rectangles needn't overlap; a single
{cpp:class}`BRegion` can contain a little rectangle way down there, a big
one over yonder, and another that lives somewhere to the left of Baden
Baden.

You define and modify the contents of a region through to {cpp:func}`Set()
<BRegion::Set>`, {cpp:func}`Include() <BRegion::Include>`,
{cpp:func}`Exclude() <BRegion::Exclude>`, and {cpp:func}`IntersectWith()
<BRegion::IntersectWith>`. You can examine a region's rectangle's through
{cpp:func}`RectAt() <BRegion::RectAt>`, but note that the object coalesces
rectangles when it can, so the rectangles that you retrieve may not match
the ones that you passed in.

:::{admonition} Warning
:class: warning
The {cpp:class}`BRegion` class is designed to be used with coordinates
with integral values only; if any non-integral values are used in the
{cpp:class}`BRegion`, functions in the class may behave unpredictably.
:::

{cpp:class}`BRegion` objects can be allocated on the stack.
