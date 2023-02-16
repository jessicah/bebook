# BShape

The {cpp:class}`BShape` class provides a powerful means of representing
the outline of any shape that can be comprised of lines or Beziér curves.

The {cpp:class}`BShapeIterator` class provides a means for utilizing
{cpp:class}`BShape` objects in your own code. You can also use
{cpp:class}`BShape` objects to obtain outlines of characters in a
{cpp:class}`BFont` by calling {cpp:func}`BFont::GetGlyphShapes`.

## Creating a BShape

A {cpp:class}`BShape` is essentially a list of graphics commands, of which
there are four types:

-   MoveTo. This sets the BShape's coordinates to a specified point in the
shape's space.

-   LineTo. This represents a line from the current point to the next point in
the shape.

-   BeziérTo. This represents a Bezier curve, connecting the current point to
a new point, with other points serving to control the shape of the curve.

-   Close. This indicates the end of the shape's command list.

Functions by the same names are used to add the corresponding commands to
the BShape object. For example, to create a BShape that represents two
vertical lines, the following code might be used:

:::{code} cpp
BShape shape;
shape.MoveTo(0,0);
shape.LineTo(0,100);
shape.MoveTo(5,0);
shape.LineTo(5,100);
:::
