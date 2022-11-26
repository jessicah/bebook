+------------------------------------+---------------------------------------+
| Constant                           | Description                           |
+====================================+=======================================+
| :cpp:enum:`B_INPUT_METHOD_STARTED` | Tells your view that a new inputn     |
|                                    | has begun. Inside the message is a    |
|                                    | :cpp:class:`BMessenger` named be:rept |
|                                    | you should store this because it's y  |
|                                    | way of talking to the input method we |
|                                    | transaction is going on               |
+------------------------------------+---------------------------------------+
| :cpp:enum:`B_INPUT_METHOD_STOPPED` | Lets you know he transaction is over; |
|                                    | should discard the :cpp:class:`BMesse |
|                                    | this point because it's gone stale.   |
+------------------------------------+---------------------------------------+
