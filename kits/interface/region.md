:::{cpp:class} BRegion
:::

# BRegion

## Constructor and Destructor

::::{abi-group}
:::{cpp:function} BRegion (const BRegion& region)
:::

:::{cpp:function} BRegion (const BRect& rect)
:::

:::{cpp:function} BRegion ()
:::

Initializes the {hclass}`BRegion` object to be a copy of {hparam}`region`,
or to be a rectangular region containing the space indicated by
{hparam}`rect`. If no argument is supplied, the {hclass}`BRegion` is empty
and {cpp:func}`Frame() <BRegion::Frame>` returns and invalid
{cpp:class}`BRect`.
::::

::::{abi-group}
:::{cpp:function} virtual BRegion::~BRegion()
:::

Frees the memory that was allocated to hold data describing the region.
::::

## Member Functions

::::{abi-group}
:::{cpp:function} bool BRegion::Contains(BPoint point) const
:::

Returns {cpp:expr}`true` if point lies within the region, and
{cpp:expr}`false` if not.
::::

::::{abi-group}
:::{cpp:function} BRect BRegion::Frame() const
:::

Returns the smallest rectangle that encloses all the rectangles in the
region.

If the region is empty, the returned object will be invalid. Check the
return thus:

:::{code} cpp
rect = region.Frame();
if (rect.IsValid())
   /* okay */
else
   /* nope */
:::
::::

::::{abi-group}
:::{cpp:function} bool BRegion::Intersects(BRect rect) const
:::

Returns {cpp:expr}`true` if the {hclass}`BRegion` has any area in common
with {hparam}`rect`, and {cpp:expr}`false` if not.
::::

::::{abi-group}
:::{cpp:function} void BRegion::MakeEmpty()
:::

Empties the {hclass}`BRegion` and invalidates the object's
{cpp:func}`Frame() <BRegion::Frame>` rectangle.
::::

::::{abi-group}
:::{cpp:function} void BRegion::OffsetBy(int32 horizontal, int32 vertical)
:::

Offsets all rectangles in the region by {hparam}`horizontal` and
{hparam}`vertical` deltas.
::::

::::{abi-group}
:::{cpp:function} void BRegion::PrintToStream() const
:::

Prints (to standard out) each rectangle in the {hclass}`BRegion` in the
form:

:::{code} sh
"BRect(left, top, right, bottom)"
:::

The first string that's printed is the object's frame rectangle. Each
subsequent string describes a single rectangle in the {hclass}`BRegion`.
::::

::::{abi-group}
:::{cpp:function} BRect BRegion::RectAt(int32 index)
:::

:::{cpp:function} int32 BRegion::CountRects()
:::

{hmethod}`CountRects()` returns the total number of rectangles in the
{hclass}`BRegion`; {hmethod}`RectAt()` returns the rectangle at a
particular {hparam}`index`. The order of the rectangles is unimportant.
::::

::::{abi-group}
:::{cpp:function} void BRegion::Set(BRect rect)
:::

:::{cpp:function} void BRegion::Include(BRect rect)
:::

:::{cpp:function} void BRegion::Include(const BRegion* region)
:::

:::{cpp:function} void BRegion::Exclude(BRect rect)
:::

:::{cpp:function} void BRegion::Exclude(const BRegion* region)
:::

:::{cpp:function} void BRegion::IntersectWith(const BRegion* region)
:::

{hmethod}`Set()` modifies the {hclass}`BRegion` so that it only contains
{hparam}`rect`.

{hmethod}`Include()` modifies the region to include (copies of) the
rectangles contained in {hparam}`rect` or {hparam}`region`.

{hmethod}`Exclude()` modifies the region to exclude all rectangles
contained in {hparam}`rect` or {hparam}`region`..

{hmethod}`IntersectWith()` modifies the region so that it includes only
those areas that it has in common with another region.
::::

## Operators

::::{abi-group}
:::{cpp:function} BRegion& operator =(const BRegion& )
:::

Sets the left region to be an independent copy of the right region:

:::{code} cpp
BRegion left_region = right_region;
:::
::::
