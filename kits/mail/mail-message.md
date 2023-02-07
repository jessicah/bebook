# BMailMessage
## Constructor and Destructor
::::{abi-group}

:::{cpp:function} BMailMessage::BMailMessage()
:::
Creates and returns a new {hclass}`BMailMessage` object, which is empty. You need
to call other functions defined by this class to fill out the message.
::::

::::{abi-group}

:::{cpp:function} BMailMessage::BMailMessage()
:::
Destroys the {hclass}`BMailMessage`, even if the
object's fields are "dirty." For
example, if you create a new {hclass}`BMailMessage` object with the intention of
sending a message, fill out some or all of the fields, and then delete
the object, the object is destroyed without being sent.
::::

## Member Functions
::::{abi-group}

:::{cpp:function} status_t BMailMessage::AddContent(const char* text, int32 length, uint32 encoding = B_ISO1_CONVERSION, bool replace = false)
:::
:::{cpp:function} status_t BMailMessage::AddContent(const char* text, int32 length, const char* encoding, bool replace = false)
:::
Adds the specified text (which contains length characters) to the
{hclass}`BMailMessage` object's content. The text's encoding is specified by the
{hparam}`encoding` parameter, either directly or by pointer.
If {hparam}`replace` is {cpp:enum}`true`, any
existing text is deleted before the new content
is added; otherwise, the specified text is appended to the end of the
existing message content.
:::{list-table}
---
header-rows: 1
---
-
	- Return Code
	- Description
-
	- {cpp:enum}`B_OK`.
	- The content was changed without error.
-
	- {cpp:enum}`B_ERROR`.
	- Unable to add the new content.
:::
::::

::::{abi-group}

:::{cpp:function} status_t BMailMessage::AddEnclosure(entry_ref* enclosure_ref, bool replace = false)
:::
:::{cpp:function} status_t BMailMessage::AddEnclosure(const char* path, bool replace = false)
:::
:::{cpp:function} status_t BMailMessage::AddEnclosure(const char* mime_type, void* data, int32 length, bool replace = false)
:::
Adds an attachment to the message. The first two forms of
{hmethod}`AddEnclosure()`
add a file to the message, given either an entry_ref pointer or a
pathname. The third form adds a block of memory (of the given {hparam}`length`) to
the message as an enclosure, with the specified MIME type.
If {hparam}`replace` is {cpp:enum}`true`,
any existing attachments—including the body of
the message—are removed before the new one is added; otherwise the
new enclosure is added, leaving previous attachments intact.
If you specify {cpp:enum}`true` for {hparam}`replace`,
not only will all existing enclosures
be discarded, but so will the content of the message body itself.
:::{list-table}
---
header-rows: 1
---
-
	- Return Code
	- Description
-
	- {cpp:enum}`B_OK`.
	- The content was changed without error.
-
	- {cpp:enum}`B_ERROR`.
	- Unable to add the new enclosure.
:::
::::

::::{abi-group}

:::{cpp:function} status_t BMailMessage::AddHeaderField(const char* field_name, const char* field_str, bool replace = false)
:::
Adds a header field to the {hclass}`BMailMessage` object. The value of the field
whose name is specified by {hparam}`field_name` is set to the string specified by
{hparam}`field_str`.
If {hparam}`replace` is {cpp:enum}`true`, all
existing header fields of the specified name are
deleted before adding the new header field; if {hparam}`replace`
is {cpp:enum}`false`, a new
header whose field is named {cpp:enum}`field_name` is added.
:::{list-table}
---
header-rows: 1
---
-
	- Return Code
	- Description
-
	- {cpp:enum}`B_OK`.
	- The content was changed without error.
-
	- {cpp:enum}`B_ERROR`.
	- Unable to add the new header field.
:::
::::

::::{abi-group}

:::{cpp:function} status_t BMailMessage::Send(bool send_now = false, bool remove_when_sent = false)
:::
Queues the message for transmission. If {hparam}`send_now`
is {cpp:enum}`true`, the message is
sent immediately; otherwise, it is placed in the queue to be sent the
next time {cpp:func}`~check::for`
is called or the mail daemon performs an
automatic mail check.
If the {hparam}`remove_when_sent` argument is
{cpp:enum}`true`, the message will be deleted
from the user's disk drive after it has been sent; otherwise, it will be
saved for posterity.
:::{list-table}
---
header-rows: 1
---
-
	- Return Code
	- Description
-
	- {cpp:enum}`B_OK`.
	- The message was queued successfully
-
	- {cpp:enum}`B_MAIL_NO_RECIPIENT`.
	- There needs to be either a "To" or "Bcc" field in the message.
:::
::::
