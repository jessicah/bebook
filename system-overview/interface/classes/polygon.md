# BPolygon

A {cpp:class}`BPolygon` object represents a polygon---a closed, many-sided figure that describes an
area within a two-dimensional coordiante system. It differs from a {cpp:class}`BRect` object in that
it can have any number of sides and the sides don't have to be aligned with the coordinate axes.

A {cpp:class}`BPolygon` is defined as a series of connected points. Each point is a potential vertex
in the polygon. An outline of the polygon could be constructed by tracing a straight line from the
first point to the second, from the second point to the third, and so on through the whole series,
then by connecting the first and last points if they're not identical.

The {cpp:class}`BView` functions that draw a polygon---{cpp:func}`~BView::StrokePolygon()` and
{cpp:func}`~BView::FillPolygon()`---take {cpp:class}`BPolygon` objects as arguments.
{cpp:func}`~BView::StrokePolygon()` offers the option of leaving the polygon open---of not stroking
the line that connects the first and last points in the list. The polygon therefore won't look like
a polygon, but like a chain of lines fastened at their endpoints.
