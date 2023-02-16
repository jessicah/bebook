# Message Constants

## B_ACQUIRE_OVERLAY_LOCK, B_RELEASE_OVERLAY_LOCK

:::{list-table}
---
header-rows: 0
align: left
widths: auto
---
-
	- Purpose:

	- Deliverable

-
	- Source:

	- A graphics driver.

-
	- Target:

	- The team owning the overlay.


:::

{cpp:enumerator}`B_ACQUIRE_OVERLAY_LOCK` is sent by a graphics driver when
an overlay is acquired. {cpp:enumerator}`B_RELEASE_OVERLAY_LOCK` is sent
when the overlay is released.
