:::{cpp:class} BStatusBar
:::

# BStatusBar

## Constructor and Destructor

::::{abi-group}
:::{cpp:function} BStatusBar::BStatusBar(BRect frame, const char* name, const char* label = NULL, const char* trailingLabel = NULL)
:::

:::{cpp:function} BStatusBar::BStatusBar(BMessage* archive)
:::

Initializes the {hclass}`BStatusBar` with a {hparam}`label` and a
{hparam}`trailingLabel`, which can both be {cpp:expr}`NULL`. The
{hparam}`frame` rectangle is used for its origin and width only; when the
{hclass}`BStatusBar` is attached to a window, it will be resized to a
height that precisely accommodates its parts. The {hparam}`name` argument
is passed on to the {cpp:class}`BView` constructor.

The object is given a {cpp:enumerator}`B_WILL_DRAW` flag and a resizing
mode that keeps it glued to the left and top sides of its parent.

The default font of the {hclass}`BStatusBar` is the system plain font, and
the default color of the bar is blue (50, 150, 255). It's initial value is
0.0, the minimum, and its default maximum value is 100.0.

See also: {cpp:func}`SetMaxValue() <BStatusBar::SetMaxValue>`,
{cpp:func}`SetBarColor() <BStatusBar::SetBarColor>`
::::

::::{abi-group}
:::{cpp:function} virtual BStatusBar::~BStatusBar()
:::

Frees the labels and the text.
::::

## Hook Functions

::::{abi-group}
:::{cpp:function} virtual void BStatusBar::AttachedToWindow()
:::

Resizes the frame rectangle to accommodate the object's graphical parts.
The width isn't altered.

This function also sets the view and low colors of the
{hclass}`BStatusBar` to match the background view color of its new parent.
::::

::::{abi-group}
:::{cpp:function} virtual void BStatusBar::Draw(BRect updateRect)
:::

Draws the bar, labels, and text.
::::

::::{abi-group}
:::{cpp:function} virtual void BStatusBar::MessageReceived(BMessage* message)
:::

Responds to {cpp:enumerator}`B_UPDATE_STATUS_BAR` and
{cpp:enumerator}`B_RESET_STATUS_BAR` messages by calling the
{cpp:func}`Update() <BStatusBar::Update>` and {cpp:func}`Reset()
<BStatusBar::Reset>` functions. Each message contains data that can be
passed as arguments to the functions.

See also: {cpp:func}`BView::MessageReceived`, "BStatusBar Messages" in the
Message Protocols appendix
::::

## Member Functions

::::{abi-group}
:::{cpp:function} virtual status_t BStatusBar::Archive(BMessage* archive, bool deep = true) const
:::

Calls the inherited version of {hmethod}`Archive()`, then adds the bar
color, bar height, current value, and maximum value to the
{cpp:class}`BMessage` archive, along with the current text, trailing text,
label, and trailing label.
::::

::::{abi-group}
:::{cpp:function} const char* BStatusBar::Label() const
:::

:::{cpp:function} const char* BStatusBar::TrailingLabel() const
:::

These functions return pointers to the object's label and trailing label.
The returned strings belong to the {hclass}`BStatusBar` object and should
not be altered. They can be set only on construction or when all values are
reset.

See also: {cpp:func}`Reset() <BStatusBar::Reset>`
::::

::::{abi-group}
:::{cpp:function} virtual void BStatusBar::Reset(const char* label = NULL, const char* trailingLabel = NULL)
:::

Empties the status bar, sets its current value to 0.0 and its maximum
value to 100.0, deletes and erases the text and trailing text, and replaces
the label and trailing label with copies of the strings passed as
arguments. If either argument is {cpp:expr}`NULL`, the label or trailing
label will also be deleted and erased.

This gets the {hclass}`BStatusBar` ready to be reused for another
operation. For example, if several large files are being downloaded, the
{hclass}`BStatusBar` could be reset for each one.

See also: {cpp:func}`SetText() <BStatusBar::SetText>`, {cpp:func}`Update()
<BStatusBar::Update>`, the {cpp:enumerator}`B_RESET_STATUS_BAR` message
constant.
::::

::::{abi-group}
:::{cpp:function} virtual void BStatusBar::SetBarColor(rgb_color color)
:::

:::{cpp:function} rgb_color BStatusBar::BarColor() const
:::

These functions set and return the color that fills the bar to show how
much of an operation has been completed. The default bar color is blue (50,
150, 255).
::::

