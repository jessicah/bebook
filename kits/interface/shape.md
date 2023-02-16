:::{cpp:class} BShape
:::

# BShape

## Constructor and Destructor

::::{abi-group}
:::{cpp:function} BShape::BShape()
:::

:::{cpp:function} BShape::BShape(const BShape& copyFrom)
:::

:::{cpp:function} BShape::BShape(BMessage* archive)
:::

Creates a new {hclass}`BShape` object. The first form of the
{hclass}`BShape` constructor creates an empty shape. The second form, which
accepts another {hclass}`BShape` as an argument, copies that shape into the
new one. The third form reconstructs a {hclass}`BShape` from an archive.
::::

::::{abi-group}
:::{cpp:function} virtual BShape::~BShape()
:::

Releases memory occupied by the {hclass}`BShape` object.
::::

## Member Functions

::::{abi-group}
:::{cpp:function} status_t BShape::AddShape(const BShape* otherShape)
:::

{hmethod}`AddShape()` adds the lines and curves that comprise the
{hparam}`otherShape` to the shape.

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
:::{cpp:function} virtual BShape::Archive(BMessage* archive, bool deep = true) const
:::

Stores the {hclass}`BShape` in the {cpp:class}`BMessage` archive.

See also: {cpp:func}`BArchivable::Archive`, {cpp:func}`Instantiate()
<BShape::Instantiate>` static function
::::

::::{abi-group}
:::{cpp:function} status_t BShape::BezierTo(BPoint controlPoints[3])
:::

Adds a command to the {hclass}`BShape` that represents a Beziér curve that
begins at the current coordinates and is constructed using the specified
control points.

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
:::{cpp:function} BRect BShape::Bounds() const
:::

{hmethod}`Bounds()` returns the bounds rectangle of the entire shape; this
rectangle encloses all the lines and Beziér curves that comprise the shape.
::::

::::{abi-group}
:::{cpp:function} void BShape::Clear()
:::

{hmethod}`Clear()` deletes all the lines and Beziér curves that comprise
the shape, leaving it empty.
::::

::::{abi-group}
:::{cpp:function} void BShape::Close()
:::

{hmethod}`Close()` should be called when the shape has been
fully-constructed by calls to the {cpp:func}`BezierTo()
<BShape::BezierTo>`, {cpp:func}`LineTo() <BShape::LineTo>`, and
{cpp:func}`MoveTo() <BShape::MoveTo>` functions.

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
:::{cpp:function} status_t BShape::LineTo(BPoint point)
:::

Adds a "draw line" command to the {hclass}`BShape`. A line will be drawn
from the previous coordinates to the specified coordinates.

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
:::{cpp:function} status_t BShape::MoveTo(BPoint point)
:::

Adds a "move to" command to the {hclass}`BShape`. The next
{cpp:func}`LineTo() <BShape::LineTo>` or {cpp:func}`BezierTo()
<BShape::BezierTo>` will begin at this point. This lets you create
noncontiguous shapes.

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

## Static Functions

::::{abi-group}
:::{cpp:function} static BArchivable* BShape::Instantiate(BMessage* archive)
:::

Returns a new {hclass}`BShape` object, allocated by new and created with
the version of the constructor that takes a {cpp:class}`BMessage` archive.
However, if the archive message doesn't contain data for a {hclass}`BShape`
object, the return value will be {cpp:expr}`NULL`.

{cpp:func}`BArchivable::Instantiate`, {cpp:func}`instantiate_object()
<instantiate::object>`, {cpp:func}`Archive() <BShape::Archive>`
::::

## Archived Fields

The {cpp:func}`Archive() <BShape::Archive>` function adds the following
fields to its {cpp:class}`BMessage` argument:

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-
	- Field

	- Type code

	- Description

-
	- {hparam}`pts`

	- {cpp:enumerator}`B_POINT_TYPE`

	- The list of points used by the shape's commands.

-
	- {hparam}`ops`

	- {cpp:enumerator}`B_INT32_TYPE`

	- The list of command opcodes indicating the shape's commands.


:::
