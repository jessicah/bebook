# BTextView
## Constructor and Destructor
::::{abi-group}

:::{cpp:function} BTextView::BTextView(BRect frame, const char* name, BRect textRect, uint32 resizingMode, uint32 flags)
:::
:::{cpp:function} BTextView::BTextView(BRect frame, const char* name, BRect textRect, const BFont* font, const rgb_color* color, uint32 resizingMode, uint32 flags)
:::
:::{cpp:function} BTextView::BTextView(BMessage* archive)
:::

Initializes the {hclass}`BTextView` to the
{hparam}`frame` rectangle, stated in its eventual
parent's coordinate system, assigns it an identifying {hparam}`name`, sets its
resizing behavior to {hparam}`resizingMode` and its drawing
behavior with {hparam}`flags`.
These four arguments—{hparam}`frame`, {hparam}`name`,
{hparam}`resizingMode`, and {hparam}`flags`—are
identical to those declared for the
{cpp:class}`BView` class and are passed to the
{cpp:class}`BView`
{cpp:func}`~BView::Constructor`.
The {hparam}`frame`, {hparam}`name`, and {hparam}`resizingMode` arguments are passed
to the {cpp:class}`BView` class
unchanged, but two flags are added to the flags
argument—{cpp:enum}`B_FRAME_EVENTS`, so that the
{hclass}`BTextView` can reformat the
text when it's resized, and {cpp:enum}`B_PULSE_NEEDED`, so that the caret marking the
insertion point can "blink" in time with {cpp:enum}`B_PULSE` messages. Later,
{cpp:func}`~BTextView::AttachedToWindow`
will set the window's pulse rate to 500,000 microseconds.

The text rectangle, {hparam}`textRect`, is stated in the
{hclass}`BTextView`'s coordinate
system. It determines where text in placed within the view's bounds
rectangle:

- The first line of text is placed at the top of the text rectangle. As additional lines of text are entered into the view, the text grows downward and may actually extend beyond the bottom of the rectangle.
- The left and right sides of the text rectangle determine where lines of text are placed within the view. Lines can be aligned to either side of the rectangle, or they can be centered between the two sides. See the {cpp:func}`~BTextView::SetAlignment` function.
- When lines wrap on word boundaries, the width of the text rectangle determines the maximum length of a line; each line of text can be as long as the rectangle is wide. When word wrapping isn't turned on, lines can extend beyond the boundaries of the text rectangle. See the {cpp:func}`~BTextView::SetWordWrap` function.

The bottom of the text rectangle is ignored; it doesn't limit the amount
of text the view can contain. The text can be limited by the number of
characters, but not by the number of lines.

If a default font is provided, the {hclass}`BTextView` will display its text in
that font, unless another font is later set. Similarly, if a default
color is specified, the text will be displayed in that color, unless the
color is subsequently changed. If the font is {cpp:enum}`NULL` or not specified, the
{hclass}`BTextView` uses the system plain font, be_plain_font. If the color pointer
is {cpp:enum}`NULL` or not specified, the text is drawn in black.

The constructor establishes the following default properties for a new
{hclass}`BTextView`:

- The text is selectable and editable. (See {cpp:func}`~BTextView::MakeSelectable` and {cpp:func}`~BTextView::MakeEditable`.)
- Multiple character formats are not permitted. (See {cpp:func}`~BTextView::SetStylable`.)
- The text is left-aligned. (See {cpp:func}`~BTextView::SetAlignment`.)
- The tab width is 28.0 coordinate units. (See {cpp:func}`~BTextView::SetTabWidth`.)
- Word wrapping is turned on. (See {cpp:func}`~BTextView::SetWordWrap`.)
- Automatic indenting is turned off. (See {cpp:func}`~BTextView::SetAutoindent`.)
- The maximum amount of data is permitted. (See {cpp:func}`~BTextView::SetMaxBytes`.)
- The view doesn't grow to accommodate more characters. (See {cpp:func}`~BTextView::MakeResizable`.)
- All characters the user may type are acceptable. (See {cpp:func}`~BTextView::DisallowChar`.)

See also:
{cpp:func}`~BTextView::AttachedToWindow`,
{cpp:func}`~BTextView::SetFontAndColor`,
the {cpp:class}`BView` {cpp:func}`~BView::Constructor`

::::

::::{abi-group}

:::{cpp:function} virtual BTextView::~BTextView()()
:::

Frees the memory the {hclass}`BTextView` allocated to hold the text and to store
information about it.

::::

## Hook Functions
::::{abi-group}

:::{cpp:function} virtual void BTextView::AttachedToWindow()
:::

Completes the initialization of the {hclass}`BTextView` object after it becomes
attached to a window. This function sets up the object so that it can
correctly format text and display it. Among other things, it sets the
drawing mode to {cpp:enum}`B_OP_COPY`. If the {hclass}`BTextView`
is targeted by scroll bars,
it adjusts them so that they're accurately set up for scrolling the text.

Because the {hclass}`BTextView` uses pulses to animate (or "blink") the caret, the
vertical line that marks the current insertion point, this function also
enables pulsing in the window and fixes the pulse rate at 2 per second.

{hmethod}`AttachedToWindow()` is called for you when the
{hclass}`BTextView` becomes part a
window's view hierarchy; you shouldn't call it yourself, though you can
override it. A function that's implemented by a derived class should
begin by incorporating the {hclass}`BTextView` version:

:::{code}
void MyText::AttachedToWindow()
{
   BTextView::AttachedToWindow()
   . . .
}
:::

If it doesn't, the {hclass}`BTextView` won't be able to properly display the text.

See also:
{cpp:func}`BView::AttachedToWindow`

::::

::::{abi-group}

:::{cpp:function} virtual void BTextView::DetachedFromWindow()
:::

Resets the cursor to the standard hand image ({cpp:enum}`B_HAND_CURSOR`) if it's
above the {hclass}`BTextView` when the
{hclass}`BTextView` is removed from the window.

See also:
{cpp:func}`BView::DetachedFromWindow`

::::

::::{abi-group}

:::{cpp:function} virtual void BTextView::Draw(BRect updateRect)
:::

Draws the {hclass}`BTextView`.

See also:
{cpp:func}`BView::Draw`

::::

::::{abi-group}

:::{cpp:function} virtual void BTextView::FrameResized(float width, float height)
:::

Overrides the {cpp:class}`BView`
{cpp:func}`~BView::FrameResized`
of this function to reset the ranges of the
{hclass}`BTextView`'s scroll bars and to update the sizes of their proportional
knobs whenever the size of the {hclass}`BTextView` changes.

See also: {cpp:func}`BView::FrameResized`

::::

::::{abi-group}

:::{cpp:function} virtual void BTextView::KeyDown(const char* bytes, int32 numBytes)
:::

Enters text at the current selection in response to the user's typing.
This function is called from the window's message loop for every report
of a key-down event—typically once for every character the user
types. However, it does nothing unless the {hclass}`BTextView` is the focus view
and the text it contains is editable.

If the character encoded in the bytes string is an editing instruction,
{hmethod}`KeyDown()` takes the appropriate action:

