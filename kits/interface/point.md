# BPoint
## Data Members
::::{abi-group}

The coordinate value measured horizontally along the x-axis.

::::

::::{abi-group}

The coordinate value measured vertically along the y-axis.

::::

## Constructor and Destructor
::::{abi-group}

:::{cpp:function} inline BPoint::BPoint(float x, float y)
:::
:::{cpp:function} inline BPoint::BPoint(const BPoint& point)
:::
:::{cpp:function} inline BPoint::BPoint()
:::

Creates a new {hclass}`BPoint` object that corresponds to the
point ({hparam}`x`, {hparam}`y`), or
{hclass}`BPoint`
that's copied from point. If no coordinate values are assigned, the
{hclass}`BPoint`'s location is indeterminate.

See also:
{cpp:func}`~BPoint::Set`,
the assignment operator

::::

## Member Functions
::::{abi-group}

:::{cpp:function} void BPoint::ConstrainTo(BRect rect)
:::

Ensures that the {hclass}`BPoint` lies within {hparam}`rect`.
If it's already contained in
the rectangle, the {hclass}`BPoint` is unchanged; otherwise, it's moved to the
{hparam}`rect`'s nearest edge.

See also:
{cpp:func}`BRect::Contains`

::::

::::{abi-group}

:::{cpp:function} void BPoint::PrintToStream() const
:::

Prints the {hclass}`BPoint`'s coordinates to standard output in the form:

:::{code}
"BPoint(x, y)"
:::
::::

::::{abi-group}

:::{cpp:function} inline void BPoint::Set(float x, float y)
:::

Sets the {hclass}`BPoint`'s x and y coordinates.

::::

## Operators
::::{abi-group}

:::{cpp:function} inline BPoint& operator =(const BPoint& from)
:::

Copies from's coordinate data into the left-side object.

::::

::::{abi-group}

:::{cpp:function} bool operator ==(BPoint) const
:::
:::{cpp:function} bool operator !=(BPoint) const
:::

{hmethod}`==` returns {cpp:enum}`true` if
the two objects' point exactly coincide.

{hmethod}`!=` returns {cpp:enum}`true` if
the two objects' points don't coincide.

::::

::::{abi-group}

:::{cpp:function} BPoint operator +(const BPoint& ) const
:::
:::{cpp:function} BPoint operator +=(const BPoint& ) const
:::

{hmethod}`+` creates and returns a new {hclass}`BPoint` that adds the two operands together.
The new object's x coordinate is the sum of the operands' x values; its y
value is the sum of the operands' y values.

{hmethod}`+=` adds the operands together and stores the result in the left operand.

::::

::::{abi-group}

:::{cpp:function} BPoint operator -(const BPoint& ) const
:::
:::{cpp:function} BPoint operator -=(const BPoint& ) const
:::

{hmethod}`-` creates and returns a new {hclass}`BPoint` that subtracts the right operand from
the left. The new object's x coordinate is the difference between the
operands' x values; its y value is the difference between the operands' y
values.

{hmethod}`-=` performs the subtraction and stores the result in the left operand.

::::

## Global Objects
::::{abi-group}

{hclass}`BPoint` object that represents (0.0, 0.0).

::::
