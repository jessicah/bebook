# BClipboard

A {cpp:class}`BClipboard` object is an interface to a clipboard, a
resource that provides system-wide, temporary data storage. Clipboards are
identified by name; if two apps want to refer to the same clipboard, they
simply create respective {cpp:class}`BClipboard` objects with the same
name:

:::{code}
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
through the global {cpp:func}`~BClipboard::be` variable, accesses the
default system clipboard. Data that you write to your
{cpp:func}`~BClipboard::be` object can be read from any other app's
{cpp:func}`~BClipboard::be` For example, the cut/copy/paste operations
defined by {cpp:class}`BTextView` transfer data through the system
clipboard.

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
(through its {cpp:func}`~BClipboard::Data` function). The
{cpp:class}`BMessage` follows these conventions:

- The {cpp:func}`~BMessage::what` value is unused.

- The data is stored in a message field. The field should be typed as
{cpp:enum}`B_MIME_TYPE`; the MIME type that describes the data should be
used as the name of the field that holds the data (see
"{cpp:func}`~BClipboard::Overview`" for an example).

- If the {cpp:class}`BMessage` contains more than one field, each field
should present the same data in a different format. For example, the
StyledEdit app writes text data in its own format (in order to encode the
fonts, colors, etc.) and also writes the data as plain ASCII text (MIME
type "text/plain").

## Writing to the Clipboard

The following annotated example shows how to write to the clipboard.

:::{code}
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



If you decide that you don't want to commit your changes, you should call
{cpp:func}`~BClipboard::Revert` before you unlock.

## Reading from the Clipboard

Here we show how to read a simple string from the clipboard.

:::{code}
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



## Persistence