- If the character is from one of the arrow keys ({cpp:enum}`B_UP_ARROW`, {cpp:enum}`B_LEFT_ARROW`, {cpp:enum}`B_DOWN_ARROW`, or {cpp:enum}`B_RIGHT_ARROW`), it extends the selection or moves the insertion point in the appropriate direction, depending on the modifiers
- If the character is {cpp:enum}`B_BACKSPACE` or {cpp:enum}`B_DELETE`, it deletes the current selection—or the character preceding or following the current insertion point.
- If the character comes from one of the paging keys ({cpp:enum}`B_HOME`, {cpp:enum}`B_END`, {cpp:enum}`B_PAGE_UP`, or {cpp:enum}`B_PAGE_DOWN`), it scrolls the display.

Otherwise, it checks whether the character was registered as unacceptable
(by
{cpp:func}`~BTextView::DisallowChar`).
If not disallowed, it calls the
{cpp:func}`~BTextView::InsertText`
hook function to enter the character into the text and display it. Derived
classes can preview about-to-be-inserted characters by overriding
{cpp:func}`~BTextView::InsertText`.

See also:
{cpp:func}`BView::KeyDown`

::::

::::{abi-group}

:::{cpp:function} virtual void BTextView::MessageReceived(BMessage* message)
:::

Augments the {cpp:class}`BView` version of
{cpp:func}`~BView::MessageReceived` to handle scripting
requests, dropped data, and four editing messages—{cpp:enum}`B_CUT`, {cpp:enum}`B_COPY`,
{cpp:enum}`B_PASTE`, and {cpp:enum}`B_SELECT_ALL`.

If the message was dragged and dropped on the {hclass}`BTextView` and it contains
{cpp:enum}`B_MIME_TYPE` data under the name "text/plain", this function inserts the
new text at the point where it was dropped—but only if
{cpp:func}`~BTextView::AcceptsDrop`
returns {cpp:enum}`true` for the message.

This function handles {cpp:enum}`B_CUT`, {cpp:enum}`B_COPY`,
{cpp:enum}`B_PASTE`, and {cpp:enum}`B_SELECT_ALL` messages
by calling the
{cpp:func}`~BTextView::Cut`,
{cpp:func}`~BTextView::Copy`,
{cpp:func}`~BTextView::Paste`, and
{cpp:func}`~BTextView::SelectAll`
functions. A
{hclass}`BTextView` will get these messages, even if the application doesn't send
them, when it's the focus view and the user uses the
Command+x,
Command+c,
Command+v,
and Command+a
shortcuts. See
"{cpp:func}`~BTextView::Overview`"
in the class overview for information on how to set up compatible
Cut, Copy,
Paste, and Select All
menu items.

To inherit this functionality, {hmethod}`MessageReceived()` functions implemented by
derived classes should be sure to call the {hclass}`BTextView` version.

See also:
{cpp:func}`~BTextView::AcceptsPaste`,
{cpp:func}`~BTextView::InsertText`,
{cpp:func}`BView::MessageReceived`,
{cpp:func}`BInvoker::SetMessage`,
{cpp:func}`BInvoker::SetTarget`

::::

::::{abi-group}

:::{cpp:function} virtual void BTextView::MouseDown(BPoint point)
:::

Selects text, drags text, and positions the insertion point in response
to the user's mouse actions. If the {hclass}`BTextView` isn't already the focus
view for its window, this function calls
{cpp:func}`~BTextView::MakeFocus` to make it the focus
view.

{hmethod}`MouseDown()` is called for each mouse-down event that occurs inside the
{hclass}`BTextView`'s frame rectangle.

See also:
{cpp:func}`BView::MouseDown`

::::

::::{abi-group}

:::{cpp:function} virtual void BTextView::MouseMoved(BPoint point, uint32 transit, BMessage* message)
:::

Responds to {cpp:enum}`B_MOUSE_MOVED` messages by changing the cursor to the standard
I-beam image for editing text whenever the cursor enters the view and by
resetting it to the standard hand image when the cursor exits the view.
The cursor is changed to an I-beam for text that is selectable or
editable, but only if the {hclass}`BTextView` is the current focus view in the
active window. However, when the cursor moves over the current selection,
this function changes it from the I-beam back to the standard hand image.
This is done to indicate that it's possible to drag and drop the current
selection.

If a message is being dragged to the {hclass}`BTextView`, this function tests it
see whether it contains textual data and tracks it to its destination.

See also:
{cpp:func}`BView::MouseMoved`,
{cpp:func}`~BTextView::AcceptsDrop`

::::

::::{abi-group}

:::{cpp:function} virtual void BTextView::Pulse()
:::

Turns the caret marking the current insertion point on and off when the
{hclass}`BTextView` is the focus view in the active window.
{hmethod}`Pulse()` is called by
the system at regular intervals.

This function is first declared in the
{cpp:class}`BView` class.

See also:
{cpp:func}`BView::Pulse`

::::

::::{abi-group}

:::{cpp:function} virtual void BTextView::WindowActivated(bool flag)
:::

Highlights the current selection when the {hclass}`BTextView`'s window becomes the
active window (when {hparam}`flag` is
{cpp:enum}`true`)—provided that the {hclass}`BTextView` is
the current focus view—and removes the highlighting when the window
ceases to be the active window (when {hparam}`flag` is {cpp:enum}`false`).

