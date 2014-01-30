Installing torcollect
=====================

A torcollect setup consists of two parts. The servers that run tor and the machine that
torcollect runs on:

    +--------------------+ 1     N +------------+
    | torcollect-machine |---------| tor server |
    +--------------------+         +------------+

Making a torserver ready for use with torcollect:
-------------------------------------------------

* Create a user for torcollect on the tor-machines that you want to draw statistics from.
* Give this user the rights to read from /var/lib/tor. Preferably you put him in the same
  group as the tor-user himself.
* Create a folder /var/lib/torcollect and chown it to the user torcollect.
* Make the script /clone_stats/ available to the tor-user. For example by copying it to
* /usr/local/bin/ and chmodding it to 755.
* Create a cronjob that executes /clone_stats/ every 24 hours.
* clone_stats ist going to copy the bridge stats into a safe environment so that you don't
  have to fiddle around on permissions with tor-relevant folders.
* Generate a SSH-keypair for the torcollect user and keep the publickey file ready when
  wanting register the server with torcollect.

Setting up a torcollect server:
-------------------------------

* Create a user torcollect on the machine.
* Make sure the dependencies are installed (paramiko, pgdb).
* Move the folder torcollect to /usr/local/lib/python2.7/dist-packages/
* Move the file bin/torcollect to /usr/local/bin/
* Chmod /usr/local/bin/torcollect to 755
* Set up a postgres database for the user torcollect using *database.sql*.
* One should only be able to connect to it from localhost by now.
* The name of the database should be "torcollect"
* The password of the database should be "test" by now.

* install python-pip (apt-get install python-pip)
* install pygal via pip (pip install pygal)
* make the following changes to the config.py in /usr/local/lib/python2.7/dist-packages/pygal/config.py:
  substitute the adresses "http://kozea.github.com/pygal.js/javascripts/pygal-tooltips.js" and
  "http://kozea.github.com/pygal.js/javascripts/svg.jquery.js" so that the files are searched on your
  own webserver. For example "http://mytorcollect.server.tld/pygal-tooltips.js" and respectively
  "http://mytorcollect.server.tld/svg.jquery.js". This prevents external services from knowing who
  uses torcollect at which time and is thus necessary to support our users' privacy.
* go to the documentroot of your webserver and wget
  http://kozea.github.com/pygal.js/javascripts/pygal-tooltips.js
  and http://kozea.github.com/pygal.js/javascripts/svg.jquery.js

* You can now fiddle around with the new command *torcollect* that you should be
able to execute in the console.
* You'll find there documented the command torcollect server add. Use this command
on every server you prepared in the step "Making a torserver ready for use with torcollect"
* Install a webserver of your choice.
* Copy the contents of web/ to the documentroot of your webserver
* make sure the torcollect user is allowed to write on your webservers documentroot 
* Check if the correct paths are in /usr/local/lib/python2.7/dist-packages/torcollect/paths.py
* You should now be able to execute the commands *torcollect collect* and *torcollect generate*
* There are the two commands that do the routinely work. The first one acquires information from
  the entered server whereas the latter one generates HTML reports.
* To finalize the setup, create two cronjobs that execute *torcollect collect* and *torcollect generate* on a regular basis
