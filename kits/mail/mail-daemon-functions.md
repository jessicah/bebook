# The Mail Daemon Functions

## check_for_mail()















Sends and retrieves mail. More specifically, this function asks the mail
daemon to retrieve incoming messages from the POP server and send any
queued outgoing messages to the SMTP server. The number of POP messages
that were retrieved are stored in the variable pointed to by
{hparam}`incoming_count`. If you specify {cpp:expr}`NULL` for
{hparam}`incoming_count`, check_for_mail() won't return the number of
messages retrieved. You should specify {cpp:expr}`NULL` unless you really
want to know how many messages were retrieved, since requesting this
information could potentially slow down the retrieval process.

If all is well in the mail world, this function returns
{cpp:enumerator}`B_OK`; otherwise, it returns a highly useful result code.

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-
	- Return Code

	- Description

-
	- {cpp:enumerator}`B_OK`
	- Mail was sent and retrieved without incident.
-
	- {cpp:enumerator}`B_MAIL_NO_DAEMON`
	- The mail daemon isn't running.
-
	- {cpp:enumerator}`B_MAIL_UNKNOWN_USER`
	- The POP server doesn't recognize the user name.
-
	- {cpp:enumerator}`B_MAIL_WRONG_PASSWORD`
	- The POP server doesn't recognize the password.
-
	- {cpp:enumerator}`B_MAIL_UNKNOWN_HOST`
	- The POP or SMTP server can't be found.
-
	- {cpp:enumerator}`B_MAIL_ACCESS_ERROR`
	- The connection to the POP or SMTP server failed.

:::

## count_pop_accounts()





Returns the number of POP accounts that have been configured.

:::{admonition} Note
:class: note
The mail daemon currently supports only one POP account, so this function
will always return 1. You shouldn't assume there will only be one POP
account, though, as this will probably change in the future.
:::

## decode_base64()





Decodes the base-64 data pointed to by {hparam}`in`, which is
{hparam}`length` bytes long, and writes the decoded output into the buffer
pointed to by {hparam}`out`. If {hparam}`replace_cr` is {cpp:expr}`true`,
carriage return characters in the output are converted into newlines,
otherwise the data is returned in its original, unaltered, form.

You would typically specify {hparam}`replace_cr` as {cpp:expr}`true` if
you're decoding an ASCII text document, and as {cpp:expr}`false` if
decoding a binary file.

This function returns the size of the output data that's been stored in
the {hparam}`out` buffer.

:::{admonition} Warning
:class: warning
You must be certain, in advance, that the output buffer is large enough to
hold the decoded data, or this function will do bad things.
:::

## encode_base64()





Encodes the data pointed to by {hparam}`in`, which is {hparam}`length`
bytes long, and writes the base-64 encoded output into the buffer pointed
to by {hparam}`out`.

This function returns the size of the output data that's been stored in
the {hparam}`out` buffer.

:::{admonition} Warning
:class: warning
You must be certain, in advance, that the output buffer is large enough to
hold the encoded data, or this function will do bad things.
:::

## forward_mail()





Forwards the mail message specified by {hparam}`message_ref` to the list
of users given by {hparam}`recipients`. The list of user names specified in
{hparam}`recipients` must be separated by commas and/or whitespace, and
must be null-terminated.

If the {hparam}`now` parameter is {cpp:expr}`true`, the messages will be
sent immediately; if {cpp:expr}`false`, the message will be queued up to be
sent the next time {ref}`check_for_mail()` is called, or the next time the
mail daemon performs an automatic mail check.

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-
	- Return Code

	- Description

-
	- {cpp:enumerator}`B_OK`
	- The message was forwarded without error.
-
	- {cpp:enumerator}`B_MAIL_NO_RECIPIENT`
	- No valid recipients were specified.
-
	- Other Errors
	- Errors returned by {ref}`send_queued_mail()`, if {hparam}`now` is
		{cpp:expr}`true`.

:::

## get_mail_notification(), set_mail_notification(), mail_notification











get_mail_notification() fills the specified {htype}`mail_notification`
structure with information describing how the user is currently being
notified of received e-mail. There are two possible notification signals:
the mail alert panel and the system beep. The {htype}`mail_notification`
structure looks like this:

:::{code} c
typedef struct
{
   bool alert;
   bool beep;
} mail_notification;
:::

get_mail_notification() always returns {cpp:enumerator}`B_OK`. If the
current settings can't be checked (for example, if the user has never
configured mail), {hparam}`alert` will be returned as the default value of
{cpp:expr}`false`, and {hparam}`beep` will be {cpp:expr}`true`.