If the current selection is empty (if it's an insertion point), it's
highlighted by turning the caret on and off (blinking it).

The Interface Kit calls this function for you whenever the {hclass}`BTextView`'s
window becomes the active window or it loses that status.

See also:
{cpp:func}`BView::WindowActivated`,
{cpp:func}`~BTextView::MakeFocus`

::::

## Member Functions
::::{abi-group}

:::{cpp:function} virtual bool BTextView::AcceptsDrop(const BMessage* archive)
:::
:::{cpp:function} virtual bool BTextView::AcceptsPaste(BClipboard* clipboard)
:::

These functions look at the data in their arguments, and return {cpp:enum}`true` if
its "acceptable." The default implementations return {cpp:enum}`true` if both of the
following are {cpp:enum}`true`:

- the {hclass}`BTextView` is editable
- the message or clipboard contains {cpp:enum}`B_MIME_TYPE` data stored under the name "text/plain".

If the data isn't acceptable, the drop or paste operation is aborted.

{hmethod}`AcceptsDrop()` is invoked in two places: When a message is dragged over
the {hclass}`BTextView`, and when the message is dropped on the object.
{hmethod}`AcceptsPaste()` is called when a {cpp:enum}`B_PASTE` message is received. If you
augment these functions to accept more types, you'll also have to augment
the
{cpp:func}`~BTextView::MessageReceived`
and
{cpp:func}`~BTextView::Paste`
functions to insert the text found in
message or clipboard.

::::

::::{abi-group}

:::{cpp:function} virtual status_t BTextView::Archive(BMessage* archive, bool deep = true) const
:::

Calls the inherited version of
{cpp:func}`~BView::Archive`
and stores the {hclass}`BTextView` in the
{cpp:class}`BMessage` archive.

See also:
{cpp:func}`BArchivable::Archive`,
{cpp:func}`~BTextView::Instantiate` static function

::::

::::{abi-group}

:::{cpp:function} virtual bool BTextView::CanEndLine(int32 offset)
:::

Returns {cpp:enum}`true` if the character at offset can be the last character in a
line of text, and {cpp:enum}`false` if not. Sometimes this depends on whether the
next character (if there is one) can begin a line. This function is
called as the {hclass}`BTextView` figures out where to break lines, but only if
word wrapping is turned on.

As implemented, {hmethod}`CanEndLine()` allows the following ASCII characters to end
a line regardless of the context:

:::{code}
B_SPACE =  < / &
B_TAB   +  > *
B_ENTER -- ^ | '\0'
:::

The default implementation also understands the line-ending conventions
for Chinese and Japanese. Because these languages are written without the
spaces that typically end lines in other languages, lines can potentially
break anywhere. However, certain characters are prohibited from ending a
line and others are prohibited from beginning a new line. {hmethod}`CanEndLine()`
prevents lines from ending either on a prohibited ending character or on
the character before a prohibited beginning character.

Derived classes can override this function to apply different criteria
for where lines end, possibly looking at the context of the offset
character. You can also augment the current implementation so that it
understands the conventions for other languages.

If you override this function to look to the left or right of the
character at offset, be sure to check that you haven't stepped beyond the
range of the text. For example, this version of the function makes sure
that the first hyphen of a pair doesn't break a line:

:::{code}
bool MyTextView::CanEndLine(int32 offset)
{
   if ( ByteAt[offset] == '-' ) {
      if ( TextLength() - offset > 1 ) {
            if ( ByteAt[offset + 1] == '-' )
               return false;
      }
   }
   return (baseClass::CanEndLine(offset));
}
:::

See also:
{cpp:func}`~BTextView::SetWordWrap`

::::

::::{abi-group}

:::{cpp:function} virtual void BTextView::Cut(BClipboard* clipboard)
:::
:::{cpp:function} virtual void BTextView::Copy(BClipboard* clipboard)
:::
:::{cpp:function} virtual void BTextView::Paste(BClipboard* clipboard)
:::
:::{cpp:function} virtual void BTextView::Clear()
:::

These functions implement the standard cut, copy, paste, and clear
commands. {hmethod}`Cut()` and {hmethod}`Copy()` both copy the current selection to the
specified clipboard; {hmethod}`Cut()` also deletes the text from the {hclass}`BTextView` and
removes it from the display. The text is entered in the clipboard as
{cpp:enum}`B_MIME_TYPE` data under the name "text/plain". {hmethod}`Paste()` looks in the
clipboard for just this type of data and pastes it into the
text—but only if
{cpp:func}`~BTextView::AcceptsPaste` returns {cpp:enum}`true`. The new text replaces
the current selection, or is placed at the site of the current insertion
point.

If the {hclass}`BTextView` supports multiple character formats,
{hmethod}`Cut()` and {hmethod}`Copy()`
also place a text_run_array structure describing the formats of the
copied text in the clipboard—as {cpp:enum}`B_MIME_TYPE` data under the name
"application/x-vnd.Be-text_run_array". If the {hclass}`BTextView` that takes text
from the clipboard supports multiple formats, {hmethod}`Paste()` looks for the
text_run_array in the clipboard and sets the formats of the pasted text
accordingly.

In most cases, the clipboard argument will be identical to the global
be_clipboard object.

The {hmethod}`Clear()` function simply removes the currently-selected text from the
{hclass}`BTextView` without affecting any clipboard. If there's no selection,
nothing happens.

See also:
{cpp:func}`~BTextView::AcceptsPaste`,
"{cpp:func}`~BTextView::Overview`" in the overview

::::

::::{abi-group}

:::{cpp:function} void BTextView::DisallowChar(uint32 aChar)
:::
:::{cpp:function} void BTextView::AllowChar(uint32 aChar)
:::

These functions inform the {hclass}`BTextView` whether the user should be allowed
to enter {hparam}`aChar` into the text. By default, all characters are allowed.
Call {hmethod}`DisallowChar()` for each character you want to prevent
the {hclass}`BTextView`
from accepting, preferably when first setting up the object. Although
declared as uint32, {hparam}`aChar` must be a character encoded in a single byte;
it can't be a 16-bit Unicode value or a multibyte UTF-8 string.

{hmethod}`AllowChar()` reverses the effect of {hmethod}`DisallowChar()`.

Alternatively, and for more control over the context in which characters
are accepted or rejected, you can implement an
{cpp:func}`~BTextView::InsertText` function for
the {hclass}`BTextView`.
{cpp:func}`~BTextView::InsertText`
is called for all insertions, including each
character the user types, all text the user drags to the {hclass}`BTextView`, and
all attempts to paste from the clipboard.

::::

::::{abi-group}

:::{cpp:function} virtual void BTextView::FindWord(int32 offset, int32* start, int32* finish)
:::

Looks for a sequence of characters that qualifies as a word—that
is, a sequence that the user can double-click to select—that
includes the character at {hparam}`offset`. This function places the offset of the
word's first character in the variable that {hparam}`start` refers to and the
offset following the last character in the word in the variable that
{hparam}`finish` refers to. If the {hparam}`offset`
character can't be part of a word, the
{hparam}`start` and {hparam}`finish` offsets will be identical.

As implemented, this function allows the user to select a group of
similar characters with a double-click. For example, in the following
line of malformed text,

:::{code}
"You what!!?"
:::

it would allow the user to select the words "You" and "what," the group
of spaces between the words, and the group of punctuation marks at the
end.

The function also defines similar groups of Japanese characters that can
be selected together.

::::

::::{abi-group}

:::{cpp:function} virtual void BTextView::GetDragParameters(BMessage* drag, BBitmap** bitmap, BPoint* point, BHandler** handler)
:::

{hmethod}`GetDragParameters()` is called when a drag session is initiated. The
values that it retrieves (by reference in the arguments) are passed on to
{cpp:func}`BView::DragMessage`.
If you don't supply a bitmap (if you set {hparam}`*bitmap` to
{cpp:enum}`NULL`), the outline rectangle version of
{cpp:func}`~BView::DragMessage` is used.

::::

::::{abi-group}

:::{cpp:function} void BTextView::GetSelection(int32* start, int32* finish)
:::

Provides the current selection by writing the offset before the first
selected character into the variable referred to by {hparam}`start` and the offset
after the last selected character into the variable referred to by
{hparam}`finish`. If no characters are selected, both offsets will record the
position of the current insertion point.

If the text isn't selectable, both offsets will be 0.

See also:
{cpp:func}`~BTextView::Select`

::::

::::{abi-group}

:::{cpp:function} void BTextView::GetTextRegion(int32 start, int32 finish, BRegion* region) const
:::

Calculates the region where the run of characters beginning at the {hparam}`start`
offset and ending at the {hparam}`finish` offset would be displayed within the
{hclass}`BTextView`'s coordinate system, and modifies the
{cpp:class}`BRegion` object passed as
the third argument, {hparam}`region`, so that it represents that region.

See also:
{cpp:func}`~BTextView::TextHeight`

::::

::::{abi-group}

:::{cpp:function} void BTextView::GoToLine(int32 index)
:::
:::{cpp:function} int32 BTextView::CurrentLine() const
:::
:::{cpp:function} int32 BTextView::CountLines() const
:::

