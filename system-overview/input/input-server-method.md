# BInputServerMethod

{cpp:class}`BInputServerMethod` is a base class for input methods; these
are instances of {cpp:class}`BInputServerMethod` that act as an interface
between the user and languages using character sets that can't be easily
represented on standard keyboards, such as the Japanese input method that
comes with BeOS.

Input methods generally handle {cpp:enumerator}`B_KEY_DOWN` messages in
their {cpp:func}`Filter() <BInputServerFilter::Filter>` function (see
{cpp:class}`BInputServerFilter`), keeping some sort of state around to
translate these standard keyboard messages into new
{cpp:enumerator}`B_KEY_DOWN` messages representing another character set.
An input method can handle any input event, they're not limited to keyboard
events.

:::{admonition} Warning
:class: warning
Writing an input method is an involved process, even though the
{hclass}`BInputServerMethod` protocol is relatively simple. If you're
working on an input method, please feel free to contact Be Developer
Technical Support (devsupport@be.com) for additional information.
:::

## Input Method Events

Input methods insert {cpp:enumerator}`B_INPUT_METHOD_EVENT` messages
(using their {cpp:func}`EnqueueMessage()
<BInputServerMethod::EnqueueMessage>` function) into the Input Server's
event stream. These messages let {cpp:class}`BView` subclasses work
together with your input method to create a seamless experience for the
user.

Each {cpp:enumerator}`B_INPUT_METHOD_EVENT` message contains a
{hparam}`be:opcode` field (an {htype}`int32` value) indicating the kind of
event:

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
	- {cpp:enumerator}`B_INPUT_METHOD_STARTED`
	- Indicates that a new input transaction has begun. Add a
		{cpp:class}`BMessenger` in the {hparam}`be:reply_to` field; the receiver of
		the message will use this messenger to communicate with you during the
		transaction.
-
	- {cpp:enumerator}`B_INPUT_METHOD_STOPPED`
	- Indicates that the transaction is over.

:::

In between the {cpp:enumerator}`B_INPUT_METHOD_STARTED` and
{cpp:enumerator}`B_INPUT_METHOD_STOPPED` messages, you'll send
{cpp:enumerator}`B_INPUT_METHOD_CHANGED` and
{cpp:enumerator}`B_INPUT_METHOD_LOCATION_REQUEST` messages as the
transaction proceeds.

{cpp:enumerator}`B_INPUT_METHOD_CHANGED` does most of the work in an input
transaction; add the following important fields:

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-
	- Entry

	- Type

	- Description

-
	- {hparam}`be:string`

	- {cpp:enumerator}`B_STRING_TYPE`

	- The text the user is currently entering; the receiver will display it at
the current insertion point. {cpp:class}`BTextView` also highlights the
text in blue to show that it's part of a transitory transaction.

-
	- {hparam}`be:selection`

	- {cpp:enumerator}`B_INT32_TYPE`

	- A pair of B_INT32_TYPE offsets into the {hparam}`be:string` if part of
{hparam}`be:string` is current selected. {cpp:class}`BTextView` highlights
this selection in red instead of drawing it in blue.

-
	- {hparam}`be:clause_start`

	- {cpp:enumerator}`B_INT32_TYPE`

	- Zero or more offsets into the {hparam}`be:string` for handling languages
(such as Japanese) that separate a sentence or phrase into numerous
clauses. An equal number of {hparam}`be:clause_start` and
{hparam}`be:clause_end` pairs delimit these clauses; {cpp:class}`BTextView`
separates the blue/red highlighting wherever there is a clause boundary.

-
	- {hparam}`be:clause_end`

	- {cpp:enumerator}`B_INT32_TYPE`

	- Zero or more offsets into {hparam}`be:string`; there must be as many
{hparam}`be:clause_end` entries as there are {hparam}`be:clause_start`.

-
	- {hparam}`be:confirmed`

	- {cpp:enumerator}`B_BOOL_TYPE`

	- True when the user has entered and "confirmed" the current string and
wishes to end the transaction. {cpp:class}`BTextView` unhighlights the
blue/red text and waits for a {cpp:enumerator}`B_INPUT_METHOD_STOPPED` (to
close the transaction) or another {cpp:enumerator}`B_INPUT_METHOD_CHANGED`
(to start a new transaction immediately).


:::

{cpp:enumerator}`B_INPUT_METHOD_LOCATION_REQUEST` is the input method's
way of asking for the on-screen location of each character in
{hparam}`be:string`. This information can be used by the input method to
pop up additional windows giving the user an opportunity to select
characters from a list or anything else that makes sense. When you send a
{cpp:enumerator}`B_INPUT_METHOD_LOCATION_REQUEST`, the receiver will reply
to the {hparam}`be:reply_to` messenger (that you sent in your
{cpp:enumerator}`B_INPUT_METHOD_STARTED` message) with a
{cpp:enumerator}`B_INPUT_METHOD_EVENT` message, filling in the following
fields:

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-
	- Entry

	- Type

	- Description

-
	- {hparam}`be:opcode`

	- {cpp:enumerator}`B_INT32_TYPE`

	- Set to {cpp:enumerator}`B_INPUT_METHOD_LOCATION_REQUEST`.

-
	- {hparam}`be:location_reply`

	- {cpp:enumerator}`B_POINT_TYPE`

	- The co-ordinates of each character (there should be one
{hparam}`be:location_reply` for every character in {hparam}`be:string`)
relative to the display (not your view or your window).

-
	- {hparam}`be:height_reply`

	- {cpp:enumerator}`B_FLOAT_TYPE`

	- The height of each character in {hparam}`be:string`.


:::

## Creating

To create a new input method, you must:

-   Create a subclass of {cpp:class}`BInputServerMethod`

-   Implement the instantiate_input_method() C function to create an instance
of your {cpp:class}`BInputServerMethod` subclass

-   Compile the class and function as an add-on

-   Install the add-on in one of the input method directories

At boot time (or whenever the Input Server is restarted; see "Dynamic
Loading"), the Input Server loads the add-ons it finds in the input method
directories. For each add-on it finds, the Server invokes
instantiate_input_method() to get a pointer to the add-on's
{hclass}`BInputServerMethod` object. After constructing the object, the
Server calls {hmethod}`InitCheck()` to give the add-on a chance to bail out
if the constructor failed.

## Installing an Input Method

The input server looks for input methods in the "input_server/methods"
subdirectories of {cpp:enumerator}`B_BEOS_ADDONS_DIRECTORY`,
{cpp:enumerator}`B_COMMON_ADDONS_DIRECTORY`, and
{cpp:enumerator}`B_USER_ADDONS_DIRECTORY`.

-   You can install your input devices in the latter two directories—i.e.
those under {cpp:enumerator}`B_COMMON_ADDONS_DIRECTORY`, and
{cpp:enumerator}`B_USER_ADDONS_DIRECTORY`.

-   The {cpp:enumerator}`B_BEOS_ADDONS_DIRECTORY` is reserved for add-ons that
are supplied by the BeOS.
