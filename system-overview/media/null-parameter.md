# BNullParameter

The {cpp:class}`BNullParameter` class represents a junction or I/O point
in the parameter web. It doesn't take any value; instead, it's used
primarily to identify special places in the parameter web that need to be
displayed specially by the client application.

Typical uses of {cpp:class}`BNullParameter`s are to identify where signals
enter or leave the node (input and output jacks, ADCs or DACs, and so
forth).