{hmethod}`GoToLine()` moves the insertion point to the beginning of the line at
{hparam}`index`. The first line has an index of 0, the second line an index of 1,
and so on. If the index is out-of-range, the insertion point is moved to
the beginning of the line with the nearest in-range index—that is,
to either the first or the last line.

{hmethod}`CurrentLine()` returns the index of the line where the first character of
the selection—or the character following the insertion
point—is currently located.

{hmethod}`CountLines()` returns how many lines of text
the {hclass}`BTextView` currently
contains.

Like other functions that change the selection, {hmethod}`GoToLine()` doesn't
automatically scroll the display to make the new selection visible. Call
{cpp:func}`~BTextView::ScrollToSelection`
to be sure that the user can see the start of the selection.

::::

::::{abi-group}

:::{cpp:function} void BTextView::HideTyping(bool flag)
:::
:::{cpp:function} bool BTextView::IsTypingHidden() const
:::

The first of these functions sets whether the user can see the text in
the {hclass}`BTextView`; the second returns whether or not the text is currently
visible. When flag's state is {cpp:enum}`true`, text contained by the
{hclass}`BTextView` isn't visible.

::::

::::{abi-group}

:::{cpp:function} inline void BTextView::Highlight(int32 start, int32 finish)
:::

Highlights (or unhighlights) the characters between the {hparam}`start` and {hparam}`finish`
offsets. This is the function that the {hclass}`BTextView` calls to highlight and
unhighlight the current selection. You don't need to call it yourself for
this purpose. It's in the public API just in case you may need to
highlight a range of text in some other circumstance.

If the text is not currently highlighted, this function highlights it.
But if the text is already highlighted, it unhighlights it. If you
highlight some text, be sure to unhighlight it before the next editorial
change; the {hclass}`BTextView` will not do it for you.

See also:
{cpp:func}`~BTextView::Select`,
{cpp:func}`~BTextView::GetTextRegion`

::::

::::{abi-group}

:::{cpp:function} void BTextView::Insert(const char* text, const text_run_array* runs = NULL)
:::
:::{cpp:function} void BTextView::Insert(const char* text, int32 length, const text_run_array* runs = NULL)
:::
:::{cpp:function} void BTextView::Insert(int32 offset, const char* text, int32 length, const text_run_array* runs = NULL)
:::
:::{cpp:function} void BTextView::Delete()
:::
:::{cpp:function} void BTextView::Delete(int32 start, int32 finish)
:::

{hmethod}`Insert()` adds {hparam}`length` bytes of
text to the {hclass}`BTextView`—or if a length
isn't specified, all the characters of the text string up to the null
character that terminates it. The text is inserted at {hparam}`offset`—or at
the beginning of the current selection if an {hparam}`offset` isn't specified. The
current selection is not deleted and the insertion is not selected.

The inserted characters are displayed in the fonts and colors specified
in the accompanying {hparam}`runs` array, provided the
{hclass}`BTextView` allows multiple
character formats. If multiple formats aren't allowed, the {hparam}`runs` array is
ignored. If multiple formats are allowed but a {hparam}`runs` array isn't provided,
the insertion is displayed in the font and color in force at the point of
insertion. This generally means the font and color of the first character
of the selection, or of the character immediately preceding the offset
character.

Offsets in the {hparam}`runs` array should describe the text being inserted; in
other words, the first offset should be 0. See
{cpp:func}`~BTextView::SetRunArray` for a
description of the text_run_array structure.

{hmethod}`Insert()` doesn't assume responsibility
for the {hparam}`text` data or the {hparam}`runs`
array. It copies the information it needs.

{hmethod}`Delete()` removes the characters bounded by the
{hparam}`start` and {hparam}`finish` offsets
from the display and deletes them from the {hclass}`BTextView`'s text, without
copying them to the clipboard. If the {hparam}`start`
and {hparam}`finish` offsets are the
same, nothing is deleted. If offsets are not provided, {hmethod}`Delete()` deletes
the current selection.

See also:
{cpp:func}`~BTextView::SetText`,
{cpp:func}`~BTextView::Cut`,
{cpp:func}`~BTextView::SetRunArray`

::::

::::{abi-group}

:::{cpp:function} virtual void BTextView::InsertText(const char* text, int32 length, int32 offset, const text_run_array* runs = NULL)
:::
:::{cpp:function} virtual void BTextView::DeleteText(int32 start, int32 finish)
:::

These protected functions are the vehicles through which the {hclass}`BTextView`
performs every insertion and deletion of text (with one exception). You
can augment them in a subclass to take note of pending changes to the
text, and to modify or prevent the change.

Don't call {hmethod}`Insert()`, {hmethod}`Delete()`
or any other high-level text-manipulating
function in your implementation.

{hmethod}`InsertText()` adds {hparam}`length` bytes
of text to the {hclass}`BTextView`, inserting it at
{hparam}`offset` within the text buffer. The font and color of the inserted
characters may be described by an accompanying {hparam}`runs` array. If the
{hclass}`BTextView` doesn't support multiple character formats, the {hparam}`runs` array is
ignored. If multiple formats are supported but the {hparam}`runs` array is {cpp:enum}`NULL`,
the text is displayed in the font and color of the character preceding
offset (or of the first character, if offset is 0.)

The offsets in the {hparam}`runs` data structure are relative to the inserted text;
that is, the first offset in the array is 0, not {hparam}`offset`.

{hmethod}`InsertText()` is called for every insertion, except one. The exception
occurs when {cpp:func}`~BTextView::SetText`
takes text from a file; in this case the text goes
directly from the file to the {hclass}`BTextView`; it's not stored in a temporary
buffer while {hmethod}`InsertText()` is called.

{hmethod}`DeleteText()` removes the text bounded by the
{hparam}`start` and {hparam}`finish` offsets. It
fails if the offsets don't differ, or if the {hparam}`finish` offset isn't greater
than the {hparam}`start` offset. This function is called for every deletion.

See also:
{cpp:func}`~BTextView::Insert`,
{cpp:func}`~BTextView::Delete`

::::

::::{abi-group}

:::{cpp:function} int32 BTextView::LineAt(int32 offset) const
:::
:::{cpp:function} int32 BTextView::LineAt(BPoint point) const
:::
:::{cpp:function} BPoint BTextView::PointAt(int32 offset, float* height = NULL) const
:::
:::{cpp:function} int32 BTextView::OffsetAt(int32 offset) const
:::
:::{cpp:function} int32 BTextView::OffsetAt(BPoint point) const
:::

These functions translate between coordinate values, text offsets, and
line indices. {hmethod}`LineAt()` returns the index of the line containing the
character at {hparam}`offset` in the text, or the line located at the specified
{hparam}`point` in the {hclass}`BTextView`'s coordinate system. Line indices begin at 0.

{hmethod}`PointAt()` returns the coordinate location of the character at {hparam}`offset`. The
point is the left top corner of a rectangle enclosing the character and
is stated in the {hclass}`BTextView`'s coordinate system. The x-coordinate of the
point is the position on the baseline where the character is (or would
be) drawn; its y-coordinate is the top of the line where the {hparam}`offset`
character is located. If a {hparam}`height` argument is provided, {hmethod}`PointAt()` returns
the height of the line by reference.

