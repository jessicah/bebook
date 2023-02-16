:::{cpp:class} BRect
:::

# BRect

## Data Members

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-
	- Member

	- Description

-
	- floatleft
	- The value of the rectangle's left side.
-
	- floattop
	- The value of the rectangle's top.
-
	- floatright
	- The value of the rectangle's right side.
-
	- floatbottom
	- The value of the rectangle's bottom.

:::

## Constructor and Destructor

::::{abi-group}
:::{cpp:function} inline BRect::BRect(float left, float top, float right, float bottom)
:::

:::{cpp:function} inline BRect::BRect(BPoint leftTop, BPoint rightBottom)
:::

:::{cpp:function} inline BRect::BRect(BRect& rect)
:::

:::{cpp:function} inline BRect::BRect()
:::

Initializes a {hclass}`BRect` as four sides, as two diametrically opposed
corners, or as a copy of some other {hclass}`BRect` object. A rectangle
that's not assigned any initial values is invalid, until a specific
assignment is made, either through a {cpp:func}`Set() <BRect::Set>`
function or by setting the object's data members directly.
::::

## Member Functions

::::{abi-group}
:::{cpp:function} bool BRect::Contains(BPoint point) const
:::

:::{cpp:function} bool BRect::Contains(BRect rect) const
:::

:::{cpp:function} bool BRect::Intersects(BRect rect) const
:::

{hmethod}`Contains()` returns {cpp:expr}`true` if {hparam}`point` or
{hparam}`rect` lies entirely within the {hclass}`BRect`'s rectangle (and
{cpp:expr}`false` if not). A rectangle contains the points that lie along
its edges; for example, two identical rectangles contain each other.

{hmethod}`Intersect()` returns {cpp:expr}`true` if the {hclass}`BRect` has
any area—even a corner or part of a side—in common with {hparam}`rect`, and
{cpp:expr}`false` if it doesn't.

:::{admonition} Note
:class: note
This function's results are unpredictable if either rectangle is invalid.
:::

See also: {cpp:func}`& (intersection)`, {cpp:func}`| (union)`,
{cpp:func}`BPoint::ConstrainTo`
::::

::::{abi-group}
:::{cpp:function} void BRect::InsetBy(float x, float y)
:::

:::{cpp:function} void BRect::InsetBy(BPoint point)
:::

:::{cpp:function} BRect& BRect::InsetBySelf(float x, float y)
:::

:::{cpp:function} BRect& BRect::InsetBySelf(BPoint point)
:::

:::{cpp:function} BRect BRect::InsetByCopy(float x, float y)
:::

:::{cpp:function} BRect BRect::InsetByCopy(BPoint point)
:::

:::{cpp:function} void BRect::OffsetBy(float x, float y)
:::

:::{cpp:function} void BRect::OffsetBy(BPoint point)
:::

:::{cpp:function} BRect& BRect::OffsetBySelf(float x, float y)
:::

:::{cpp:function} BRect& BRect::OffsetBySelf(BPoint point)
:::

:::{cpp:function} BRect BRect::OffsetByCopy(float x, float y)
:::

:::{cpp:function} BRect BRect::OffsetByCopy(BPoint point)
:::

:::{cpp:function} void BRect::OffsetTo(float x, float y)
:::

:::{cpp:function} void BRect::OffsetTo(BPoint point)
:::

:::{cpp:function} BRect& BRect::OffsetToSelf(float x, float y)
:::

:::{cpp:function} BRect& BRect::OffsetToSelf(BPoint point)
:::

:::{cpp:function} BRect BRect::OffsetToCopy(float x, float y)
:::

:::{cpp:function} BRect BRect::OffsetToCopy(BPoint point)
:::

Sorting out the different versions, there are three basic
rectangle-manipulation functions here:

-   {hmethod}`InsetBy()` insets the sides of the {hclass}`BRect`'s rectangle
by {hparam}`x` units (left and right sides) and {hparam}`y` units (top and
bottom). Positive inset values shrink the rectangle; negative values expand
it. Note that both sides of each pair moves the full amount. For example,
if you inset a {hclass}`BRect` by (4,4), the left side moves (to the right)
four units and the right side moves (to the left) four units (and similarly
with the top and bottom).

-   {hmethod}`OffsetBy()` moves the {hclass}`BRect` horizontally by
{hparam}`x` units and vertically by {hparam}`y` units. The rectangle's size
doesn't change.

