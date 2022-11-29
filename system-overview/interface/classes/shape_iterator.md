# BShapeIterator

Applications can create classes derived from {cpp:class}`BShapeIterator` to iterate over the
components of a {cpp:class}`BShape` object. There are four virtual functions that the application
must implement to process the four graphics commands described in the {cpp:class}`BShape`
documentation: {cpp:func}`~BShape::MoveTo()`, {cpp:func}`~BShape::LineTo()`,
{cpp:func}`~BShape::BezierTo()`, and {cpp:func}`~BShape::Close()`.

These functions can be implemented to do anything they like with the commands (rendering them to the
screen comes to mind as one possibility).