{hmethod}`OffsetAt()` returns the offset to the character that begins the {hparam}`index`
line, or to the character displayed at {hparam}`point`.

::::

::::{abi-group}

:::{cpp:function} float BTextView::LineHeight(int32 index = 0) const
:::
:::{cpp:function} float BTextView::TextHeight(int32 firstIndex, int32 lastIndex) const
:::

{hmethod}`LineHeight()` returns the height of the line of text at {hparam}`index`, or the
first line if an index isn't specified. Line indices begin at 0. The
height is stated in coordinate units and depends on the font. It's the
sum of how far characters can ascend above and descend below the
baseline, plus the amount of leading that separates lines. If more than
one font is used on the line, the ascent is taken from the tallest font
and the descent and leading from the deepest.

{hmethod}`TextHeight()` returns the height of the set of lines from {hparam}`firstIndex`
through {hparam}`lastIndex`.

Both functions reset out-of-range indices to be in-range—that is,
to the index of the first or last line.

See also:
{cpp:func}`BFont::GetHeight`

::::

::::{abi-group}

:::{cpp:function} float BTextView::LineWidth(int32 index = 0) const
:::

Returns the width of the line at {hparam}`index`—or, if no index is given,
the width of the first line. The value returned is the sum of the widths
(in coordinate units) of all the characters in the line, from the first
through the last, including tabs and spaces. Line indices begin at 0.

If the {hparam}`index` passed is out-of-range, it's reinterpreted to be the nearest
in-range index—that is, as the index to the first or the last line.

See also:
{cpp:func}`BFont::StringWidth`

::::

::::{abi-group}

:::{cpp:function} void BTextView::MakeEditable(bool flag = true)
:::
:::{cpp:function} bool BTextView::IsEditable() const
:::

The first of these functions sets whether the user can edit the text
displayed by the {hclass}`BTextView`; the second returns whether or not the text is
currently editable. Text is editable by default.

When text is editable but not selectable, the user can enter and delete
text at the insertion point, but can't select text to make changes to
more than one character at a time.

See also:
{cpp:func}`~BTextView::MakeSelectable`

::::

::::{abi-group}

:::{cpp:function} virtual void BTextView::MakeFocus(bool flag = true)
:::

Overrides the {cpp:class}`BView` version of
{cpp:func}`~BView::MakeFocus` to highlight the current
selection when the {hclass}`BTextView` becomes the focus view (when
{hparam}`flag` is {cpp:enum}`true`)
and to unhighlight it when the {hclass}`BTextView` no longer is the focus view
(when {hparam}`flag` is {cpp:enum}`false`). However, the
current selection is highlighted only
if the {hclass}`BTextView`'s window is the current active window.

This function is called for you whenever the user's actions make the
{hclass}`BTextView` become the focus view, or force it to give up that status.

See also:
{cpp:func}`~BTextView::MouseDown`

::::

::::{abi-group}

:::{cpp:function} void BTextView::MakeResizable(bool resizable, BView* containerView = NULL)
:::
:::{cpp:function} bool BTextView::IsResizable() const
:::

{hmethod}`MakeResizable()` gives the {hclass}`BTextView`
the ability to automatically resize
itself to fit its contents if the {hparam}`resizable` flag is
{cpp:enum}`true`, and takes away
that ability if the flag is {cpp:enum}`false`. {hmethod}`IsResizable()` returns whether the
{hclass}`BTextView` is currently resizable.

The frame rectangle and text rectangle of a resizable {hclass}`BTextView`
automatically grow and shrink to exactly enclose all the characters
entered by the user. The object should display just a single line of text
(the resizing is horizontal); if the {hparam}`resizable` flag is {cpp:enum}`true`,
{hmethod}`MakeResizable()` turns off line wrapping. The text can be aligned to the
left, right, or center of the text rectangle.

The {hparam}`containerView` is a view that draws a border around the text (like a
{cpp:class}`BScrollView` object) and is
the parent of the {hclass}`BTextView`; it's the view
that's resized to fit the text. The {hclass}`BTextView`'s resizing mode should be
such that it will be resized in tandem with the container (for example,
{cpp:enum}`B_FOLLOW_LEFT_RIGHT` or {cpp:enum}`B_FOLLOW_ALL_SIDES`).
However, if the {hparam}`containerView`
is {cpp:enum}`NULL`, as it is by default, the {hclass}`BTextView`
itself is resized to fit the text.

If the {hparam}`resizable` flag is {cpp:enum}`false`, the
{hparam}`containerView` argument is ignored.

This resizing mechanism is an alternative to the automatic resizing
behavior provided in the {cpp:class}`BView`
class. It triggers resizing on the user's
entry of text, not on a change in the parent view's size. The two schemes
are incompatible; the container view (or the {hclass}`BTextView`, if there is no
container) should not automatically resize itself when its parent is
resized.

See also:
{cpp:func}`~BTextView::SetAlignment`

::::

::::{abi-group}

:::{cpp:function} void BTextView::MakeSelectable(bool flag = true)
:::
:::{cpp:function} bool BTextView::IsSelectable() const
:::

The first of these functions sets whether it's possible for the user to
select text displayed by the {hclass}`BTextView`; the second returns whether or not
the text is currently selectable. Text is selectable by default.

When text is selectable but not editable, the user can select one or more
characters to copy to the clipboard, but can't position the insertion
point (an empty selection), enter characters from the keyboard, or paste
new text into the view.

See also:
{cpp:func}`~BTextView::MakeEditable`

::::

::::{abi-group}

See {cpp:func}`BHandler::ResolveSpecifier`

::::

::::{abi-group}

:::{cpp:function} virtual void BTextView::ScrollToOffset(int32 offset)
:::
:::{cpp:function} void BTextView::ScrollToSelection()
:::

These functions scroll the text so that the character at {hparam}`offset`—or
the character that begins the current selection—is within the
visible region of the view. If the {hclass}`BTextView` is equipped with scroll
bars, the {cpp:class}`BScrollBar`
objects are informed so they can update themselves.

See also:
{cpp:func}`BView::ScrollTo`

::::

::::{abi-group}

:::{cpp:function} virtual void BTextView::Select(int32 start, int32 finish)
:::

Selects the characters from {hparam}`start` up to {hparam}`finish`,
where {hparam}`start` and {hparam}`finish`
are offsets into the {hclass}`BTextView`'s text. If
{hparam}`start` and {hparam}`finish` are the same,
the selection will be empty (an insertion point). See
"{cpp:func}`~BTextView::Overview`" in the
class overview for a discussion of the constraints on the offset
arguments.

Normally, the selection is changed by the user. This function provides a
way to change it programmatically.

If the {hclass}`BTextView` is the current focus view in the active window,
{hmethod}`Select()`
highlights the new selection (or displays a blinking caret at the
insertion point). However, it doesn't automatically scroll the contents
of the {hclass}`BTextView` to make the new selection visible. Call
{cpp:func}`~BTextView::ScrollToSelection`
to be sure that the user can see the start of the selection.

See also:
{cpp:func}`~BTextView::Text`,
{cpp:func}`~BTextView::GetSelection`,
{cpp:func}`~BTextView::ScrollToSelection`,
{cpp:func}`~BTextView::GoToLine`,
{cpp:func}`~BTextView::MouseDown`

