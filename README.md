example-poll-backend
====================
This repo stores a minimal backend that works with videogular-questions to store and return poll information.

It is to be used as a guide to the polls API. The backend database and any processing that occurs after receipt, or prior to sending, is an example and can be switched out for whatever other system is required.

API
====================

The server exposes two endpoints, a POST /vote and a GET /results/annotationId/questionId. Additionally some work is done to fix CORS problems that could occur.

The POST endpoint expects a schema similar to the vg-questions webworker:
```
{
  questionResult: questionId,
  annotation: annotationid
  result: ...
}
```

The GET endpoint returns an object of result<->vote-count pairs:
```
{
  optionOne: 5,
  cheese: 2
  last: 3
}
```

Example Setup
====================

Before use you should browse to /setup to allow the server to setup the database


Configuring an Apache webserver to run this application
=======================================================

First deploy this repository to the webserver.

Then the apache httpd.conf file needs to be configured by adding the following entry somewhere in the file:

	<VirtualHost <hostname>:80>
		ServerName <hostname>
		WSGIDaemonProcess poll_server user=<user> group=<group> threads=5
		WSGIScriptAlias / /<location>/poll_server.wsgi
		ErrorLog logs/poll_server-error_log
		CustomLog logs/poll_server-access_log common
	
		<Directory <location>>
			WSGIProcessGroup poll_server
	            WSGIApplicationGroup %{GLOBAL}
	            Order deny,allow
	            Allow from all
		</Directory>
	</VirtualHost>

Parameters needing changes:

* `<hostname>` is the hostname of the server. e.g. hostname.domain.com
* `<location>` is the location of the sourcecode on the server. e.g. /var/www/poll_server/
* `<user>` is the user you want the script to run under, by default apache
* `<group>` is the group you want the script to run under, by default apache
* The `ErrorLog` and `CustomLog` parameters can be changed to any location
