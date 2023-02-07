# BSlider
## Constructor and Destructor
::::{abi-group}

:::{cpp:function} BSlider::BSlider(BRect frame, const char* name, const char* label, BMessage* message, int32 minValue, int32 maxValue, thumb_style thumbType = B_BLOCK_THUMB, int32 resizingMode = B_FOLLOW_LEFT | B_FOLLOW_TOP, int32 flags = B_FRAME_EVENTS | B_WILL_DRAW | B_NAVIGABLE)
:::
:::{cpp:function} BSlider::BSlider(BRect frame, const char* name, const char* label, BMessage* message, int32 minValue, int32 maxValue, orientation posture, thumb_style thumbType = B_BLOCK_THUMB, int32 resizingMode = B_FOLLOW_LEFT | B_FOLLOW_TOP, int32 flags = B_FRAME_EVENTS | B_WILL_DRAW | B_NAVIGABLE)
:::
:::{cpp:function} BSlider::BSlider(BMessage* archive)
:::

Initializes the {hclass}`BSlider` by passing the appropriate arguments to the
{cpp:class}`BControl` constructor.
{cpp:class}`BControl` initializes the slider's {hparam}`label` and assigns
it a model {hparam}`message` that identifies the action that should be carried out
when the slider is invoked.

The {hparam}`frame`, {hparam}`name`,
{hparam}`resizingMode`, and {hparam}`flags` arguments are the same as those
declared for the {cpp:class}`BView`
class and are passed up the inheritance hierarchy
to the {cpp:class}`BView` constructor without change.

The {hparam}`minValue` and {hparam}`maxValue` parameters define the minimum and maximum
values to which the slider can be set.

If you want to control whether the slider is horizontal or vertical, use
the second form of the constructor, and set the {hparam}`posture` argument to
either {cpp:enum}`B_HORIZONTAL` or {cpp:enum}`B_VERTICAL`. If you don't specify this argument,
the slider will be horizontal by default.

The {hparam}`thumbType` argument defines the look of the slider's thumb, and can be
either of the following values:

:::{list-table}
---
header-rows: 1
---
-
	- Constant
	- Description
-
	- {cpp:enum}`B_BLOCK_THUMB`
	- The thumb is a rectangular block.
-
	- {cpp:enum}`B_TRIANGLE_THUMB`
	- The thumb is a triangular pointer.
:::
::::

::::{abi-group}

:::{cpp:function} virtual BSlider::~BSlider()
:::

Frees memory allocated by the {hclass}`BSlider` object.

::::

## Hook Functions
::::{abi-group}

:::{cpp:function} virtual void BSlider::AttachedToWindow()
:::

Augments the {cpp:class}`BControl`
version of this function to set the background
color of the button so that it matches the background color of its
parent. This function also sets the start position of the slider and
allocates other memory needed for the slider to function.

See also:
{cpp:func}`BView::AttachedToWindow`,
{cpp:func}`BControl::AttachedToWindow`

::::

::::{abi-group}

:::{cpp:function} virtual void BSlider::Draw(BRect updateRect)
:::

Draws the slider by calling
{cpp:func}`~BSlider::DrawSlider`.

See also:
{cpp:func}`BView::Draw`

::::

::::{abi-group}

:::{cpp:function} virtual void BSlider::DrawBar()
:::
:::{cpp:function} virtual BRect BSlider::BarFrame() const
:::

{hmethod}`DrawBar()` draws the slider bar. The bar is the narrow region the thumb
slides through. The bar should be drawn into the offscreen view.

{hmethod}`BarFrame()` returns the frame rectangle that encloses the slider bar.

These functions can be augmented or replaced by your own versions to
alter the appearance of the slider bar.

See also:
{cpp:func}`~BSlider::OffscreenView`

::::

::::{abi-group}

:::{cpp:function} virtual void BSlider::DrawFocusMark()
:::

If the slider is in focus, draws a mark indicating that this is the case.

You can override this function to alter the appearance of the slider
control.

::::

::::{abi-group}

:::{cpp:function} virtual void BSlider::DrawHashMarks()
:::
:::{cpp:function} virtual BRect BSlider::HashMarksFrame() const
:::

{hmethod}`DrawHashMarks()` draws the hash marks.

{hmethod}`HashMarksFrame()` returns the frame rectangle that encloses the hash
marks. If the hash marks are set to {cpp:enum}`B_HASH_MARKS_TOP` or
{cpp:enum}`B_HASH_MARKS_BOTTOM`, the rectangle encloses only the area needed to draw
the marks. If the setting is {cpp:enum}`B_HASH_MARKS_BOTH`, the hash marks frame
rectangle is the bounds rectangle of the entire slider control.

These functions can be augmented or replaced by your own versions to
alter the appearance of the hash marks.