::::

::::{abi-group}

:::{cpp:function} void BTextView::SelectAll()
:::

Selects the entire text of the {hclass}`BTextView`, and highlights it if the
{hclass}`BTextView` is the current focus view in the active window.

See also:
{cpp:func}`~BTextView::Select`

::::

::::{abi-group}

:::{cpp:function} void BTextView::SetAlignment(alignment where)
:::
:::{cpp:function} alignment BTextView::Alignment() const
:::

These functions set the way text is aligned within the text rectangle and
return the current alignment. Three settings are possible:

:::{list-table}
---
header-rows: 1
---
-
	- Constant
	- Description
-
	- {cpp:enum}`B_ALIGN_LEFT`
	- Each line is aligned at the left boundary of the text rectangle.
-
	- {cpp:enum}`B_ALIGN_RIGHT`
	- Each line is aligned at the right boundary of the text rectangle.
-
	- {cpp:enum}`B_ALIGN_CENTER`
	- Each line is centered between the left and right boundaries of the text rectangle.
:::

The default is {cpp:enum}`B_ALIGN_LEFT`.

::::

::::{abi-group}

:::{cpp:function} void BTextView::SetAutoindent(bool flag)
:::
:::{cpp:function} bool BTextView::DoesAutoindent() const
:::

These functions set and return whether a new line of text is
automatically indented the same as the preceding line. When set to {cpp:enum}`true`
and the user types Return at the end of a line that begins with tabs or
spaces, the new line will automatically indent past those tabs and spaces
to the position of the first visible character.

The default value is {cpp:enum}`false`.

::::

::::{abi-group}

:::{cpp:function} void BTextView::SetColorSpace(color_space space)
:::
:::{cpp:function} color_space BTextView::ColorSpace() const
:::

These functions set and return the color space of the offscreen bitmap
that buffers the drawing the {hclass}`BTextView` does. The default color space is
{cpp:enum}`B_CMAP8`.

See also: the {cpp:class}`BBitmap` class

::::

::::{abi-group}

:::{cpp:function} void BTextView::SetDoesUndo(bool sayIt)
:::
:::{cpp:function} bool BTextView::DoesUndo() const
:::
:::{cpp:function} undo_state BTextView::UndoState(bool* isRedo) const
:::
:::{cpp:function} virtual void BTextView::Undo(BClipboard* clipboard)
:::
:::{code}
enum undo_state {}
:::

These functions and enum comprise {hclass}`BTextView`'s undo world. The operations
that {hclass}`BTextView` can undo are listed below. The
default undo mechanism is one operation deep: Udoing undoes the previous
(undo-able) operation; a second (immediate) undo redoes the operation.

You call {hmethod}`SetDoesUndo()` to enable or disable the undo machinery for this
object. By default, undo is enabled. The ability to undo is also
controlled by the object's editability (
{cpp:func}`~BTextView::MakeEditable`), but this is a
tautology, since in order to have something to undo you have to have been
able to edit the object in the first place.

{hmethod}`DoesUndo()` tells you whether the object is "undoable" as set by
{hmethod}`SetDoesUndo()`. It doesn't take editability into consideration.

{hmethod}`UndoState()` tells you what the previous action was (as represented by the
constants listed below). This is the action that will be undone if the
object is told to undo. The {hparam}`isRedo` value that's returned by reference is
set to {cpp:enum}`true` if the previous action occurred because of an undo.

:::{list-table}
---
header-rows: 1
---
-
	- Constant
	- Description
-
	- {cpp:enum}`B_UNDO_UNAVAILABLE`
	- Nothing to undo
-
	- {cpp:enum}`B_UNDO_TYPING`
	- Text was inserted or deleted
-
	- {cpp:enum}`B_UNDO_CUT`
	- Selection was cut
-
	- {cpp:enum}`B_UNDO_PASTE`
	- Text was pasted
-
	- {cpp:enum}`B_UNDO_CLEAR`
	- Selection was cleared
-
	- {cpp:enum}`B_UNDO_DROP`
	- Message was dropped
:::

The {hmethod}`Undo()` hook function is called when the
{hclass}`BTextView` receives a {cpp:enum}`B_UNDO`
message. (By default, {cpp:enum}`B_UNDO` is bound to the window's
Command+z shortcut;
Undo menu items need to set up the binding explicitly.) The {hparam}`clipboard`
argument is a pointer to the be_clipboard; if you're using a custom
clipboard in your {hclass}`BTextView` subclass, you should pass along your
clipboard when you invoke the inherited version of {hmethod}`Undo()`.

Don't try to do too much in a subclass implementation of {hmethod}`Undo()`. In
particular, you probably won't get too far if you're trying to "broaden"
the undo tree.

::::

::::{abi-group}

:::{cpp:function} void BTextView::SetFontAndColor(int32 start, int32 finish, const BFont* font, uint32 properties = B_FONT_ALL, rgb_color* color = NULL)
:::
:::{cpp:function} void BTextView::SetFontAndColor(const BFont* font, uint32 properties = B_FONT_ALL, rgb_color* color = NULL)
:::
:::{cpp:function} void BTextView::GetFontAndColor(int32 offset, BFont* font, rgb_color* color = NULL) const
:::
:::{cpp:function} void BTextView::GetFontAndColor(BFont* font, uint32* sameProperties = B_FONT_ALL, rgb_color* color = NULL, bool* sameColor = NULL) const
:::

These functions set and get the font and color used to display the text.
If the {hclass}`BTextView` supports multiple character formats, {hmethod}`SetFontAndColor()`
sets the font and color of the characters bounded by the {hparam}`start` and {hparam}`finish`
offsets. If no offsets are given, it sets the font and color of the
current selection. However, if multiple character formats are not
supported, {hmethod}`SetFontAndColor()` ignores the offsets and formats the entire
text.

{hmethod}`SetFontAndColor()` works like
{cpp:class}`BView`'s
{cpp:func}`~BView::SetFont` function.
It sets the {hparam}`font`
to the attributes of the font {cpp:class}`BFont`
object that are enumerated by the
properties mask. The mask is formed by combining the following constants:

- {cpp:enum}`B_FONT_FAMILY_AND_STYLE`
- {cpp:enum}`B_FONT_SIZE`
- {cpp:enum}`B_FONT_SHEAR`
- {cpp:enum}`B_FONT_ROTATION`
- {cpp:enum}`B_FONT_SPACING`
- {cpp:enum}`B_FONT_ENCODING`
- {cpp:enum}`B_FONT_FACE`
- {cpp:enum}`B_FONT_FLAGS`

In addition, {cpp:enum}`B_FONT_ALL` is a shorthand for all properties of the
specified font. However, the {hclass}`BTextView` modifies the font to ensure that:

- Characters are not rotated.
- Antialiasing is not disabled.
- The spacing mode is {cpp:enum}`B_BITMAP_SPACING`.
- The character encoding is UTF-8 ({cpp:enum}`B_UNICODE_UTF8`).

If the {hparam}`font` argument is {cpp:enum}`NULL`,
the font is not set and the properties mask is ignored.

