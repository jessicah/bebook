:::{cpp:class} BShapeIterator
:::

# BShapeIterator

## Constructor and Destructor

::::{abi-group}
:::{cpp:function} BShapeIterator::BShapeIterator()
:::

Constructor
::::

::::{abi-group}
:::{cpp:function} BShapeIterator::~BShapeIterator()
:::

Destructor
::::

## Member Functions

::::{abi-group}
:::{cpp:function} status_t BShapeIterator::Iterate(BShape* shape)
:::

{hmethod}`Iterate()` iterates over each command that comprises the shape,
in order, calling the {hmethod}`Iterate…()` function that corresponds to
each command.

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-
	- Return Code

	- Description

-
	- {cpp:enumerator}`B_OK`.
	- No error.
-
	- Other errors.
	- None are defined at this time, but you should always check for errors
		returned by this function.

:::
::::

::::{abi-group}
:::{cpp:function} virtual status_t BShapeIterator::IterateBezierTo(int32 bezierCount, BPoint* bezierPoints)
:::

:::{cpp:function} virtual status_t BShapeIterator::IterateClose()
:::

:::{cpp:function} virtual status_t BShapeIterator::IterateLineTo(int32 lineCount, BPoint* linePoints)
:::

:::{cpp:function} virtual status_t BShapeIterator::IterateMoveTo(BPoint* linePoints)
:::

These functions are called by {cpp:func}`Iterate()` to process the shape
commands. Your {hclass}`BShapeIterator`-derived class must implement these
four functions.
::::
