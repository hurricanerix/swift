Sample Middleware
=================

Reference middleware to be used as an example/starting point for OpenStack swift
middleware.  The provided example has been written with the proxy server in mind, but could easily be adapted to work as  account/container/object middleware.

Usage
-----

Here you can provide descriptions and examples of how to use the middleware you authored.

```Shell
$ curl -i -XGET -H"X-Auth-Token: $TOKEN" http://127.0.0.1:8080/v1/AUTH_test/c/o
HTTP/1.1 200 OK
Content-Length: 4
Accept-Ranges: bytes
Last-Modified: Thu, 03 Dec 2015 17:10:38 GMT
Etag: 81dc9bdb52d04dc20036dbd8313ed055
X-Timestamp: 1449162637.16523
Content-Type: application/x-www-form-urlencoded
X-Trans-Id: tx4016a66e26484dd8a4e98-0056607791
Date: Thu, 03 Dec 2015 17:10:41 GMT

1234
```

Configuration
-------------

To install this middleware simply:

```Shell
$ cd $PATH_TO_MIDDLEWARE
$ sudo python setyp.py [install|develop]
```

And don't forget to add it to your pipeline in proxy-server.conf as follows:
TODO: warn about dangers of pipeline ordering

```INI
[pipeline:main]
pipeline = ... tempauth sample ...

[filter:sample]
use = egg:sample_middleware#swift_sample_middleware
key1 = value1
key2 = value2
secretkey1 = secretvalue1
```

Middleware Explained
--------------------

Everything above this section is meant to be a template for the README of your middleware.  When you create your middleware based off of it, you should remove everything from "Middleware Explained" and on, as it here for informational purposes and is not intended to be part of the template.

WSGI
----

In its most basic form, middleware for swift simply implements the [Python Web Server Gateway Interface](https://www.python.org/dev/peps/pep-3333/).

setup.py
--------

When configuring your project's setup.py, each middleware within the project should be added to the entry point's list of paste filter factories.

```Python
entry_points={
    'paste.filter_factory': [
        'swift_sample_middleware=sample.middleware:filter_factory',
    ],
},
```

In the preceding example, "swift_sample_middleware" would be the name used when referencing the middleware from the proxy-server.conf and "sample.middleware:filter_factory" would be the path to the filter factory function in your middleware module.

Pipeline
--------

The pipeline defines the order which middleware is executed.  Middleware on the left hand side wraps middleware on the right hand side.  Each name in the pipeline will use it's corresponding section in the config to determine the code that is loaded.

The config section is named with the convention "[filter:sample]" where "sample" is the name that was added to the pipeline.

The only required key for the middleware is the "use" key which references the middleware to be loaded.  For example "use = egg:sample_middleware#swift_sample_middleware" loads middleware with the name "sample_middleware" from the name key and "swift_sample_middleware" references the corresponding paste.filter_factory entry point, both located in setup.py.

### Pipeline Example

Say you had the following Pipeline

```INI
pipeline = ... sample1 sample2 sampel3 ...
```

When the proxy is started, functions/methods would be executed as follows:

```
sample1 filter_factory
sample2 filter_factory
sample3 filter_factory
sample3 sample_filter
sample3 __init__
sample2 sample_filter
sample2 __init__
sample1 sample_filter
sample1 __init__
```

When the proxy receives a request, the middleware's methods would get executed as follows:

```
sample1 __call__
sample2 __call__
sample3 __call__
sample3 _start_response
sample2 _start_response
sample1 _start_response
```