::::

::::{abi-group}

:::{cpp:function} virtual void BSlider::DrawSlider()
:::

Draws the entire slider control by calling the functions responsible for
drawing the various parts of the control:

- {cpp:func}`~BSlider::DrawBar`
- {cpp:func}`~BSlider::DrawHashMarks`
- {cpp:func}`~BSlider::DrawThumb`
- {cpp:func}`~BSlider::DrawFocusMark`
- {cpp:func}`~BSlider::DrawText`

Once the slider has been drawn into the offscreen view, it's copied to
its parent window.

::::

::::{abi-group}

:::{cpp:function} virtual void BSlider::DrawText()
:::

Draws the slider's text areas. These are the minimum label, maximum
label, and status message.

The minimum and maximum labels can be set using the
{cpp:func}`~BSlider::SetLimitLabels`
function. The status message is obtained by calling the
{cpp:func}`~BSlider::UpdateText`
function. If you want there to be a status message, simply override
{cpp:func}`~BSlider::UpdateText`
to return the string you want drawn as the status message.

:::{admonition} Note
:class: note
In the default implementation of this function, the limit labels are
only drawn if both of them have been configured to a value other than
{cpp:enum}`NULL`. If either of them is {cpp:enum}`NULL`,
neither will be drawn.
:::

This function can be augmented or replaced by your own version to alter
the appearance or placement of the text.

::::

::::{abi-group}

:::{cpp:function} virtual void BSlider::DrawThumb()
:::
:::{cpp:function} virtual BRect BSlider::ThumbFrame() const
:::

{hmethod}`DrawThumb()` draws the slider's thumb. If you choose to reimplement this
function, you should call
{cpp:func}`~BSlider::Style`
to determine whether to draw a block thumb or a triangle thumb.

{hmethod}`ThumbFrame()` returns the frame rectangle that encloses the thumb.

These functions can be augmented or replaced by your own versions to
alter the appearance of the thumb.

::::

::::{abi-group}

:::{cpp:function} virtual void BSlider::FrameResized(float* width, float* height)
:::

Augments the
{cpp:class}`BControl`
version of
{cpp:func}`~BView::FrameResized`
to adjust the offscreen view and bitmap used for rendering the slider.

::::

::::{abi-group}

:::{cpp:function} virtual void BSlider::GetPreferredSize(float* width, float* height)
:::
:::{cpp:function} virtual void BSlider::ResizeToPreferred()
:::

{hmethod}`GetPreferredSize()` calculates the width and height of the area needed to
render the complete slider control, given the current configuration of
the control's various settings.

The {hparam}`width` returned by this function is the width of the slider control.
The {hparam}`height` is calculated by taking the height of the slider bar itself,
adding two times the height of the hash marks, then adding room for the
status text (if there is any) and limit strings (if there are any).

Note that the height always includes room for hash marks both above and
below the slider, even if the slider has no hash marks or only one of the
two sets of marks.

{hmethod}`ResizeToPreferred()` resizes the slider control to be the preferred size.

You can override these functions to alter the preferred size of the
slider; this is particularly important if you override other functions to
change the appearance of the slider.

::::

::::{abi-group}

:::{cpp:function} virtual void BSlider::KeyDown(const char* bytes, int32 numBytes)
:::

Augments the inherited version of
{cpp:func}`~BControl::KeyDown` to let the up and right arrow
keys increment the value of the slider, and the down and left arrow keys
to decrement the value of the slider.

See also:
{cpp:func}`BControl::Invoke`,
{cpp:func}`BView::KeyDown`

::::

::::{abi-group}

:::{cpp:function} virtual void BSlider::MouseDown(BPoint point)
:::

Overrides the
{cpp:class}`BView` version of
{cpp:func}`~BView::MouseDown`
to track mouse the mouse when
the button is pressed. A single click causes the thumb to immediately
reposition itself to the clicked location, and a click and drag motion
causes the slider to follow the mouse cursor until the button is released.

If a modification message has been established, it is sent repeatedly
while the mouse button is down. This can be used, for example, to let the
changes to the value of the slider be instantly reflected in an onscreen
display. When the mouse button is released and the slider has been set to
its resting position, the slider's model message is sent.

See also:
{cpp:func}`BControl::Invoke`,
{cpp:func}`BInvoker::SetTarget`,
{cpp:func}`~BSlider::ModificationMessage`,
{cpp:func}`~BSlider::SetModificationMessage`

::::

## Member Functions
::::{abi-group}

:::{cpp:function} virtual status_t BSlider::Archive(BMessage* archive, bool deep = true) const
:::

Archives the {hclass}`BSlider` by recording its the fields shown
{cpp:func}`~BSlider::ArchivedFields` in the
{cpp:class}`BMessage` {hparam}`archive`.

