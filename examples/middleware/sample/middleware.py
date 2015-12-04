# Copyright (c) 2010-2015 OpenStack Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

from swift.common.swob import Request, Response
from swift.common.utils import register_swift_info, split_path, public
from swift.proxy.controllers.base import delay_denial, cors_validation

from sample import name


class SampleMiddleware(object):

    def __init__(self, app, conf):
        self.app = app
        self.conf = conf

    def __call__(self, env, start_response):
        """
        The entry point for your middleware, this gets called with
        every request to Swift.
        """
        req = Request(env)

        # Example of adding a custom path to Swift.
        # Care should be taken when adding custom paths
        # to avoid collisions with existing and future
        # paths.
        if req.method == 'GET' and req.path == '/sample':
            handler = self.GET
            return handler(req)(env, start_response)

        # Example of checking for a headers
        foo = req.headers.get('sample-foo')

        # Example of handling requests to a account,
        # container or object.  We also check to ensure that
        # the request is to the v1 API (currently the only version)
        v, a, c, o = split_path(
            req.path, minsegs=0, maxsegs=4, rest_with_last=True)
        if o and v == 'v1':
            print('request for object: {0} belonging to {1}/{2}'.format(
                  o, a, c))
        elif c and v == 'v1':
            print('request for container: {0} beloning to {1}'.format(c, a))
        elif a and v == 'v1':
            print('request for account: {0}'.format(a))

        def _start_response(status, headers, exc_info=None):
            """
            start_response returns

            :param status: text line of HTTP status code/msg
            :param headers: list of tuples represnting the headers to be
                            returned.
                            For example: [('Content-Type', 'text/plain'), ...]
            :param exc_info: ...

            :returns: the response from the next middleware in the pipeline.
            """
            # Example of adding headers to the Response.
            # NOTE: make sure you append the header as a tuple.
            headers.append(('Sample-Bar', 'bar'))

            # Example of changing a header.
            # If you wish to change a header, you must construct a new list
            # of headers, appending the headers you don't care about and
            # replacing the ones you do.
            new_headers = []
            for h in headers:
                if h[0].lower() == 'content-type':
                    new_headers.append(('Content-Type', 'foo/bar'))
                else:
                    new_headers.append(h)

            return start_response(status, new_headers, exc_info)

        # Return the result from calling the next middleware in the pipeline
        # If you don't care about inspecting the response on the way out
        # you can omit defining _start_response, and just pass start_response
        # in the following call.
        return self.app(env, _start_response)

    # Declare this method as publicly accessible for HTTP requests
    @public
    # Allow unauthorized OPTIONS call
    @cors_validation
    # Allow admin or account owner requests to skip expensive ACL verifications
    @delay_denial
    def GET(self, req):
        return self.GETorHEAD(req)

    @public
    @cors_validation
    @delay_denial
    def HEAD(self, req):
        return self.GETorHEAD(req)

    def GETorHEAD(self, req):
        return Response(request=req, body="SAMPLE", content_type="text/plain")


def filter_factory(global_conf, **local_conf):
    """
    Executed once when the proxy is started.

    @global_conf dictionary containing the config values located
    in the default section of the proxy-server.conf.
    @local_conf dictionary containing the config values located
    in this middleware's config section.

    @returns ...
    """
    # In most cases your middleware won't need the global conf.
    # If you do, you could either add global_conf to conf or
    # modify your middleware class to accept both configs.

    # Iterate through config to ensure all keys are the lowercase equivalent.
    conf = {key.lower(): value for (key, value) in local_conf.iteritems()}

    # Next make sure that any required config values are set.
    for key, value in {'key1': 'default value1',
                       'key2': 'default value2',
                       'secretkey1': 'default secretvalue1'}.iteritems():
        if key not in conf:
            conf[key] = value

    # If you wish for your middleware to be discoverable by clients, you
    # may register it.
    # Clients can then make a GET request to http://127.0.0.1:8080/info
    # The name of the middleware is the only required parameter, but you may
    # optionally provide config data for clients to be aware of when
    # discovering your middleware.
    register_swift_info(
        name,
        key1=conf.get('key1'),
        key2=conf.get('key2'))

    # You may also register the middlware in a privileged admin section.
    # info regsitered in this way will not be discoverable unless a
    # valid HMAC is provided, ensuring that only authorized clients have
    # access to it.
    register_swift_info(
        name,
        admin=True,
        secretkey1=conf.get('secretkey1'))

    def sample_filter(app):
        """
        @app the next middleware in the pipeline.
        """
        return SampleMiddleware(app, conf)
    return sample_filter
