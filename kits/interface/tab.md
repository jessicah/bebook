# BTab
## Constructor and Destructor
::::{abi-group}

:::{cpp:function} BTab::BTab(BView* tabView = NULL)
:::
:::{cpp:function} BTab::BTab(BMessage* archive)
:::

Initializes the {hclass}`BTab` to be enabled, but neither selected nor the current
focus. The specified {hparam}`tabView` becomes the tab's target view—when the
tab is selected, its target view is activated. See the
{cpp:class}`BTabView` class for
further details on how this works.

If an {hparam}`archive` message is specified, the message's contents are used to
duplicate the archived {hclass}`BTab` object.

See also:
{cpp:func}`~BTab::SetView`

::::

::::{abi-group}

:::{cpp:function} virtual BTab::~BTab()
:::

Frees all memory the {hclass}`BTab` allocated. If there is a target view assigned
to the tab, it is removed from the parent window and deleted.

::::

## Hook Functions
::::{abi-group}

:::{cpp:function} virtual void BTab::DrawFocusMark(BView* owner, BRect frame)
:::
:::{cpp:function} virtual void BTab::DrawTab(BView* owner, BRect frame, tab_position position, bool full = true)
:::
:::{cpp:function} virtual void BTab::DrawLabel(BView* owner, BRect frame)
:::

These three functions can be implemented by your {hclass}`BTab`-derived class to
create a new visual appearance for your application's tabs. The owner is
the {cpp:class}`BView` in which your tab is being drawn, and the frame is the
rectangle in which the tab is to be drawn.

The {hmethod}`DrawFocusMark()` function draws the mark indicating that the {hclass}`BTab`
object is in focus. By default, this consists of a line in the keyboard
navigation color, drawn across the bottom of the tab's frame rectangle.

{hmethod}`DrawTab()` is called to draw the tab. It draws the tab's title by calling
{hmethod}`DrawLabel()`, then renders the lines to create the tab itself. The
position of the tab may affect how the tab is rendered—for example,
if the tab is frontmost, it may have a different appearance than the
other tabs.

If {hparam}`full` is {cpp:enum}`true`, the complete tab is drawn inside the frame rectangle. If
{hparam}`full` is {cpp:enum}`false`, the right side of the tab is being obscured by the tab to
its left, so the right edge should be eliminated or truncated as
necessary.

::::

## Member Functions
::::{abi-group}

:::{cpp:function} virtual status_t BTab::Archive(BMessage* archive, bool deep = true) const
:::

Calls the inherited version of
{cpp:func}`~BArchivable::Archive` and stores the
{hclass}`BTab` in the
{cpp:class}`BMessage` archive.

See also:
{cpp:func}`BArchivable::Archive`,
{cpp:func}`~BTab::Instantiate` static function

::::

::::{abi-group}

:::{cpp:function} bool BTab::IsEnabled() const
:::
:::{cpp:function} virtual void BTab::SetEnabled(bool enabled)
:::

The {hmethod}`IsEnabled()` function returns the {cpp:enum}`true` if the tab is enabled (and can
therefore be selected by the user) or {cpp:enum}`false` if the tab is disabled.

{hmethod}`SetEnabled()` is called to enable or disable the tab. Pass a value of {cpp:enum}`true`
to enable the tab, or {cpp:enum}`false` to disable it.

::::

::::{abi-group}

:::{cpp:function} bool BTab::IsSelected() const
:::
:::{cpp:function} virtual void BTab::Deselect()
:::
:::{cpp:function} virtual void BTab::Select(BView* owner)
:::

The {hmethod}`IsSelected()` function returns true if the tab is currently selected,
{cpp:enum}`false` if it's not.

{hmethod}`Deselect()` is called to deselect the tab. This removes the tab's target
view from the owner window by calling the target view's
{cpp:func}`~BView::RemoveSelf`
function.

{hmethod}`Select()` is called to select the tab. This also adds the tab's target
view to the specified owner view. This is called after the previously
selected tab's {hmethod}`Deselect()` function is called.

::::

::::{abi-group}

:::{cpp:function} const char* BTab::Label() const
:::
:::{cpp:function} virtual void BTab::SetLabel(const char* label)
:::

The {hmethod}`Label()` function returns the tab's label. The label is the same as
the target view's name.

{hmethod}`SetLabel()` is called to set the tab's label. This also changes the target
view's name to match the tab's label, if a target view exists.

:::{admonition} Note
:class: note
If the tab doesn't have a target view, {hmethod}`SetLabel()` does nothing. Make
sure a target view has been set (by calling
{cpp:func}`~BTab::SetView`,
{cpp:func}`BTabView::AddTab`
with a valid target view argument, or in the {hclass}`BTab` constructor) before you
call {hmethod}`SetLabel()`.
:::
::::

::::{abi-group}

:::{cpp:function} bool BTab::IsFocus() const
:::
:::{cpp:function} void BTab::MakeFocus(bool inFocus = true)
:::

{hmethod}`IsFocus()` returns {cpp:enum}`true` if the tab is the current focus or {cpp:enum}`false` if it is
not.

{hmethod}`MakeFocus()` specifies whether or not the tab is the current focus. Pass
{cpp:enum}`true` to make the tab the current focus, or {cpp:enum}`false` if you don't want it to
be the focus.

::::

::::{abi-group}

:::{cpp:function} BView* BTab::View() const
:::
:::{cpp:function} virtual void BTab::SetView(BView* view)
:::

The {hmethod}`View()` function returns the tab's target view.

{hmethod}`SetView()` is called to set the tab's target view to the specified {hparam}`view`.

::::

## Static Functions
::::{abi-group}

:::{cpp:function} static BArchivable* BTab::Instantiate(BMessage* archive)
:::

Returns a new {hclass}`BTab` object, allocated by new and created with the version
of the constructor that takes a {cpp:class}`BMessage`
archive. However, if the message doesn't contain archived data for a
{hclass}`BTab`, {hmethod}`Instantiate()` returns {cpp:enum}`NULL`.

See also:
{cpp:func}`BArchivable::Instantiate`,
{cpp:func}`~instantiate::object`,
{cpp:func}`~BTab::Archive`

::::

## Archived Fields