See also:
{cpp:func}`BArchivable::Archive`,
{cpp:func}`~BSlider::Instantiate` static function

::::

::::{abi-group}

:::{cpp:function} BView* BSlider::OffscreenView(BView* view)
:::

Returns a pointer to the offscreen {cpp:class}`BView`
in which the slider is rendered
prior to being copied to the screen. Because the slider is a complex
graphical construct, it's rendered offscreen, then copied onto the
screen. This function is provided to make it possible to further
customize the appearance of a custom slider control.

::::

::::{abi-group}

:::{cpp:function} virtual void BSlider::SetBarColor(rgb_color bar_color)
:::
:::{cpp:function} virtual rgb_color BSlider::BarColor() const
:::

{hmethod}`SetBarColor()` sets the color of the slider bar.

{hmethod}`BarColor()` returns the slider bar's color.

::::

::::{abi-group}

:::{cpp:function} virtual void BSlider::SetBarThickness(float thickness)
:::
:::{cpp:function} float BSlider::BarThickness() const
:::

{hmethod}`SetBarThickness()` sets the slider bar's thickness and
{hmethod}`BarThickness()`
returns the current thickness.

The slider bar's thickness determines how many pixels across the slider
bar is. If no thickness is defined, the bar occupies the entire unused
width or height of the slider's bounding rectangle.

::::

::::{abi-group}

:::{cpp:function} virtual void BSlider::SetFont(const BFont* font, uint32 properties = B_FONT_ALL)
:::

Sets the {hparam}`font` used for the slider's labels to font. The {hparam}`properties` flags
indicate which properties of the font should be used, and which should
remain unchanged.

::::

::::{abi-group}

:::{cpp:function} virtual void BSlider::SetHashMarks(hash_mark_location where)
:::
:::{cpp:function} hash_mark_location BSlider::HashMarks() const
:::

{hmethod}`SetHashMarks()` sets the placement of the hash marks. This value can be
one of the following:

:::{list-table}
---
header-rows: 1
---
-
	- Constant
	- Description
-
	- {cpp:enum}`B_HASH_MARKS_NONE`
	- The slider should have no hash marks.
-
	- {cpp:enum}`B_HASH_MARKS_TOP`
	- The slider should have hash marks above the slider bar. For horizontal sliders only.
-
	- {cpp:enum}`B_HASH_MARKS_BOTTOM`
	- The slider should have hash marks below the slider bar. For horizontal sliders only.
-
	- {cpp:enum}`B_HASH_MARKS_BOTH`
	- The slider should have hash marks above and below the slider bar.
-
	- {cpp:enum}`B_HASH_MARKS_LEFT`
	- The slider should have has marks to the left of the slider bar. For vertical sliders only.
-
	- {cpp:enum}`B_HASH_MARKS_RIGHT`
	- The slider should have has marks to the right of the slider bar. For vertical sliders only.
:::

{hmethod}`HashMarks()` returns the current placement of the hash marks.

::::

::::{abi-group}

:::{cpp:function} virtual void BSlider::SetHashMarkCount(int32 hash_mark_count)
:::
:::{cpp:function} int32 BSlider::HashMarkCount() const
:::

{hmethod}`SetHashMarkCount()` sets the number of hash marks that will be displayed
above and/or below the slider.

{hmethod}`HashMarkCount()` returns the number of hash marks currently set up.

::::

::::{abi-group}

:::{cpp:function} virtual void BSlider::SetKeyIncrementValue(int32 increment_value)
:::
:::{cpp:function} int32 BSlider::KeyIncrementValue() const
:::

{hmethod}`SetKeyIncrementValue()` sets the amount by which the slider's value
changes when the keyboard is used to move the thumb.

{hmethod}`KeyIncrementValue()` returns the amount by which the slider's value
changes when the keyboard is used to move the thumb.

::::

::::{abi-group}

:::{cpp:function} virtual void BSlider::SetLimitLabels(const char* minLabel, const char* maxLabel)
:::
:::{cpp:function} const char* BSlider::MinLimitLabel() const
:::
:::{cpp:function} const char* BSlider::MaxLimitLabel() const
:::

{hmethod}`SetLimitLabels()` sets the labels used to mark the minimum and maximum
values on the slider.

{hmethod}`MinLimitLabel()` and
{hmethod}`MaxLimitLabel()` return the current strings used to
mark the minimum and maximum values on the slider.

::::

::::{abi-group}

:::{cpp:function} virtual void BSlider::SetModificationMessage(BMessage* message)
:::
:::{cpp:function} BMessage* BSlider::ModificationMessage() const
:::

{hmethod}`SetModificationMessage()` sets the model message that's sent while the
mouse is being tracked. The modification message is sent repeatedly as
long as the mouse button is held down after being initially clicked
inside the slider.

