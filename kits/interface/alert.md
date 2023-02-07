# BAlert
## Constructor and Destructor
::::{abi-group}

:::{cpp:function} BAlert::BAlert(const char* title, const char* text, const char* button0Label, const char* button1Label = NULL, const char* button2Label = NULL, button_width widthStyle = B_WIDTH_AS_USUAL, alert_type type = B_INFO_ALERT)
:::
:::{cpp:function} BAlert::BAlert(const char* title, const char* text, const char* button0Label, const char* button1Label, const char* button2Label, button_width widthStyle, button_spacing spacing, alert_type type = B_INFO_ALERT)
:::
:::{cpp:function} BAlert::BAlert(BMessage* archive)
:::
Creates an alert panel that's ready to be displayed. The arguments are:
:::{list-table}
---
header-rows: 1
---
-
	- title
	- Is the name of the panel. Since an alert panel doesn't have a title tab, the title isn't actually displayed in the panel. Nonetheless, it can be useful in debugging: The {hparam}`title` is used to name the window thread ("w>{hparam}`title`").
-
	- text
	- Is displayed in the body of the panel; it should describe the reason the panel is being shown ("Are you sure you want to quit?", "Invalid name.", etc.).
-
	- button0Label,button1Label,button2Label
	- Label the panel's buttons. An alert panel can have one, two, or three buttons—however many labels you supply is the number of buttons that are displayed. The buttons are arranged at the bottom of the panel as shown in the illustration above, and each is assigned an index (0, 1, or 2, left to right) that's used to identify the button that the user clicked.
-
	- widthStyle
	- Is a constant that describes how the buttons should be sized, one of {cpp:enum}`B_WIDTH_AS_USUAL`, {cpp:enum}`B_WIDTH_FROM_WIDEST`, or {cpp:enum}`B_WIDTH_FROM_LABEL`. See {cpp:func}`~button::width` for details.
-
	- spacing
	- Is a constant that describes how the buttons are spaced, either {cpp:enum}`B_EVEN_SPACING`, or {cpp:enum}`B_OFFSET_SPACING`. The constructor that lacks the spacing argument uses {cpp:enum}`B_EVEN_SPACING`. See {cpp:func}`~button::spacing` for details.
-
	- type
	- Is a constant that determines which of the five alert icons is displayed in the panel: {cpp:enum}`B_EMPTY_ALERT`, {cpp:enum}`B_INFO_ALERT`, {cpp:enum}`B_IDEA_ALERT`, {cpp:enum}`B_WARNING_ALERT`, or {cpp:enum}`B_STOP_ALERT`. See {cpp:func}`~alert::type` for pictures.
:::
After the {hclass}`BAlert` is constructed,
{cpp:func}`~BAlert::Go` must be called to display it. The
panel is removed and the object is deleted after the user clicks a button.
::::

::::{abi-group}

:::{cpp:function} BAlert::~BAlert()
:::
A standard destructor
::::

## Hook Functions
::::{abi-group}

See {cpp:func}`BWindow::FrameResized`

::::

::::{abi-group}

See {cpp:func}`BWindow::MessageReceived`

::::

## Member Functions
::::{abi-group}

:::{cpp:function} BPoint BAlert::AlertPosition(float width, float height) const
:::
Computes the "best" frame for an alert of the given
{hparam}`width` and {hparam}`height`, and
returns the top left corner of the computed frame in screen coordinates.
This function is called automatically when you construct your
{hclass}`BAlert`; you never have to invoke it
yourself.
::::

::::{abi-group}

:::{cpp:function} BButton* BAlert::ButtonAt(int32 index) const
:::

Returns a pointer to the
{cpp:class}`BButton` object identified by
{hparam}`index`. Indices
begin at 0 and count buttons from left to right. The {cpp:class}`BButton` belongs to
the {hclass}`BAlert` object and should not be freed.

::::

::::{abi-group}

:::{cpp:function} int32 BAlert::Go()
:::
:::{cpp:function} status_t BAlert::Go(BInvoker* invoker)
:::

Displays the alert panel. {hmethod}`Go()` can operate synchronously or
asynchronously:

- The no-argument version is synchronous: The function doesn't return until the user has clicked a button and the panel has been removed from the screen.. The value it returns is the index of the clicked button (0,1, or 2, left-to-right)..
- The {cpp:class}`BInvoker` argument version is asynchronous: The function returns immediately (with {cpp:enum}`B_OK`) and the button index is delivered as the int32 "which" field of the {cpp:class}`BMessage` that's sent to the {cpp:class}`BInvoker`'s target.

If you call {hmethod}`Go()` with a (literal) {cpp:enum}`NULL` argument…

:::{code}
alert->Go(NULL);
:::

…the asynchronous version is used, but the
{cpp:class}`BMessage` isn't sent.

The synchronous version deletes the object before it returns; the
asynchronous version deletes it after the message is sent. In either
case, you should consider the {hclass}`BAlert` object to be invalid after you call
{hmethod}`Go()`.

If the {hclass}`BAlert` is sent a
{cpp:func}`~B::QUIT`
message while the panel is still
on-screen, the synchronous version of {hmethod}`Go()` returns -1; the asynchronous
version suppresses the index-reporting message.

::::

::::{abi-group}

:::{cpp:function} void BAlert::SetShortcut(int32 index, char shortcut)
:::
:::{cpp:function} char BAlert::Shortcut(int32 index) const
:::

These functions set and return the shortcut character that's mapped to
the button at {hparam}`index`. A given button can have only one shortcut except for
the rightmost button, which, in addition to the shortcut that you give it
here, is always mapped to {cpp:enum}`B_ENTER.`

If you create a "Cancel" button, you should give it a shortcut of
{cpp:enum}`B_ESCAPE`.

::::

::::{abi-group}

:::{cpp:function} BTextView* BAlert::TextView() const
:::

Returns a pointer to the {cpp:class}`BTextView`
object that contains the textual
information that's displayed in the panel. You can fiddle with this
object but you mustn't delete it.

::::

## Constants and Defined Types
::::{abi-group}






Declared in: interface/Alert.h
:::{code}
enum alert_type
{
    B_EMPTY_ALERT,
    B_INFO_ALERT,
    B_IDEA_ALERT,
    B_WARNING_ALERT,
    B_STOP_ALERT
};
:::

The alert_type constants represent the five alert icons:

B_EMPTY_ALERTB_INFO_ALERTB_IDEA_ALERTB_WARNING_ALERTB_STOP_ALERT (none)
::::

::::{abi-group}



:::{code}
enum button_spacing
{
    B_EVEN_SPACING,
    B_OFFSET_SPACING
};
:::

Used to set the spacing of the alert's buttons:

:::{list-table}
---
header-rows: 1
---
-
	- {cpp:enum}`B_EVEN_SPACING`
	- The buttons are evenly spaced. (This is used by the constructor without the spacing argument.)
-
	- {cpp:enum}`B_OFFSET_SPACING`
	- If the alert has more than one button, the leftmost button is shifted left to separate it from its neighbor(s). You should use this configuration for an alert that has a (leftmost) "Cancel" button, as shown in the illustration at the beginning of this document.
:::
::::

## Archived Fields