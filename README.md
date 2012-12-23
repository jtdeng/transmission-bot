# transmission-bot

transmission-bot is an python powered XMPP bot which works as an agent 
between transmission daemon and your XMPP enabled IM, so that you can control 
your transmission bittorrent server using any XMPP client such as Google Talk 
or Pidgin.
A typical use case is that you want to control your transmission daemon running
on your DD-WRT router from your mobile phone.


## Installation
transmission-bot requires the following python libraries, you can install them
with pip or easy_install

    $ sudo pip install transmissionrpc
    $ sudo pip install dnspython
    $ sudo pip install sleekxmpp
    $ sudo pip install feedparser

If you run transmission-bot on DD-WRT with opkg installed, you need to install
the following packages before installing sleekxmpp

    $ opkg install python-expat
    $ opkg install python-openssl
    $ opkg install pyopenssl

## Configuration
* Static configuration is saved in settings.py, each parameter is described there.
* Dynamic configuration is saved in dynamic.json, which is created on first 
startup.


## Functions
* Show usage of all supported commands or the one specified
    ```
    $help [command]
    ```

* Show the status of all downloads
    ```
    $status
    ```

* Add a new download by url or base64 of torrent file
    ```
    $add url http://www.btdownload.net/file.torrent
    $add url magnet:?xt=urn:btih:E1F86D6127D705871A8053533BD4B55776FD31E5...
    $add base64 '<base64 string of torrent file>'
    ```

* Start or stop one or more downloads by comma separated ids
    ```
    $start <ids>|all
    $stop <ids>|all
    ```

* Remove one or more downloads (delete torrent only or delete data)
    ```
    $remove <ids>|all
    $remove <ids>|all data
    ```

* Turn on/off notification on completion or feed updates
    ```
    $notify
    $notify [on|off]
    ```

* Automatic stop torrent when 100% downloaded
    ```
    $autostop
    $autostop [on|off]
    ```

* Torrent discovery using feed like rss, atom etc 
    ```
    $feed list
    $feed subscribe <feed_url>
    $feed unsubscribe <ids>|all
    $feed enable|disable <ids>|all
    ```

* Manage item queue discovered from subscribed feeds
    ```
    $queue list             
    $queue download <ids>|all 
    $queue remove <ids>|all   
    ```

* Dump or load dynamic configuration 
    ```
    $config dump
    $config load '<json_string>'
    ```

## Issues
Can not send torrent files using IM file transfer due to [SleekXMPP limitation](https://groups.google.com/forum/?fromgroups=#!msg/sleekxmpp-discussion/e-9wEwic2gk/GFO9edQYj4AJ), workaround is to use base64 string of the torrent file