The color of the characters is set by a pointer to an rgb_color
structure. If the pointer is {cpp:enum}`NULL`, as it is by default, the color is not
set.

{hmethod}`GetFontAndColor()` gets the font and color used to display the character
at {hparam}`offset`. It modifies the {hparam}`font`
{cpp:class}`BFont` object and the {hparam}`color`
rgb_color
structure so that they describe the font and color of the character.

If an {hparam}`offset` isn't specified, {hmethod}`GetFontAndColor()`
looks at the current
selection. It provides a font and color description of the first
character of the selection—or the character at the insertion point
if the selection is empty. It also modifies that variable that the
{hparam}`sameProperties` argument refers to so that it lists all the font
properties that are uniform for all characters in the selection.
Similarly, it indicates, in the variable that {hparam}`sameColor` refers to,
whether all the characters in the selection are displayed in the same
color.

::::

::::{abi-group}

:::{cpp:function} void BTextView::SetMaxBytes(int32 max)
:::
:::{cpp:function} int32 BTextView::MaxBytes() const
:::

These functions set and return the maximum number of bytes that the
{hclass}`BTextView` can accept. The default is the maximum number of bytes that can
be designated by a signed 32-bit integer, a number sufficiently large to
accommodate all uses of a {hclass}`BTextView`. Use this function only if you need
to restrict the number of characters that the user can enter in a text
field.

Note that these functions count bytes, not characters.

::::

::::{abi-group}

:::{cpp:function} void BTextView::SetRunArray(int32 start, int32 finish, const text_run_array* runs)
:::
:::{cpp:function} text_run_array* BTextView::RunArray(int32 start, int32 finish, int32* length = NULL) const
:::

These functions set and return the font and color formats of all the
characters bounded by the {hparam}`start` and
{hparam}`finish` offsets. The formats are
described by a text_run_array structure, which has the following fields:

:::{list-table}
---
header-rows: 1
---
-
	- Field
	- Description
-
	- int32count
	- The number of text_run structures in the array.
-
	- text_runruns[1]
	- A structure describing the font and color formats in effect at a particular offset in the {hclass}`BTextView`'s text.
:::

The text_run structure describes a run of characters that share the same
font and color formats. It has three fields:

:::{list-table}
---
header-rows: 1
---
-
	- Field
	- Description
-
	- int32offset
	- An offset to the first byte of a character in the text buffer. The text run begins with this character; it continues until another run begins.
-
	- BFontfont
	- The font that's used to display the run of characters beginning at the specified offset.
-
	- rgb_colorcolor
	- The color that's used to display the run of characters beginning at the specified offset.
:::

The first offset of the first text_run in the array passed to
{hmethod}`SetRunArray()` should be 0; the array returned by
{hmethod}`RunArray()` also begins at offset 0.

If the {hclass}`BTextView` doesn't support multiple character formats,
{hmethod}`SetRunArray()` ignores the {hparam}`start`
and {hparam}`finish` offsets and sets the entire
text to the font and color of the first text_run in the array. Similarly,
{hmethod}`RunArray()` returns a text_run_array
with one text_run describing the entire text.

{hmethod}`RunArray()` returns a pointer to memory that it allocated (using
malloc()). It puts the number of bytes that it allocated in the variable
that the {hparam}`length` argument points to. Although
{hmethod}`RunArray()` allocated the
memory, the caller is responsible for freeing it when the returned
text_run_array is no longer needed.

{hmethod}`SetRunArray()` doesn't assume responsibility for the runs data it's
passed; it's up to the caller to free it.

See also:
{cpp:func}`~BTextView::SetFontAndColor`

::::

::::{abi-group}

:::{cpp:function} void BTextView::SetStylable(bool stylable)
:::
:::{cpp:function} bool BTextView::IsStylable() const
:::
 {hmethod}`SetStylable()` sets whether the
{hclass}`BTextView` permits multiple character formats. If
the {hparam}`stylable` flag is
{cpp:enum}`true`, the functions that set the font and color of
the text can apply to particular characters in the text buffer. If the flag
is {cpp:enum}`false`, those functions apply only to the entire
text. When {hmethod}`SetStylable()` is called to turn off
support for multiple formats, all the text is reformatted in the font and
color of the first character. 
 {hmethod}`IsStylable()` returns whether multiple
formats are permitted. By default, they're not. 
See also:
{cpp:func}`~BTextView::SetFontAndColor`
{cpp:func}`~BTextView::SetRunArray`
::::

::::{abi-group}

:::{cpp:function} void BTextView::SetTabWidth(float width)
:::
:::{cpp:function} float BTextView::TabWidth() const
:::

These functions set the distance between tab stops to {hparam}`width` coordinate
units and return the current tab width. Tabs cannot be removed nor can
they be individually set; all tabs have a uniform width. The default tab
width is 28.0 coordinate units.

::::

::::{abi-group}

:::{cpp:function} void BTextView::SetText(const char* text, const text_run_array* runs = NULL)
:::
:::{cpp:function} void BTextView::SetText(const char* text, int32 length, const text_run_array* runs = NULL)
:::
:::{cpp:function} void BTextView::SetText(BFile* file, int32 offset, int32 length, const text_run_array* runs = NULL)
:::

Removes any text currently in the {hclass}`BTextView` and
copies new text from a {hparam}`text` buffer or from a
{hparam}`file` to replace it. This function copies
{hparam}`length` bytes of text from the buffer—or all
the bytes in the buffer, up to the null character, if a
{hparam}`length` isn't specified. Or it copies
{hparam}`length` bytes from the {hparam}`file`
beginning at the {hparam}`offset` byte. If the
{hparam}`text` or {hparam}`file` is
{cpp:enum}`NULL` or {hparam}`length` is 0, it empties
the {hclass}`BTextView` without replacing the text.

If a {hparam}`runs` text_run_array is provided, it will be used to set the font and
color formats of the new text—provided that the {hclass}`BTextView` permits
multiple character formats. If not, the {hparam}`runs` array is ignored.

The {hclass}`BTextView` doesn't assume ownership of the
{hparam}`text` buffer, the {hparam}`file`, or the
{hparam}`runs` array; you can delete them when
{hmethod}`SetText()` returns.

Text taken from a file is inserted directly into the text, bypassing the
{cpp:func}`~BTextView::InsertText`
function. In other words, you won't receive an
{cpp:func}`~BTextView::InsertText`
notification for text taken from a file.

This function is typically used to set the text initially displayed in
the view. If the {hclass}`BTextView` is already attached to a window, it's updated
to show its new contents.

See also:
{cpp:func}`~BTextView::Text`,
{cpp:func}`~BTextView::TextLength`

::::

::::{abi-group}

:::{cpp:function} void BTextView::SetTextRect(BRect rect)
:::
:::{cpp:function} BRect BTextView::TextRect() const
:::

{hmethod}`SetTextRect()` makes {hparam}`rect` the
{hclass}`BTextView`'s text rectangle—the
rectangle that locates where text is placed within the view. This
replaces the text rectangle originally set in the {hclass}`BTextView` constructor.
The layout of the text is recalculated to fit the new rectangle, and the
text is redisplayed.

{hmethod}`TextRect()` returns the current text rectangle.

See also:
the {hclass}`BTextView` {cpp:func}`~BTextView::Constructor`

