---
title: The Application Kit
---

# Introduction

The Application Kit is the starting point for all applications. Its classes establish an application
as an identifiable entity, one that can cooperate and communicate with other applications.

The Application Kit is divided into these topics:

{cpp:class}`BApplication`.
	All but the simplest of applications must have one (and only one) {cpp:class}`BApplication`
	object. This object is typically an instance of a {cpp:class}`BApplication` subclass that you
	create especially for your application. The {cpp:class}`BApplication` object makes a connection
	to the App Server and runs the application's main message loop.

[](./messaging.rst).
	The kit provides a messaging service that lets threads talk to each other. This service can
	deliver messages within your own application, or from one application to another. It's also used
	by the system to deliver user event messages (key clicks, mouse moves) to your application. Most
	of the Application Kit's classes are involved in the messaging system.

[](./scripting.md).
	The objects that you create can be controlled by commands issued from other applications.

{cpp:class}`BRoster`.
	The {cpp:class}`BRoster` object keeps track of all running applications. It can identify
	applications, launch them, and provide the information needed to set up communications with
	them.

{cpp:class}`BClipboard`.
	The {cpp:class}`BClipboard` object provides an interface to the clipboard where cut and copied
	data can be stored, and from which it can be pasted.

{cpp:class}`BCursor`.
	You use {cpp:class}`BCursor` objects to represent distinct cursors. Functions defined by
	{cpp:class}`BApplication` and {cpp:class}`BView` let you assign your cursors to your entire
	application, or to individual views.