-   {hmethod}`OffsetTo()` moves the {hclass}`BRect` to the location
({hparam}`x`,{hparam}`y`).

If a {cpp:class}`BPoint` argument is used, the {cpp:class}`BPoint`'s
{hparam}`x` and {hparam}`y` values are used as the {hparam}`x` and
{hparam}`y` arguments.

The {hmethod}`…Self()` versions of the functions are the same as the
simpler versions, but they conveniently return the modified
{hclass}`BRect`.

The {hmethod}`…Copy()` versions copy the {hclass}`BRect`, and then modify
and return the copy (without changing the original).
::::

::::{abi-group}
:::{cpp:function} inline bool BRect::IsValid() const
:::

Returns {cpp:expr}`true` if the {hclass}`BRect`'s right side is greater
than or equal to its left and its bottom is greater than or equal to its
top, and {cpp:expr}`false` otherwise. An invalid rectangle can't be used to
define an interface area (such as the frame of a view or window).
::::

::::{abi-group}
:::{cpp:function} void BRect::PrintToStream() const
:::

Prints the contents of the {hclass}`BRect` object to standard out in the
form:

:::{code} sh
"BRect(left, top, right, bottom)"
:::
::::

::::{abi-group}
:::{cpp:function} inline void BRect::Set(float left, float top, float right, float bottom)
:::

:::{cpp:function} void BRect::SetLeftTop(const BPoint point)
:::

:::{cpp:function} void BRect::SetLeftBottom(const BPoint point)
:::

:::{cpp:function} void BRect::SetRightTop(const BPoint point)
:::

:::{cpp:function} void BRect::SetRightBottom(const BPoint point)
:::

:::{cpp:function} BPoint BRect::LeftTop() const
:::

:::{cpp:function} BPoint BRect::LeftBottom() const
:::

:::{cpp:function} BPoint BRect::RightTop() const
:::

:::{cpp:function} BPoint BRect::RightBottom() const
:::

{hmethod}`Set()` sets the object's rectangle by defining the coordinates
of all four sides. The other {hmethod}`Set…()` functions move one of the
rectangle's corners to the {cpp:class}`BPoint` argument; the other corners
and sides are modified concomittantly. None of these functions prevents you
from creating an invalid rectangle.

The {cpp:class}`BPoint`-returning functions return the coordinates of one
of the rectangle's four corners.
::::

::::{abi-group}
:::{cpp:function} inline float BRect::Width() const
:::

:::{cpp:function} inline int32 BRect::IntegerWidth() const
:::

:::{cpp:function} inline float BRect::Height() const
:::

:::{cpp:function} inline int32 BRect::IntegerHeight() const
:::

{hmethod}`Width()` returns the numerical difference between the
rectangle's right and left sides (i.e. {hparam}`right` - {hparam}`left`).
{hmethod}`IntegerWidth()` does the same, but rounds up in the case of a
fractional difference.

{hmethod}`Height()` and {hmethod}`IntegerHeight()` perform similar
calculations for the height of the rectangle (i.e. {hparam}`bottom` -
{hparam}`top` and ceil({hparam}`bottom` - {hparam}`top`)).

The width and height of a {hclass}`BRect`'s rectangle, as returned through
these functions
::::

## Operators

::::{abi-group}
:::{cpp:function} inline BRect& operator =(const BRect from)
:::

Copies {hparam}`from`'s rectangle data into the left-side object.
::::

::::{abi-group}
:::{cpp:function} bool operator ==(BRect ) const
:::

:::{cpp:function} bool operator !=(BRect ) const
:::

{hmethod}`==` returns {cpp:expr}`true` if the two objects' rectangles
exactly coincide.

{hmethod}`!=` returns {cpp:expr}`true` if the two objects' rectangles
don't coincide.
::::

::::{abi-group}
:::{cpp:function} BRect operator &(BRect ) const
:::

Creates and returns a new {hclass}`BRect` that's the intersection of the
two operands. The new {hclass}`BRect` encloses the area that the two
operands have in common. If the two operands don't intersect, the new
{hclass}`BRect` will be invalid.
::::

::::{abi-group}
:::{cpp:function} BRect operator |(BRect ) const
:::

Creates and returns a new {hclass}`BRect` that minimally but completely
encloses the area defined by both of the operands. The shaded area
illustrates the union of the two outlined rectangles:

![Union Of Two Rectangles](./images/TheInterfaceKit/rect_union.png)
::::