::::{abi-group}
:::{cpp:function} virtual void BStatusBar::SetBarHeight(float height)
:::

:::{cpp:function} float BStatusBar::BarHeight() const
:::

These functions set and return the height of the bar itself, minus the
text and labels. The default height is 16.0 coordinate units. The frame
rectangle is adjusted to accommodate the new height, and the object is
redrawn.
::::

::::{abi-group}
:::{cpp:function} virtual void BStatusBar::SetMaxValue(float max)
:::

:::{cpp:function} float BStatusBar::MaxValue() const
:::

:::{cpp:function} float BStatusBar::CurrentValue() const
:::

{hmethod}`SetMaxValue()` sets the maximum value of the
{hclass}`BStatusBar`, which by default is 100.0. {hmethod}`MaxValue()`
returns the current maximum. The minimum value is 0.0 and cannot be
changed.

{hmethod}`CurrentValue()` returns the current value of the
{hclass}`BStatusBar`. The current value is set by {cpp:func}`Update()
<BStatusBar::Update>` and reset to 0.0 by {cpp:func}`Reset()
<BStatusBar::Reset>`.

The amount of "filling" in the status bar reflects the ratio
{hmethod}`CurrentValue()`/{hmethod}`MaxValue()`.
::::

::::{abi-group}
:::{cpp:function} virtual void BStatusBar::SetText(const char* string)
:::

:::{cpp:function} virtual void BStatusBar::SetTrailingText(const char* string)
:::

:::{cpp:function} const char* BStatusBar::Text() const
:::

:::{cpp:function} const char* BStatusBar::TrailingText() const
:::

These {hmethod}`SetText()` and {hmethod}`SetTrailingText()` functions
erase the previous text or trailing text and replace them with copies of
the string argument. string can be {cpp:expr}`NULL`. The view is
automatically redrawn.

{hmethod}`Text()` and {hmethod}`TrailingText()` return pointers to the
current text strings.
::::

::::{abi-group}
:::{cpp:function} virtual void BStatusBar::Update(float delta, const char* text = NULL, const char* trailingText = NULL)
:::

{hmethod}`Update()` updates the {hclass}`BStatusBar` by adding delta to
its current value and resetting its text and trailing text. Passing
{cpp:expr}`NULL` for the {hparam}`text` or {hparam}`trailingText` argument
retains the existing string(s). The status bar is automatically redrawn.

See also: {cpp:func}`Reset() <BStatusBar::Reset>`, the
{cpp:enumerator}`B_UPDATE_STATUS_BAR` message constant.
::::

## Static Functions

::::{abi-group}
:::{cpp:function} static BArchivable* BStatusBar::Instantiate(BMessage* archive)
:::

Returns a new {hclass}`BStatusBar` object, allocated by new and created
with the version of the constructor that takes a {cpp:class}`BMessage`
archive. However, if the archive doesn't contain data for an
{hclass}`BStatusBar` object, this function returns {cpp:expr}`NULL`.

See also {cpp:func}`BArchivable::Instantiate`,
{cpp:func}`instantiate_object() <instantiate::object>`,
{cpp:func}`Archive() <BStatusBar::Archive>`
::::

## Archived Fields

The {cpp:func}`Archive() <BStatusBar::Archive>` function adds the
following fields to its {cpp:class}`BMessage` argument:

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
	- {hparam}`_high`

	- {cpp:enumerator}`B_FLOAT_TYPE`

	- Status bar height.

-
	- {hparam}`_bcolor`

	- {cpp:enumerator}`B_INT32_TYPE`

	- Status bar color.

-
	- {hparam}`_val`

	- {cpp:enumerator}`B_FLOAT_TYPE`

	- Current value.

-
	- {hparam}`_max`

	- {cpp:enumerator}`B_FLOAT_TYPE`

	- Maximum value.

-
	- {hparam}`_text`

	- {cpp:enumerator}`B_STRING_TYPE`

	- Status bar text.

-
	- {hparam}`_ttext`

	- {cpp:enumerator}`B_STRING_TYPE`

	- Trailing text.

-
	- {hparam}`_label`

	- {cpp:enumerator}`B_STRING_TYPE`

	- Status bar label.

-
	- {hparam}`_tlabel`

	- {cpp:enumerator}`B_STRING_TYPE`

	- Trailing text label.


:::

Some of these fields may not be present if the setting they represent
isn't used, or is the default value. For example, if there is no trailing
text, the {hparam}`_ttext` field won't be found in the archive.