::::

::::{abi-group}

:::{cpp:function} void BTextView::SetWordWrap(bool flag)
:::
:::{cpp:function} bool BTextView::DoesWordWrap() const
:::

These functions set and return whether the {hclass}`BTextView` wraps lines on word
boundaries, thus pushing entire words that don't fit at the end of a line
to the next line. When word wrapping is turned on, the {hclass}`BTextView` calls
{cpp:func}`~BTextView::CanEndLine`
to determine exactly where a line can break. If word
wrapping is off, lines break only on a newline character (where the user
types Return).

By default, word wrapping is turned on ({hmethod}`DoesWordWrap()`
returns {cpp:enum}`true`).

See also:
{cpp:func}`~BTextView::SetTextRect`

::::

::::{abi-group}

:::{cpp:function} const char* BTextView::Text() const
:::
:::{cpp:function} void BTextView::GetText(int32 offset, int32 length, char* buffer) const
:::
:::{cpp:function} uchar BTextView::ByteAt(int32 offset) const
:::

These functions reveal the text contained in the {hclass}`BTextView`.

{hmethod}`Text()` returns a pointer to the text, which may be a pointer to an empty
string if the {hclass}`BTextView` is empty. The returned pointer can be used to
read the text, but not to alter it (use
{cpp:func}`~BTextView::SetText`,
{cpp:func}`~BTextView::Insert`,
{cpp:func}`~BTextView::Delete`,
and other {hclass}`BTextView` functions to do that).

{hmethod}`GetText()` copies up to {hparam}`length` bytes of the text into {hparam}`buffer`, beginning
with the byte at {hparam}`offset`, and adds a null terminator ('0'). Fewer than
{hparam}`length` bytes are copied if there aren't that many between the specified
{hparam}`offset` and the end of the text. This function doesn't make any attempt to
ensure that only full character specifications are copied; it's up to the
caller to make sure that a character begins at {hparam}`offset` and that the last
byte copied isn't in the middle of a multibyte character. The results
won't be reliable if the {hparam}`offset` is out-of-range.

{hmethod}`ByteAt()` returns the byte located at {hparam}`offset`.
The offset doesn't have to be to the first byte of a character.

The pointer that {hmethod}`Text()` returns is to the {hclass}`BTextView`'s internal
representation of the text. When it returns, the text string is
guaranteed to be null-terminated and without gaps. However, the {hclass}`BTextView`
may have had to manipulate the text to get it in that condition.
Therefore, there may be a performance price to pay if {hmethod}`Text()` is called
frequently. If you're going to copy the text, it's more efficient to have
{hmethod}`GetText()` do it for you. If you're going to index into the text, it may
be more efficient to call {hmethod}`ByteAt()`.

The pointer that {hmethod}`Text()` returns may no longer be valid after the user or
the program next changes the text. Even if valid, the string may no
longer be null-terminated and gaps may appear.

See also:
{cpp:func}`~BTextView::TextLength`

::::

::::{abi-group}

:::{cpp:function} int32 BTextView::TextLength() const
:::

Returns the number of bytes of text data the {hclass}`BTextView` currently
contains—the number of bytes in the string that
{cpp:func}`~BTextView::Text` returns (not
counting the null terminator).

See also:
{cpp:func}`~BTextView::SetMaxBytes`

::::

## Static Functions
::::{abi-group}

:::{cpp:function} static void* BTextView::FlattenRunArray(const text_run_array* runs = NULL, int32* numBytes = NULL)
:::
:::{cpp:function} static text_run_array* BTextView::UnflattenRunArray(const void* data, int32* numBytes = NULL)
:::

These functions flatten and unflatten a text_run_array structure so that
it can be treated as an untyped stream of bytes. A text_run_array that's
saved on-disk will be valid when the user reboots the machine only if
it's saved as flat data. Both functions return pointers to memory they
allocate (with malloc()). The caller is responsible for freeing the
memory when it's no longer needed.

{hmethod}`FlattenRunArray()` flattens the runs
text_run_array and returns the flat data.
{hmethod}`UnflattenRunArray()` reconstructs a
text_run_array from previously flattened data and returns a
pointer to the structure.

If a {hparam}`numBytes` argument is provided, both functions place the number of
bytes they allocated for the data in the variable that {hparam}`numBytes` refers to.

See also:
{cpp:func}`~BTextView::SetRunArray`

::::

::::{abi-group}

:::{cpp:function} static BArchivable* BTextView::Instantiate(BMessage* archive)
:::

Returns a new {hclass}`BTextView` object, allocated by new and created by the
version of the constructor that takes a
{cpp:class}`BMessage` archive. However, if the
archive doesn't contain data for a {hclass}`BTextView` object, the return value
will be {cpp:enum}`NULL`.

See also:
{cpp:func}`BArchivable::Instantiate`,
{cpp:func}`~BTextView::Archive`

::::

## Scripting Support
::::{abi-group}

The current text selection

Using two int32 offsets to the beginning and end of the selection in
either the "result" or "data" arrays, these messages convey the current
selection of the object in a manner identical to
{cpp:func}`~BTextView::GetSelection` and
{cpp:func}`~BTextView::Select`.

MessageSpecifiersDescriptionB_GET_PROPERTYB_DIRECT_SPECIFIERReturns the current selection.B_SET_PROPERTYB_DIRECT_SPECIFIERSets the current selection.
::::

::::{abi-group}

The text in the view

The "Text" get and set messages correspond to the method
{cpp:func}`~BTextView::GetText` and
{cpp:func}`~BTextView::SetText`,
using a C string to store the data. If the {cpp:enum}`B_SET_PROPERTY`
message lacks a "data" member, the selection is deleted; otherwise,
"range" bytes are inserted at offset "index." The values specifying the
range are given in byte rather than character offsets. The range counts
towards the end of the text, even for {cpp:enum}`B_REVERSE_RANGE_SPECIFIER`.

MessageSpecifiersDescriptionB_COUNT_PROPERTYB_DIRECT_SPECIFIERReturns the length of the text in bytes.B_GET_PROPERTYB_RANGE_SPECIFIER, B_REVERSE_RANGE_SPECIFIERReturns the text in the specified range in the BTextView.B_SET_PROPERTYB_RANGE_SPECIFIER, B_REVERSE_RANGE_SPECIFIERRemoves or inserts text into the specified range in the BTextView.
::::

::::{abi-group}

Font and color information for the text

These messages correspond to the methods
{cpp:func}`~BTextView::RunArray` and
{cpp:func}`~BTextView::SetRunArray`,
storing the result as a {cpp:enum}`B_RAW_TYPE`. As with the "Text" property, the
values specifying the range are given in byte rather than character
offsets. The range counts towards the end of the text, even for
{cpp:enum}`B_REVERSE_RANGE_SPECIFIER`.

MessageSpecifiersDescriptionB_GET_PROPERTYB_RANGE_SPECIFIER, B_REVERSE_RANGE_SPECIFIERReturns the style information for the text in the specified range in the BTextView.B_SET_PROPERTYB_RANGE_SPECIFIER, B_REVERSE_RANGE_SPECIFIERSets the style information for the text in the specified range in the BTextView.
::::

## Archived Fields