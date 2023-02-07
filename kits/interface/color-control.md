# BColorControl
## Constructor and Destructor
::::{abi-group}

:::{cpp:function} BColorControl::BColorControl(BPoint leftTop, color_control_layout matrix, float cellSide, const char* name, BMessage* message = NULL, bool bufferedDrawing = false)
:::
:::{cpp:function} BColorControl::BColorControl(BMessage* archive = NULL)
:::

Initializes the {hclass}`BColorControl` so that the left top corner of its frame
rectangle will be located at the stated {hparam}`leftTop` point in the coordinate
system of its parent view. The frame rectangle will be large enough to
display 256 color cells arranged in the specified {hparam}`matrix`, which can be
any of the following {cpp:func}`~BColorControl::color` constants:

- {cpp:enum}`B_CELLS_4x64`
- {cpp:enum}`B_CELLS_8x32`
- {cpp:enum}`B_CELLS_16x16`
- {cpp:enum}`B_CELLS_64x4`
- {cpp:enum}`B_CELLS_32x8`

For example, {cpp:enum}`B_CELLS_4x64` lays out a matrix with four cell columns and 64
rows; {cpp:enum}`B_CELLS_32x8` specifies 32 columns and 8 rows. Each cell is a square
{hparam}`cellSide` coordinate units on a side; since the number of units translates
directly to screen pixels, {hparam}`cellSide` should be a whole number.

When the screen is 15, 16, or 32 bits deep, the same frame rectangle will
display four color ramps, one each for the red, green, and blue
components, plus a disabled ramp for the alpha component. You might
choose {hparam}`matrix` and {hparam}`cellSize`
values with a view toward how the resulting
bounds rectangle would be divided into four horizontal rows.

The {hparam}`name` argument assigns a name to the object as a
{cpp:class}`BHandler`.
It's the same as the argument declared by the
{cpp:class}`BView` constructor.

If a model {hparam}`message` is supplied, the
{hclass}`BColorControl` will announce every
change in color value by calling
{cpp:func}`~BControl::Invoke`
(defined in the {cpp:class}`BControl` class)
to post a copy of the message to a designated target.

If the {hparam}`bufferedDrawing` flag is {cpp:enum}`true`, all changes to the on-screen display
will first be made in an off-screen bitmap and then copied to the screen.
This makes the drawing smoother, but it requires more memory.

The initial value of the new object is 0, which when translated to an
rgb_color structure, means black.

See also:
{cpp:func}`BHandler::SetName`
::::

::::{abi-group}

:::{cpp:function} virtual BColorControl::~BColorControl()
:::

Gets rid of the off-screen bitmap, if one was requested when the object
was constructed.

::::

## Hook Functions
::::{abi-group}

:::{cpp:function} virtual void BColorControl::AttachedToWindow()
:::

Augments the {cpp:class}`BControl`
{cpp:func}`~BControl::AttachedToWindow`
of this function to set the {hclass}`BColorControl`'s
view color and low color to be the same as its parent's view color and to
set up the {cpp:class}`BTextControl`
objects where the user can type red, green, and
blue color values. If the object uses buffered drawing, this function
makes sure the offscreen images are displayed on-screen.

See also:
{cpp:func}`BView::SetViewColor`

::::

::::{abi-group}

:::{cpp:function} virtual void BColorControl::Draw(BRect updateRect)
:::

Overrides the {cpp:class}`BView`
{cpp:func}`~BView::Draw`
of this function to draw the color control.
::::

::::{abi-group}

:::{cpp:function} virtual void BColorControl::GetPreferredSize(float* width, float* height)
:::

Calculates how large the color control needs to be given its layout, cell
size, and current font; the results are reported in the variables that
the {hparam}`width` and {hparam}`height` arguments refer to.

See also: {cpp:func}`BView::GetPreferredSize`

::::

::::{abi-group}

:::{cpp:function} virtual void BColorControl::KeyDown(const char* bytes, int32 numBytes)
:::

Augments the {cpp:class}`BControl`
version of {cpp:func}`~BControl::KeyDown`
to allow the user to navigate within the color control using the arrow keys.

::::

::::{abi-group}

:::{cpp:function} virtual void BColorControl::MessageReceived(BMessage message)
:::

Responds to internal messages that change the color.

See also: {cpp:func}`BHandler::MessageReceived`

::::

::::{abi-group}

