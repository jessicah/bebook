.. The Be Book documentation master file, created by
   sphinx-quickstart on Sat Aug 28 08:17:00 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to the Haiku Book
=========================

Below you will find documentation on the Application Programming Interface (API)
of the `Haiku <https://www.haiku-os.org>`_ operating system. This API describes
the internals of the operating system, allowing developers to write native C++
applications and device drivers. See the `online
version <https://api.haiku-os.org/>`_ for the most updated version of this
document. If you would like to help contributing to the documentation effort,
contact the `documentation mailing list <https://www.freelists.org/list/haiku-doc>`_. For guidance on how to help
document the API, see the `Documenting the API <>`_ page. A list of contributors
can be found in the `Credits <https://www.haiku-os.org/docs/api/credits.html>`_. Documenting the API is an ongoing process, so
contributions are greatly appreciated.

The Haiku API is based on the BeOS R5 API, but changes and additions have been
included where appropriate. Important compatibility differences are detailed on
the `Application Level API Incompatibilities with BeOS <https://www.haiku-os.org/docs/api/compatibility.html>`_ page. New classes and
methods and incompatible API changes to the BeOS R5 API are noted in the
appropriate sections.

Kits and Servers
================

The API is split into several kits and servers, each detailing a different
aspect of the operating system.

* The :doc:`Application Kit</kits/application/index>` is the starting
  point for developing applications and includes classes for messaging and for
  interacting with the rest of the system.
* The :doc:`Device Kit</kits/device/overview>` ???
* The :doc:`Game Kit</kits/game/introduction>` provides classes for producing
  game sounds and working with full screen apps.
* The :doc:`Input Server</kits/input/overview>`
* The :doc:`Interface Kit</kits/interface/introduction>` is used to create responsive and attractive graphical
  user interfaces, building on the messaging facilities provided by the
  Application Kit.

  * The :doc:`Layout API</kits/interface/layout>` is a new addition to the
    Interface Kit, in which Haiku provides resources to layout your application
    flexibly and easily.
* The :doc:`Kernel Kit</kits/kernel/overview>` ???
* The :doc:`Locale Kit</kits/locale/overview>` includes classes to localize
  your application to different languages, timezones, number formatting
  conventions and much more.
* The :doc:`Mail Kit</kits/mail/overview>` includes classes to work with e-mail
  files, folders, protocols, and filters as part of Haiku's unique mail handling
  system.
* The :doc:`Media Kit</kits/media/overview>` provides a unified and consistent
  interface for media streams and applications to intercommunicate.
* The :doc:`MIDI 2Kit </kits/midi2/overview>` describes an interface to
  generating, processing, and playing music in MIDI format. For reference
  documentation on the old MIDI Kit (libmidi.so) is also included.
* The :doc:`Network Kit</kits/network/overview>` handles everything network
  related, from interface IP address settings to HTTP connections.
* The :doc:`OpenGL Kit</kits/opengl/overview>`
* The :doc:`Storage Kit</kits/storage/overview>` is a collection of classes
  that deal with storing and retrieving information from disk.
* The :doc:`Support Kit</kits/support/overview>` contains support classes to
  use in your application including resources for thread safety, IO, and
  serialization.
* The :doc:`Translation Kit</kits/translation/overview>` provides a framework
  for converting data streams between media formats.

* :doc:`Classes And Methods </classes_and_methods>`

  * :doc:`The Application Kit </kits/application/index>`
  * :doc:`The Device Kit </kits/device/index>`
  * :doc:`The Game Kit </kits/game/index>`
  * :doc:`The Input Server </kits/input/index>`
  * :doc:`The Interface Kit </kits/interface/index>`
  * :doc:`The Kernel Kit </kits/kernel/index>`
  * :doc:`The Mail Kit </kits/mail/index>`
  * :doc:`The Network Kit </kits/network/index>`
  * :doc:`The OpenGL Kit </kits/opengl/index>`
  * :doc:`The Storage Kit </kits/storage/index>`
  * :doc:`The Support Kit </kits/support/index>`
  * :doc:`The Translation Kit </kits/translation/index>`

Special Topics
==============

* :doc:`C, POSIX, GNU and BSD functions</libroot/introduction>`
* :doc:`Device Drivers </topics/device_drivers>`
* :doc:`Drivers</topic/drivers>`
* :doc:`The Deskbar </topics/deskbar>`
* :doc:`Keyboard</topic/keyboard>`
* :doc:`The Tracker </topics/tracker>`
* :doc:`JSON Handling</topic/json>`
* :doc:`Experimental Network Services Support</kits/netapi/introduction>`

* :doc:`Appendices </appendices>`

  * :doc:`About This Book </about>`
  * :doc:`Revision History </history>`

* :doc:`Class Index </classes_and_methods/classes>`
* :doc:`Function Index </classes_and_methods/functions>`
* :doc:`Constant Index </classes_and_methods/constants>`
* :doc:`Type Index </classes_and_methods/types>`

* :ref:`search`

Acknowledgements
================

We want to express out gratitude to ACCESS Co. for showing their support for the
Haiku Project by allowing the distribution and modification of the Be Book and
the Be Newsletters. The Haiku Book is the successor of the Be Book, updated
with additional APIs and the refresh of existing API documentation.

Not only do the Be Book and the Be Newsletters hold historical value, but these
documents are also a very valuable reference resource for all Haiku developers.
We also want to thank Simon Kennedy for his work on formatting these documents.

* :doc:`Legal Notice </legal>`
* :doc:`Introduction </introduction>`

Indices and tables
==================

.. toctree::
   :glob:

   kits/**/*
   topic/*
   *

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
