BClipboard
==========

A ``BClipboard`` object is an interface to a clipboard, a resource that provides
system-wide, temporary data storage. Clipboards are identified by name; if two
apps want to refer to the same clipboard, they simply create respective
``BClipboard`` objects with the same name::

	/* App A: This creates a clipboard named "MyClipboard". */
	BClipboard *appAclipboard = new BClipboard("MyClipboard");

	/* App B: This object refers to the clipboard already created
	   by App A. */
	BClipboard *appBclipboard = new BClipboard("MyClipboard");

The System Clipboard
====================

In practice, you rarely need to construct your own ``BClipboard`` object;
instead, you use the ``BClipboard`` that's created for you by your
``BApplication`` object. This object, which you refer to through to global
``be_clipboard`` variable, accesses the default system clipboard. Data that you
write to your ``be_clipboard`` object can be read from any other app's
``be_clipboard``. For example, the cut/copy/paste operations defined by
``BTextView`` transfer data through the system clipboard.

.. note::
	To access the system clipboard without creating a ``BApplication`` object,
	construct a ``BClipboard`` object with the name "system". The system
	clipboard is under the control of the user; you should only read or write
	the system clipboard as a direct result of the user's actions. If you create
	your own clipboards, don't name them "system".

The Clipboard Message
=====================

To access a clipboard's data, you call functions on a ``BMessage`` that the
``BClipboard`` object hands you (through its ``Data()`` function). The
``BMessage`` follows these convertions:

* The ``what`` value is unused.
* The data is stored in a message field. The field should be typed as
  :cpp:enum:`B_MIME_TYPE`; the MIME type that describes that data should be used
  as the name of the field that holds the data (see "Writing to the Clipboard" for
  an example).
* If the ``BMessage`` contains more than one field, each field should present
  the same data in a different format. For example, the StyledEdit app writes
  text data in its own format (in order to encode the fonts, colors, etc.) and
  also writes the data as plain ASCII text (MIME type "text/plain").

Writing to the Clipboard
========================

The following annotated example shows how to write to the clipboard::

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

#. ``Lock()`` your ``BClipboard`` object. This uploads data from the clipboard
   into your ``BClipboard``'s local ``BMessage`` object, and prevents other
   threads in your application from accessing the ``BClipboard``s data. Note
   that locking does not lock the underlying clipboard data; other applications
   can change the clipboard while you have your object locked.
#. Prepare the ``BClipboard`` for writing by calling ``Clear()``. This erases
   the data that was uploaded from the clipboard.
#. Call ``Data()`` to get a pointer to the ``BClipboard``s ``BMessage`` object.
#. Write the data by invoking ``AddData()`` directly on the ``BMessage``. In the
   example, we write the data in two different formats.
#. Call ``Commit()`` to copy your ``BMessage`` back to the clipboard. As soon as
   you call ``Commit()``, the data that you added is visible to other clipboard
   clients.
#. ``Unlock()`` balances the ``Lock()``. The ``BClipboard`` object can now be
   accessed by other threads in your application.

If you decide that you don't want to commit your changes, you should call
``Revert()`` before you unlock.

Reading from the Clipboard
==========================

Here we show how to read a simple string from the clipboard::

	const char *text;
	int32 textLen;
	BMessage *clip = (BMessage *)NULL;
	if (be_clipboard->Lock()) {
		if ((clip = be_clipboard->Data())
			clip->FindData("text/plain", B_MIME_TYPE,
				(const void **)text, &textLen);
		
		be_clipboard->Unlock();
	}

#. As in writing, we bracket the operation with ``Lock()`` and ``Unlock()``.
   Keep in mind that ``Lock()`` uploads data from the clipboard into our object.
   Any changes that are made to the clipboard (by some other application) after
   ``Lock()`` is called won't be seen here.
#. In this example, we only look for one hard-coded format. In a real
   application, you may have a list of formats that you can look for.
#. It isn't necessary to examine the clipboard data before you unlock it. The
   ``FindData()`` call could just as well have been performed after the
   ``Unlock()`` call.

Persistence
===========

Inter-boot persistence:
	Clipboard data does not persist between boots; the constructor provides a
	persistence flag but it's currently unused.

Intra-boot persistence:
	Onve you've created a clipboard, that clipboard will exist until you reboot
	your computer. For example, let's say you design an app that creates a
	clipboard called "MyClip": You launch the app, write something to "MyClip",
	and then quit the app. The clipboard and the data that you wrote to it will
	still exist. If you relaunch your app (or any app that knows about
	"MyClip"), you can pick up the data by reading from the "MyClip" cliboard.
