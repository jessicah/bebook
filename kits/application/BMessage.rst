.. cpp:class::	BMessage

BMessage
========

.. highlight:: cpp

Data Members
------------

.. cpp:member:: what:

	public uint32 what;

A coded constant that captures what the message is about.

Constructor and Destructor
--------------------------

:cpp:func:`BMessage()`::

	BMessage(uint32 command);
	BMessage(const BMessage& message);
	BMessage();

Creates a new :cpp:class:`BMessage` object that has the given
:cpp:expr:`command` constant, or that's a copy of another :cpp:class:`BMessage`.
If it's a copy, the new object contains the same command constant and data
fields as :cpp:expr:`message`.

See also: :cpp:func:`BLooper::DetachCurrentMessage()`

:cpp:func:`~~BMessage()`::

	virtual ~BMessage();

Frees all memory allocated to hold message data. If the message sender is
expecting a reply but hasn't received one, a default reply (with
:cpp:enum:`B_NO_REPLY` as the :cpp:member:`what` data member) is sent before the
message is destroyed.

The system retains ownership of the messages it delivers to you. Each message
loop routinely deletes delivered :cpp:class:`BMessage` s after the application
is finished responding to them.

Member Functions
----------------

.. cpp:functions:: AddData(); AddBool(); AddInt8(); 

:cpp:func:`AddData(), AddBool(), AddInt8(), AddInt16(), AddInt32(), AddInt64(),
AddFloat(), AddDouble(), AddString(), AddPoint(), AddRect(), AddRef(),
AddMessage(), AddMessenger(), AddPointer(), AddFlat()`::

	status_t AddData(const char* name,
	                 type_code type,
	                 const void* data,
	                 ssize_t numBytes,
	                 bool fixedSize = true,
	                 int32 numItems = 1);

::

	status_t AddBool(const char* name,
	                 bool aBool);

::

	status_t AddInt8(const char* name,
	                 int8 anInt8);

These functions add data to the field named :cpp:expr:`name` and assign a data
type to the field. Field names can be no longer than 255 characters. If more
than one item of data is added under the same name, the :cpp:class:`BMessage`
creates an array of data for that name. Each time you add another value (to the
same name), the value is added to the end of the array--you can't add a value at
a specific index. A given field can only store one type of data.

:cpp:func:`AddData()` copies :cpp:expr:`numBytes` of :cpp:expr:`data` into the
field, and assigns the data a :cpp:expr:`type` code. It copies whatever the
:cpp:expr:`data` pointer points to. For example, if you want to add a string of
characters to the message, :cpp:expr:`data` should be the string pointer
(:cpp:expr:`char \*`). If you want to add only the string pointer, not the
characters themselves, :cpp:expr:`data` should be a pointer to the pointer
(:cpp:expr:`char \*\*`). The assigned :cpp:expr:`type` must be a specific data
type; it should not be :cpp:enum:`B_ANY_TYPE`.
