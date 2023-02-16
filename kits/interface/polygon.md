:::{cpp:class} BPolygon
:::

# BPolygon

## Constructor and Destructor

::::{abi-group}
:::{cpp:function} BPolygon::BPolygon(const BPoint* pointList, int32 numPoints)
:::

:::{cpp:function} BPolygon::BPolygon(const BPolygon* polygon)
:::

:::{cpp:function} BPolygon::BPolygon()
:::

Initializes the {hclass}`BPolygon` by copying {hparam}`numPoints` from
{hparam}`pointList`, or by copying the list of points from another polygon.
If one polygon is constructed from another, the original and the copy won't
share any data; independent memory is allocated for the copy to hold a
duplicate list of points.

If a {hclass}`BPolygon` is constructed without a point list, points must
be set with the {cpp:func}`AddPoints() <BPolygon::AddPoints>` function.
::::

::::{abi-group}
:::{cpp:function} virtual BPolygon::~BPolygon()
:::

Frees all the memory allocated to hold the list of points.
::::

## Member Functions

::::{abi-group}
:::{cpp:function} void BPolygon::AddPoints(const BPoint* pointList, int32 numPoints)
:::

Appends {hparam}`numPoints` from {hparam}`pointList` to the list of points
that already define the polygon.
::::

::::{abi-group}
:::{cpp:function} int32 BPolygon::CountPoints() const
:::

Returns the number of points that define the polygon.
::::

::::{abi-group}
:::{cpp:function} BRect BPolygon::Frame() const
:::

Returns the polygon's frame rectangle—the smallest rectangle that encloses
the entire polygon.
::::

::::{abi-group}
:::{cpp:function} void BPolygon::MapTo(BRect source, BRect destination)
:::

Modifies the polygon so that it fits the {hparam}`destination` rectangle
exactly as it originally fit the {hparam}`source` rectangle. Each vertex of
the polygon is modified so that it has the same proportional position
relative to the sides of the destination rectangle as it originally had to
the sides of the source rectangle.

The polygon doesn't have to be contained in either rectangle. However, to
modify a polygon so that it's exactly inscribed in the destination
rectangle, you should pass its frame rectangle as the source:

:::{code} cpp
BRect frame = myPolygon->Frame();
myPolygon->MapTo(frame, anotherRect);
:::
::::

::::{abi-group}
:::{cpp:function} void BPolygon::PrintToStream() const
:::

Prints the {hclass}`BPolygon`'s point list to the standard output stream
(stdout). The {cpp:class}`BPoint` version of this function is called to
report each point as a string in the form

:::{code} sh
"BPoint(x, y)"
:::

where x and y stand for the coordinate values of the point in question.

See also: {cpp:func}`BPoint::PrintToStream`
::::

## Operators

::::{abi-group}
:::{cpp:function} BPolygon& operator =(const BPolygon& )
:::

Copies the point list of one {hclass}`BPolygon` object and assigns it to
another {hclass}`BPolygon`. After the assignment, the two objects describe
the same polygon, but are independent of each other. Destroying one of the
objects won't affect the other.
::::