:::{cpp:function} virtual void BColorControl::MouseDown(BPoint point)
:::

Overrides the {cpp:class}`BView` version of
{cpp:func}`~BView::MouseDown`
to allow the user to operate the color control with the mouse.

::::

## Member Functions
::::{abi-group}

:::{cpp:function} virtual status_t BColorControl::Archive(BMessage* archive, bool deep = true) const
:::

Calls the inherited version of
{cpp:func}`~BControl::Archive`
, then adds the layout, cell
size, and whether the object uses buffered drawing to the
{cpp:class}`BMessage`
archive.

See also:
{cpp:func}`BArchivable::Archive`,
{cpp:func}`~BColorControl::Instantiate` static function

::::

::::{abi-group}

:::{cpp:function} virtual void BColorControl::SetCellSize(float cellSide)
:::
:::{cpp:function} float BColorControl::CellSize() const
:::

These functions set and return the size of a single cell in the
{hclass}`BColorControl`'s matrix of 256 colors. A cell is a square {hparam}`cellSide`
coordinate units on a side. The size is first set by the {hclass}`BColorControl`
{cpp:func}`~BColorControl::Constructor`.

::::

::::{abi-group}

:::{cpp:function} virtual void BColorControl::SetEnabled(bool enabled)
:::

Auguments the {cpp:class}`BControl` version of
{cpp:func}`~BControl::SetEnabled` to disable and re-enable
the text fields for setting the color components as the {hclass}`BColorControl` is
disabled and re-enabled. The inherited
{cpp:func}`~BControl::IsEnabled` function doesn't need
augmenting and therefore isn't reimplemented.

::::

::::{abi-group}

:::{cpp:function} virtual void BColorControl::SetLayout(color_control_layout layout)
:::
:::{cpp:function} color_control_layout BColorControl::Layout() const
:::

These functions set and return the layout of the matrix of 256 color
cells. The matrix is first arranged by the constructor. See the
{cpp:func}`~BColorControl::Constructor` for permissible layout values.

::::

::::{abi-group}

:::{cpp:function} virtual void BColorControl::SetValue(int32 color)
:::
:::{cpp:function} inline void BColorControl::SetValue(rgb_color color)
:::
:::{cpp:function} rgb_color BColorControl::ValueAsColor()
:::

These functions set and return the {hclass}`BColorControl`'s current
value—the last color that the user selected.

The `virtual` version of {hmethod}`SetValue()` takes an int32 argument and is
essentially the same as the {cpp:class}`BControl` version of the function, which it
modifies only to take care of class-internal housekeeping details. The
`inline` version, on the other hand, takes an rgb_color argument and is
unique to this class. It packs color information from the structure into
a 32-bit integer and passes it to the `virtual` version of the function.
Like all other objects that derive from {cpp:class}`BControl`, a {hclass}`BColorControl` stores
its current value as an int32; no information is lost in the translation
from an rgb_color structure to an integer.

{hmethod}`SetValue()` is called to make every change to the {cpp:class}`BControl`'s value. If you
override this function to be notified of the changes, you should override
the virtual version. (However, due to the peculiarities of C++,
overriding any version of an overloaded function hides all versions of
the function. For continued access to the rgb_color version of {hmethod}`SetValue()`
without explicitly specifying the "{hclass}`BColorControl`::" prefix, copy the
inline code from interface/ColorControl.h to the derived class.)

{hmethod}`ValueAsColor()` is an alternative to the
{cpp:func}`~BControl::Value`
function inherited from
the {cpp:class}`BControl` class. It returns the object's current value as an
rgb_color; {hmethod}`Value()` returns it as an int32.

See also: {cpp:func}`BControl::SetValue`

::::

## Static Functions
::::{abi-group}

:::{cpp:function} static BArchivable* BColorControl::Instantiate(BMessage* archive = NULL)
:::

Returns a new {hclass}`BColorControl` object, allocated by new and created with the
version of the constructor that takes a
{cpp:class}`BMessage` archive. However, if the
archive doesn't contain data for a {hclass}`BColorControl` object, this function
returns {cpp:enum}`NULL`.

See also:
{cpp:func}`BArchivable::Instantiate`,
{cpp:func}`~instantiate::object`,
{cpp:func}`~BColorControl::Archive`

::::

## Defined Types
::::{abi-group}

:::{code}
enum color_control_layout {}
:::

Determines the layout of the {hclass}`BColorControl`

::::

## Archived Fields