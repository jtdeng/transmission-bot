# Introduction
transmission-bot is an python powered XMPP(jabber) bot which works as a proxy 
between transmission daemon and your XMPP enabled IM, so that you can control 
your transmission bittorrent server using any XMPP client such as Google Talk 
or Pidgin.
A typical use case is that you want to control your transmission daemon running
on your DD-WRT router but you can not access your router directly from internet.


# Install
transmission-bot requires the following python libraries, you can install them
with pip or easy_install
	$ sudo pip install transmissionrpc
	$ sudo pip install dnspython
	$ sudo pip install sleekxmpp


# Functionality
* Show all supported commands
	$help

* Get the status of all downloads
	$status

* Add a new download
	$add url http://www.btdownload.net/file.torrent
	$add base64 <base64 string of torrent file>

* Start or stop one or more downloads
	$start <ids> | all 
	$stop <ids> | all

* Remove one or more downloads (delete torrent only or delete data)
	$remove  [ <ids> | all ]  [ torrent | data ]


# Issues
* Can not send torrent files using IM file transfer due to SleekXMPP limitation
https://groups.google.com/forum/?fromgroups=#!msg/sleekxmpp-discussion/e-9wEwic2gk/GFO9edQYj4AJ

Workaround is to use base64 string of the torrent file