set_mail_notification() accepts a pointer to a {htype}`mail_notification`
structure and configures the system to report incoming mail using the
methods specified therein. If the {hparam}`save` argument is
{cpp:expr}`true`, the change is set as the new default and will be
remembered when the computer is shut down. If {cpp:expr}`false`, the change
is temporary.

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-
	- Return Code

	- Description

-
	- {cpp:enumerator}`B_OK`
	- The notification was successfully set or retrieved.
-
	- {cpp:enumerator}`B_NO_REPLY`
	- The mail daemon didn't respond to the request.

:::

## get_pop_account(), set_pop_account(), mail_pop_account



















Get and set the specified POP account's information. The
{htype}`mail_pop_account` structure is defined as follows:

:::{code} c
typedef struct
{
   char pop_name[B_MAX_USER_NAME_LENGTH];
   char pop_password[B_MAX_USER_NAME_LENGTH];
   char pop_host[B_MAX_HOST_NAME_LENGTH];
   char real_name[128];
   char reply_to[128];
   int32 days;
   int32 interval;
   int32 begin_time;
   int32 end_time;
} mail_pop_account;
:::

The {hparam}`pop_name`, {hparam}`pop_password`, and {hparam}`pop_host`
fields in the {htype}`mail_pop_account` structure represent the username,
password, and POP server host of the e-mail user. The {hparam}`real_name`
is the user's real name, and {hparam}`reply_to` is the e-mail address to
which replies should be sent.

The {hparam}`days` field can contain any of the following flags to specify
which days of the week the mail daemon should automatically check mail for
the described account:

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
	- {cpp:enumerator}`B_CHECK_NEVER`
	- Don't automatically check the account's mail.
-
	- {cpp:enumerator}`B_CHECK_WEEKDAYS`
	- Check the mail only on weekdays.
-
	- {cpp:enumerator}`B_CHECK_DAILY`
	- Check the mail every day.
-
	- {cpp:enumerator}`B_CHECK_CONTINUOUSLY`
	- Check continuously every day.

:::

The {hparam}`interval` specifies how many seconds apart each e-mail
retrieval should be, and the {hparam}`begin_time` and {hparam}`end_time`
specify the time of day (in seconds) that automatic retrieval should begin
and end. If {hparam}`begin_time` and {hparam}`end_time` are the same, the
daemon checks mail round-the-clock.

:::{admonition} Note
:class: note
Eventually these functions will support multiple POP accounts; at this
time, the Mail Kit only supports one POP account, so you must use an
{hparam}`index` of 0. Any other {hparam}`index` will result in a
{cpp:enumerator}`B_BAD_INDEX` error.
:::

get_pop_account() fills the specified {htype}`mail_pop_account` structure
with the information on the POP account, and set_pop_account() takes the
information in the buffer and saves it as the new default.

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-
	- Return Code

	- Description

-
	- {cpp:enumerator}`B_OK`
	- The notification was successfully set or retrieved.
-
	- {cpp:enumerator}`B_BAD_INDEX`
	- An {hparam}`index` other than 0 was specified.
-
	- {cpp:enumerator}`B_NO_REPLY`
	- The mail daemon didn't reply to the request.

:::

## get_smtp_host(), set_smtp_host()









get_smtp_host() returns in the buffer pointed to by {hparam}`smtp_host`
the name of the SMTP host as currently configured. The buffer should be at
lest {cpp:enumerator}`B_MAX_HOST_NAME_LENGTH` bytes long.

set_smtp_host() sets the SMTP host through which mail will be sent in the
future to the specified host. If {hparam}`save` is {cpp:expr}`true`, the
new setting becomes the default and will persist through a reboot of the
computer; otherwise, the change is only temporary.

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-
	- Return Code

	- Description

-
	- {cpp:enumerator}`B_OK`
	- The notification was successfully set or retrieved.
-
	- {cpp:enumerator}`B_NO_REPLY`
	- The mail daemon didn't respond to the request.

:::

## send_queued_mail()





Tells the mail daemon to send all pending outgoing mail.

:::{list-table}
---
header-rows: 1
align: left
widths: auto
---
-
	- Return Code

	- Description

-
	- {cpp:enumerator}`B_OK`
	- Mail transfer intitiated successfully.
-
	- Other Errors
	- From {cpp:func}`BMessenger::SendMessage`

:::
