# BQuery

A query is a means of asking the file system for a set of entries that
satisfy certain criteria. As examples, you can ask for all the entries with
names that start with a certain letter, or that have nodes that are bigger
than a certain size, or that were modified within the last N days, and so
on.

The {hclass}`BQuery` class lets you create objects that represent specific
queries. To use a {hclass}`BQuery` you have to follow these steps:

1.    Initialize.   The first thing you have to do is initialize the object;
there are two parts to the initialization: You have to set the volume that
you want to query over ({cpp:func}`SetVolume() <BQuery::SetVolume>`), and
set the query's "criteria formula" ({cpp:func}`SetPredicate()
<BQuery::SetPredicate>`)

2.    Fetch.   After the {hclass}`BQuery` has been properly initialized, you
invoke {cpp:func}`Fetch() <BQuery::Fetch>`. The function returns
immediately while the query executes in the background.

3.    Read.   As soon as {cpp:func}`Fetch() <BQuery::Fetch>` returns, you can
start reading the list of winning entries by making iterative calls to the
entry-list functions {cpp:func}`GetNextRef() <BQuery::GetNextRef>`,
{cpp:func}`GetNextEntry() <BQuery::GetNextEntry>`, and
{cpp:func}`GetNextDirents() <BQuery::GetNextDirents>`. If you ask for
entries faster than the query can deliver them, your {hmethod}`GetNext…()`
call will block until the next entry arrives. The function returns an error
when there are no more entries to retrieve.

The set of entries that the {hmethod}`GetNext…()` calls retrieve (for a
given fetch) are called the query's "static" entries. This distinction will
become useful when we speak of "live" queries, below.

## Reusing your BQuery

Want to go around again? You can, but first you have to clear the object:

-   Between each "fetching session," you have to invoke {cpp:func}`Clear()
<BQuery::Clear>` on your {hclass}`BQuery` object.

Clearing erases the object's predicate, volume, target (which we'll get to
later), and list of static entries—in other words, clearing gets you back
to a fresh {hclass}`BQuery` object.

And speaking of going around again, be aware that the {cpp:func}`Rewind()
<BQuery::Rewind>` function, which {hclass}`BQuery` inherits from
{cpp:class}`BEntryList`, is implemented to be a no-op: You can't rewind a
{hclass}`BQuery`'s list of static entries. After you've performed a fetch,
you should read the entry list as quickly as possible and get on with
things; you can't turn back or start over.

{cpp:func}`CountEntries() <BQuery::CountEntries>` is also a no-op. This
function is also defined by {cpp:class}`BEntryList`. It doesn't apply to
{hclass}`BQuery`s.

## Live Queries

A live query is the gift that keeps on giving. After you tell a live query
to fetch, you walk through the entry list (as described above), and then
you wait for "query update" messages to be sent to your "target." A query
update message describes a single entry that has changed so that…

-   it now satisfies the predicate (where it didn't use to), or…

-   it no longer satisfies the predicate (where it did before).

Not every {hclass}`BQuery` is live; you have to tell it you want it to be
live. To do this, all you have to do is set the object's target, through
the {cpp:func}`SetTarget() <BQuery::SetTarget>` function. The target is a
{cpp:class}`BMessenger` that identifies a
{cpp:class}`BHandler`/{cpp:class}`BLooper` pair (as described in the
{cpp:func}`SetTarget() <BQuery::SetTarget>` function). Also…

-   Live query notifications stop when you {cpp:func}`Clear() <BQuery::Clear>`
or destroy the {hclass}`BQuery` object.

Another important point regarding live queries is that you can start
receiving updates before you're done looking at all the static entries (in
other words, before you've reached the end of the {hmethod}`GetNext…()`
loop). It's possible that your target could receive an "entry dropped out"
update before you retrieve the entry through a {hmethod}`GetNext…()` call.
If you're using live queries, you should take care in synchronizing the
{hmethod}`GetNext…()` iteration with the target's message processing.

We'll look at the format of the update message in a moment; first, let's
fill in some gaps.

## The Predicate, Attributes, and Indices

A {hclass}`BQuery`'s predicate is a logical expression that evaluates to
{cpp:expr}`true` or {cpp:expr}`false`. The "atoms" of the expression are
comparisons in the form…

-   __attribute op value__

…where __attribute__ is the name of an existing attribute, __op__ is a
constant that represents a comparison operation (==, <, >, etc), and
__value__ is the value that you want to compare the attribute to.

## Attributes

As mentioned above, the attribute part of a query is a string name. When
you tell the query to fetch, the file system looks for all nodes that have
an attribute with that name and then compare the attribute's value to the
appropriate value in the predicate. However…

-   Every query must include at least one indexed attribute.

-   The index only knows about attributes that were written after the index
(for that attribute) was created.

To index an attribute, you call the {ref}`fs_create_index()` function.
Unfortunately, there's currently no way to retroactively include existing
attributes in a newly created index. (Such a utility would be simple enough
to write, but it would take a long time to execute since it would have to
look at every file in the file system.)

Only string and numeric attributes can be queried. Although an attribute
can hold any type of data (it's stored as raw bytes), the query mechanism
can only perform string and numeric comparisons.

On the bright side, every file gets three attributes for free:

-   "name" is the name of the entry.

-   "size" is the size of the data portion of the entry's node. The size is a
64-bit integer, and doesn't include the node's attributes.

-   "last_modified" is the time the entry's node was last modified (data and
attributes), measured in seconds since January 1, 1970. The modification
time is recorded as a 32-bit integer.

Technically, "name", "size", and "last_modified" aren't actually
attributes—you can't get them through {cpp:func}`BNode::ReadAttr`, for
example. But they're always eligible as the attribute component in a query.

## Values

The value part of the "attribute op value" equation is any expression that
can be evaluated at the time the predicate is set. Once evaluated, the
value doesn't change. For example, you can't specify another attribute as
the value component in hopes of comparing, file by file, the value of one
attribute to the value of another. The value is just data. And data is
data.

The type of the value should match the type of the attribute: You compare
string attributes to strings; numeric attributes to numbers. You aren't
prevented from comparing a string to a number (for example), but it may not
give you the result you expect.

:::{admonition} Warning
:class: warning
The value of an indexed attribute can be, at most, 255 bytes.
:::

## Constructing a Predicate

There are two ways to construct a predicate:

-   You can set the predicate formula as a string through
{cpp:func}`SetPredicate() <BQuery::SetPredicate>`, or

-   You can construct the predicate by "pushing" the components in Reverse
Polish Notation (or "postfix") order through the {cpp:func}`PushAttr()
<BQuery::PushAttr>`, {hmethod}`PushValue…()`, and {cpp:func}`PushOp()
<BQuery::PushOp>` functions. There are seven value-pushing functions that
push specific types: {htype}`string`, {htype}`int32`, {htype}`uint32`,
{htype}`int64`, {htype}`uint64`, {htype}`float`, and {htype}`double`.

You can't combine the methods: Pushing the predicate always takes
precedence over {cpp:func}`SetPredicate() <BQuery::SetPredicate>`,
regardless of the order in which the methods are deployed.

{cpp:func}`SetPredicate() <BQuery::SetPredicate>` features:

-   Comparison operators: = < > <= >= !=

-   Logical operators: || &&

-   Negation operator: !

-   Grouping: ()

-   String (value) wildcard: * (prefix and/or postfix only)

-   String (value) quoting: ' '

The following are all legitimate strings that you can pass to
{cpp:func}`SetPredicate() <BQuery::SetPredicate>`:

:::{code} sh
size < 500

(name = fido) || (size >= 500)

(! ((name = *id*) || ( 'final utterance' = 'pass the salt'))) &&
(last_modified > 1024563)
:::

Push features:

-   The {cpp:func}`PushOp() <BQuery::PushOp>` function takes operator symbols,
such as {cpp:enumerator}`B_EQ` (equals), {cpp:enumerator}`B_GT` (greater
than), {cpp:enumerator}`B_LT` (less than), and so on. The complete list is
given in the {cpp:func}`PushOp() <BQuery::PushOp>` function description.

-   Value strings passed as arguments to {cpp:func}`PushString()
<BQuery::PushString>` are naturally quoted, so you don't have to
single-quote to embed spaces or other odd characters.

-   The '*' wildcard is allowed, or you can use special "contains", "begins
with", and "ends with" operators.

In Reverse Polish Notation, the operator is postfixed. You then push the
components from left to right. For example, this…

:::{code} sh
size < 500
:::

…becomes…

:::{code} sh
size 500 <
:::

The push sequence is…

:::{code} cpp
query.PushAttr("size");
query.PushInt32(500);
query.PushOp(B_LT);
:::

Another example; this…

:::{code} sh
(name = fido) || (size >= 500)
:::

...becomes...

:::{code} sh
(name fido =) (size 500 >=) ||
:::

In code:

:::{code} cpp
query.PushAttr("name");
query.PushString("fido");
query.PushOp(B_EQ);
query.PushAttr("size");
query.PushInt32(500);
query.PushOp(B_GE);
query.PushOp(B_OR);
:::

There are no grouping operators in this notation; they're not
needed—grouping is implied by the order in which the components are pushed.

When you're performing a numeric comparison, the {hmethod}`Push…()`
function that you choose doesn't have to exactly match the natural type of
the attribute, but you can't mix integers and floating point. For example,
even though "size" is a 64 bit value, you can compare it to an
{htype}`int32`…

:::{code} cpp
query.PushAttr("size");
query.PushInt32(2000);
query.PushOp(B_GE);
:::

But you can't (or shouldn't) compare it to a {htype}`float`…

:::{code} cpp
query.PushAttr("size");
query.PushInt32(2000);
query.PushOp(B_GE);
:::

## Query Update Messages

The {cpp:class}`BMessages` that are delivered by a live query have a
{hparam}`what` field of {cpp:enumerator}`B_QUERY_UPDATE`. The rest of the
message depends on what happened:

-   If the update is telling you that an entry has passed the predicate, the
message's {hparam}`opcode` field will be {cpp:enumerator}`B_ENTRY_CREATED`.

-   If the update is telling you that an entry has been eliminated from the
query, the {hparam}`opcode` field will be
{cpp:enumerator}`B_ENTRY_REMOVED`.

Note that the format of the messages that a live query generates are the
same as the similarly-opcode'd Node Monitor messages. The only difference
is the {hparam}`what` field (the what for Node Monitor messages is
{cpp:enumerator}`B_NODE_MONITOR`).

## Entry Created

The {cpp:enumerator}`B_ENTRY_CREATED` opcode means an entry has changed so
that it now passes the query's predicate. The message's fields are:

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
	- {hparam}`opcode`

	- {cpp:enumerator}`B_INT32_TYPE`

	- {cpp:enumerator}`B_ENTRY_CREATED`

-
	- {hparam}`name`

	- {cpp:enumerator}`B_STRING_TYPE`

	- The name of the new entry.

-
	- {hparam}`directory`

	- {cpp:enumerator}`B_INT64_TYPE`

	- The {htype}`ino_t` (node) number for the directory in which the entry was
created.

-
	- {hparam}`device`

	- {cpp:enumerator}`B_INT32_TYPE`

	- The {htype}`dev_t` number of the device on which the new entry resides.

-
	- {hparam}`node`

	- {cpp:enumerator}`B_INT64_TYPE`

	- The {htype}`ino_t` number of the new entry itself. (More accurately, it
identifies the node that corresponds to the entry.)


:::

If you want to cache a reference to the entry, notice that you can create
an {htype}`entry_ref` and a {htype}`node_ref` with the data in the
message's fields:

:::{code} cpp
/* Create an entry_ref */
entry_ref ref;
const char* name;
...
msg->FindInt32("device", &ref.device);
msg->FindInt64("directory", &ref.directory);
msg->FindString("name", &name);
ref.set_name(name);

/* Create a node_ref */
node_ref nref;
status_t err;

...
msg->FindInt32("device", &nref.device);
msg->FindInt64("node", &nref.node);
:::

The {htype}`node_ref` is handy because you may want to start monitoring
the node (through a call to the Node Monitor). We'll get back to this point
when discussing {cpp:enumerator}`B_ENTRY_REMOVED` messages.

## Entry Removed

The {cpp:enumerator}`B_ENTRY_REMOVED` opcode means an entry used to pass
the predicate, but something has changed (in the entry or the entry's node)
so that now it doesn't.

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
	- {hparam}`opcode`

	- {cpp:enumerator}`B_INT32_TYPE`

	- {cpp:enumerator}`B_ENTRY_REMOVED`

-
	- {hparam}`directory`

	- {cpp:enumerator}`B_INT64_TYPE`

	- The {htype}`ino_t` (node) number of the directory from which the entry was
removed.

-
	- {hparam}`device`

	- {cpp:enumerator}`B_INT32_TYPE`

	- The {htype}`dev_t` number of the device that the removed node used to live
on.

-
	- {hparam}`node`

	- {cpp:enumerator}`B_INT64_TYPE`

	- The {htype}`ino_t` number of the node that was removed.


:::

Notice that the {cpp:enumerator}`B_ENTRY_REMOVED` message doesn't tell you
the name of the entry. This is an unfortunate oversight that will be
corrected. In the meantime, if you need to match the node in this message
to an entry from a previous {cpp:enumerator}`B_ENTRY_CREATED` (or that you
got from a {hmethod}`GetNext…()` invocation), you have to keep track of the
entry/node yourself. However, the location of the entry that "contains" the
node may have changed since the time that the entry passed the predicate.
Follow this outline:

1.    You set up a live query ask for entries that have nodes larger than 500
bytes.

2.    The query mechanism tells you (either in the static set or through a
{cpp:enumerator}`B_ENTRY_CREATED` message) that /boot/home/fido/data
satisfies the predicate.

3.    You create an {htype}`entry_ref` and a {htype}`node_ref` to the entry, and
cache them away somewhere.

4.    The user then renames or moves the entry. The query mechanism doesn't tell
you about this change—it only cares about the size of the node, not its
name

5.    You get a {cpp:enumerator}`B_ENTRY_REMOVED` message. You create a
{htype}`node_ref` from the message and match it to your cache—and get an
out-of-date {htype}`entry_ref`.

To get around the lack of a "name" field, you should monitor the nodes
that you receive in your initial {hmethod}`GetNext…()` calls and
{cpp:enumerator}`B_ENTRY_CREATED` messages.
