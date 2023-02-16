# BInvoker

{cpp:class}`BInvoker` is a convenience class that bundles up everything
you need to create a handy message-sending package.

The {cpp:class}`BInvoker` contains:

-   a {cpp:class}`BMessage`

-   a {cpp:class}`BMessenger` (that identifies a target handler), and

-   an optional {cpp:class}`BHandler` that handles replies.

You set these ingredients, invoke {cpp:func}`Invoke() <BInvoker::Invoke>`,
and off goes the message to the target. Replies are sent to the reply
handler ({hparam}`be_app` by default).

{cpp:class}`BInvoker` uses {cpp:func}`BMessenger::SendMessage` to send its
messages. The invocation is asynchronous, and there's no time limit on the
reply.

{cpp:class}`BInvoker` is mostly used as a mix-in class. A number of
classes in the {ref}`Interface Kit` notably {cpp:class}`BControl` derive
from {cpp:class}`BInvoker`.
