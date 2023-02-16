# BClipboard

A {cpp:class}`BClipboard` object is an interface to a clipboard, a
resource that provides system-wide, temporary data storage. Clipboards are
identified by name; if two apps want to refer to the same clipboard, they
simply create respective {cpp:class}`BClipboard` objects with the same
name:

:::{code} cpp
/* App A: This creates a clipboard named "MyClipboard". */
BClipboard *appAclipboard = new BClipboard("MyClipboard");

/* App B: This object refers to the clipboard already created
   by App A. */
BClipboard *appBclipboard = new BClipboard("MyClipboard");
:::

## The System Clipboard

In practice, you rarely need to construct your own {cpp:class}`BClipboard`
object; instead, you use the {hclass}`BClipboard` that's created for you by
your {cpp:class}`BApplication` object. This object, which you refer to
through the global {cpp:var}`be_clipboard` variable, accesses the default
system clipboard. Data that you write to your {cpp:var}`be_clipboard`
object can be read from any other app's {cpp:var}`be_clipboard` For
example, the cut/copy/paste operations defined by {cpp:class}`BTextView`
transfer data through the system clipboard.

:::{admonition} Note
:class: note
To access the system clipboard without creating a
{cpp:class}`BApplication` object, construct a {cpp:class}`BClipboard`
object with the name "system". The system clipboard is under the control of
the user; you should only read or write the system clipboard as a direct
result of the user's actions. If you create your own clipboards don't name
them "system".
:::

## The Clipboard Message

To access a clipboard's data, you call functions on a
{cpp:class}`BMessage` that the {cpp:class}`BClipboard` object hands you
(through its {cpp:func}`Data() <BClipboard::Data>` function). The
{cpp:class}`BMessage` follows these conventions:

-   The {cpp:var}`what` value is unused.

-   The data is stored in a message field. The field should be typed as
{cpp:enumerator}`B_MIME_TYPE`; the MIME type that describes the data should
be used as the name of the field that holds the data (see "{ref}`Writing to
the Clipboard`" for an example).

-   If the {cpp:class}`BMessage` contains more than one field, each field
should present the same data in a different format. For example, the
StyledEdit app writes text data in its own format (in order to encode the
fonts, colors, etc.) and also writes the data as plain ASCII text (MIME
type "text/plain").

## Writing to the Clipboard

The following annotated example shows how to write to the clipboard.

:::{code} cpp
BMessage* clip = (BMessage *)NULL;
  if (be_clipboard->Lock()) {
    be_clipboard->Clear();
    if ((clip = be_clipboard->Data()) {
       clip->AddData("text/MyFormat", B_MIME_TYPE, myText,
                     myLength);
       clip->AddData("text/plain", B_MIME_TYPE, asciiText,
                     asciiLength);
       be_clipboard->Commit();
    }
    be_clipboard->Unlock();
 }
:::

:::{list-table}
---
header-rows: 0
align: left
widths: auto
---
-
	- {ref}``

	- {hmethod}`Lock()` your {cpp:class}`BClipboard` object. This uploads data
		from the clipboard into your {cpp:class}`BClipboard`'s local
		{cpp:class}`BMessage` object, and prevents other threads in your
		application from accessing the {cpp:class}`BClipboard`'s data. Note that
		locking does not lock the underlying clipboard data other applications can
		change the clipboard while you have your object locked.
-
	- {ref}``

	- Prepare the {cpp:class}`BClipboard` for writing by calling
		{hmethod}`Clear()`. This erases the data that was uploaded from the
		clipboard.
-
	- {ref}``

	- Call {cpp:func}`Data() <BClipboard::Data>` to get a pointer to the
		{cpp:class}`BClipboard`'s {cpp:class}`BMessage` object.
-
	- {ref}``

	- Write the data by invoking {cpp:func}`AddData() <BMessage::AddData>`
		directly on the {cpp:class}`BMessage`. In the example, we write the data in
		two different formats.
-
	- {ref}``

	- Call {cpp:func}`Commit() <BClipboard::Commit>` to copy your
		{cpp:class}`BMessage` back to the clipboard. As soon as you call
		{cpp:func}`Commit() <BClipboard::Commit>`, the data that you added is
		visible to other clipboard clients.
-
	- {ref}``

	- {cpp:func}`Unlock() <BClipboard::Unlock>` balances the {cpp:func}`Lock()
		<BClipboard::Lock>`. The {cpp:class}`BClipboard` object can now be accessed
		by other threads in your application.

:::

If you decide that you don't want to commit your changes, you should call
{cpp:func}`Revert() <BClipboard::Revert>` before you unlock.

## Reading from the Clipboard

Here we show how to read a simple string from the clipboard.

:::{code} cpp
const char *text;
int32 textLen;
BMessage *clip = (BMessage *)NULL;
 if (be_clipboard->Lock()) {
   if ((clip = be_clipboard->Data())
      clip->FindData("text/plain", B_MIME_TYPE,
          (const void **)text, textlen);

   be_clipboard-Unlock();
}
:::

:::{list-table}
---
header-rows: 0
align: left
widths: auto
---
-
	- {ref}``

	- As in writing, we bracket the operation with {cpp:func}`Lock()
		<BClipboard::Lock>` and {cpp:func}`Unlock() <BClipboard::Unlock>`. Keep in
		mind that {cpp:func}`Lock() <BClipboard::Lock>` uploads data from the
		clipboard into our object. Any changes that are made to the clipboard (by
		some other application) after {cpp:func}`Lock() <BClipboard::Lock>` is
		called won't be seen here.
-
	- {ref}``

	- In this example, we only look for one hard-coded format. In a real
		application, you may have a list of formats that you can look for.
-
	- {ref}``

	- It isn't necessary to examine the clipboard data before you unlock it. The
		{cpp:func}`FindData() <BMessage::FindData>` call could just as well have
		been performed after the {cpp:func}`Unlock() <BClipboard::Unlock>` call.

:::

## Persistence

Inter-boot persistence:

: Clipboard data does not persist between boots, the constructor provides a
persistence flag but it's currently unused.

Intra-boot persistence:

: Once you've created a clipboard, that clipboard will exist until you
reboot your computer. For example, let's say you design an app that creates
a clipboard called "MyClip": You launch the app, write something to
"MyClip", and then quit the app. The clipboard and the data that you wrote
to it will still exist: If you relaunch your app (or any app that knows
about "MyClip"), you can pick up the data by reading from the "MyClip"
clipboard.
