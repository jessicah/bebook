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

* The :doc:`Application Kit</kits/application/introduction>` is the starting
  point for developing applications and includes classes for messaging and for
  interacting with the rest of the system.
* The :doc:`Game Kit</kits/game/introduction>` provides classes for producing
  game sounds and working with full screen apps.
* The :doc:`Interface Kit</kits/interface/introduction>` is used to create responsive and attractive graphical
  user interfaces, building on the messaging facilities provided by the
  Application Kit.

  * The :doc:`Layout API</kits/interface/layout>` is a new addition to the
    Interface Kit, in which Haiku provides resources to layout your application
    flexibly and easily.

Special Topics
==============

* :doc:`C, POSIX, GNU and BSD functions</libroot/introduction>`
* :doc:`Drivers</topic/drivers>`
* :doc:`Keyboard</topic/keyboard>`
* :doc:`JSON Handling</topic/json>`
* :doc:`Experimental Network Services Support</kits/netapi/introduction>`

Acknowledgements
================

We want to express out gratitude to ACCESS Co. for showing their support for the
Haiku Project by allowing the distribution and modification of the Be Book and
the Be Newsletters. The Haiku Book is the successor of the Be Book, updated
with additional APIs and the refresh of existing API documentation.

Not only do the Be Book and the Be Newsletters hold historical value, but these
documents are also a very valuable reference resource for all Haiku developers.
We also want to thank Simon Kennedy for his work on formatting these documents.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