{hmethod}`ModificationMessage()` returns the modification message currently set up.

See also:
{cpp:func}`~BSlider::MouseDown`

::::

::::{abi-group}

:::{cpp:function} virtual void BSlider::SetOrientation(orientation posture)
:::
:::{cpp:function} orientation BSlider::Orientation() const
:::

{hmethod}`SetOrientation()` sets the slider's orientation and {hmethod}`Orientation()` returns
its current orientation. The possible values are {cpp:enum}`B_HORIZONTAL` and
{cpp:enum}`B_VERTICAL`.

::::

::::{abi-group}

:::{cpp:function} virtual void BSlider::SetPosition(float* position)
:::
:::{cpp:function} virtual float BSlider::Position() const
:::

{hmethod}`SetPosition()` sets the value of the slider given a value between 0.0 and
1.0, where 0.0 is the minimum value of the slider, and 1.0 is the maximum
value. This lets you set the slider to a relative position without having
to look up the maximum and minimum values of the slider.

{hmethod}`Position()` returns the slider value scaled to the range 0.0 to 1.0.

::::

::::{abi-group}

:::{cpp:function} virtual void BSlider::SetSnoozeAmount(int32 snooze_time)
:::
:::{cpp:function} int32 BSlider::SnoozeAmount() const
:::

{hmethod}`SetSnoozeAmount()` sets the time (in microseconds) that the slider snoozes
for between updates while the mouse is being tracked.

{hmethod}`SnoozeAmount()` returns the time that the slider snoozes while the mouse
is being tracked.

::::

::::{abi-group}

:::{cpp:function} virtual void BSlider::SetStyle(thumb_style style)
:::
:::{cpp:function} thumb_style BSlider::Style() const
:::

{hmethod}`SetStyle()` sets the thumb style for the slider. The style can be either
of the following two values:

:::{list-table}
---
header-rows: 1
---
-
	- Constant
	- Description
-
	- {cpp:enum}`B_BLOCK_THUMB`
	- The thumb is a rectangular block.
-
	- {cpp:enum}`B_TRIANGLE_THUMB`
	- The thumb is a triangular pointer.
:::

{hmethod}`Style()` returns the current thumb style.

::::

::::{abi-group}

:::{cpp:function} virtual void BSlider::SetValue(int32* value)
:::
:::{cpp:function} virtual int32 BSlider::Value() const
:::
:::{cpp:function} virtual int32 BSlider::ValueForPoint(BPoint location) const
:::

{hmethod}`SetValue()` augments the
{cpp:class}`BControl`
{cpp:func}`~BControl::SetValue`
to pin the value to the maximum
and minimum values for the slider and the position of the thumb before
calling the inherited function.

{hmethod}`ValueForPoint()` returns the slider value represented by the given screen
coordinates.

::::

::::{abi-group}

:::{cpp:function} virtual char* BSlider::UpdateText() const
:::

Returns the status message that should be displayed with the slider. By
default, this function returns {cpp:enum}`NULL`; if you want a status message to be
displayed, simply override this function to return the appropriate string.

The pointer you return is yours; the
{cpp:func}`~BSlider::DrawText` routine won't dispose of
it unless you augment it to do so.

::::

::::{abi-group}

:::{cpp:function} virtual void BSlider::UseFillColor(bool use_fill, const rgb_color* bar_color = NULL)
:::
:::{cpp:function} virtual bool BSlider::FillColor(rgb_color* bar_color) const
:::

{hmethod}`UseFillColor()` sets the color used to fill the area of the slider bar
that's "filled." That is, the part of the bar between the minimum value
of the slider and the current thumb position. If the {hparam}`use_fill` parameter
is {cpp:enum}`true`, filling this area of the slider with the fill color is turned
on. If {hparam}`use_fill` is {cpp:enum}`false`, the entire slider bar is always drawn in the
bar color.

{hmethod}`FillColor()` stores the current fill color in {hparam}`bar_color`. The boolean value
returned by the function is {cpp:enum}`true` if the fill color is being used, {cpp:enum}`false`
if not.

::::

## Static Functions
::::{abi-group}

:::{cpp:function} static BArchivable* BSlider::Instantiate(BMessage* archive)
:::

Returns a new {hclass}`BSlider` object, allocated by new and created with the
version of the constructor that takes a {cpp:class}`BMessage` archive. However, if the
archive doesn't contain data for a {hclass}`BSlider` object, {hmethod}`Instantiate()` returns
{cpp:enum}`NULL`.

See also:
{cpp:func}`BArchivable::Instantiate`,
{cpp:func}`~instantiate::object`,
{cpp:func}`~BControl::Archive`

::::

## Archived Fields