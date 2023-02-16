:::{cpp:class} BStringView
:::

# BStringView

## Constructor and Destructor

::::{abi-group}
:::{cpp:function} BStringView::BStringView(BRect frame, const char* name, const char* text, uint32 resizingMode = B_FOLLOW_LEFT | B_FOLLOW_TOP, uint32 flags = B_WILL_DRAW)
:::

:::{cpp:function} BStringView::BStringView(BMessage* archive)
:::

Initializes the {hclass}`BStringView` by assigning it a {hparam}`text`
string and the system plain font ({hparam}`be_plain_font`). The
{hparam}`frame`, {hparam}`name`, {hparam}`resizingMode`, and
{hparam}`flags` arguments are passed unchanged to the {cpp:class}`BView`
constructor.

The {hparam}`frame` rectangle needs to be large enough to display the
entire string in the current font. The string is drawn at the bottom of the
frame rectangle and, by default, is aligned to the left side. A different
horizontal alignment can be set by calling {cpp:func}`SetAlignment()
<BStringView::SetAlignment>`.
::::

::::{abi-group}
:::{cpp:function} virtual BStringView::~BStringView()
:::

Frees the text string.
::::

## Hook Functions

::::{abi-group}
:::{cpp:function} virtual void BStringView::AttachedToWindow()
:::

Sets the {hclass}`BStringView`'s low color and its background view color
to match the background color of its new parent view.

See also: {cpp:func}`BView::AttachedToWindow`
::::

::::{abi-group}
:::{cpp:function} virtual void BStringView::Draw(BRect updateRect)
:::

Draws the string along the bottom of the {hclass}`BStringView`'s frame
rectangle in the current high color.
::::

## Member Functions

::::{abi-group}
:::{cpp:function} virtual status_t BStringView::Archive(BMessage* archive, bool deep = true) const
:::

Calls the inherited version of {cpp:func}`Archive() <BView::Archive>`,
then adds the string and its alignment to the {cpp:class}`BMessage`
archive.
::::

::::{abi-group}
:::{cpp:function} void BStringView::SetAlignment(alignment flag)
:::

:::{cpp:function} alignment BStringView::Alignment() const
:::

These functions align the string within the {hclass}`BStringView`'s frame
rectangle and return the current alignment. The alignment flag can be:

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-
	- Constant

	- Description

-
	- {cpp:enumerator}`B_ALIGN_LEFT`
	- The string is aligned at the left side of the frame rectangle.
-
	- {cpp:enumerator}`B_ALIGN_RIGHT`
	- The string is aligned at the right side of the frame rectangle.
-
	- {cpp:enumerator}`B_ALIGN_CENTER`
	- The string is aligned so that the center of the string falls midway
		between the left and right sides of the frame rectangle.

:::

The default is {cpp:enumerator}`B_ALIGN_LEFT`.
::::

::::{abi-group}
:::{cpp:function} void BStringView::SetText(const char* string)
:::

:::{cpp:function} const char* BStringView::Text() const
:::

These functions set and return the text string that the
{hclass}`BStringView` draws. {hmethod}`SetText()` frees the previous string
and copies string to replace it. {hmethod}`Text()` returns the
null-terminated string.
::::

## Static Functions

### Instantiate()

See {cpp:func}`BArchivable::Instantiate`

## Archived Fields

The {cpp:func}`Archive() <BStringView::Archive>` function adds the
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
	- {hparam}`_text`

	- {cpp:enumerator}`B_STRING_TYPE`

	- Text displayed in the view (present only if it is not {cpp:expr}`NULL`).

-
	- {hparam}`_align`

	- {cpp:enumerator}`B_INT32_TYPE`

	- Alignment of text in frame.


:::
