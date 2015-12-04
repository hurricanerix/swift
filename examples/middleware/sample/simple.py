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


MIDDLEWARE_NAME = 'simple-example'


class SimpleMiddleware(object):

    def __init__(self, app, conf):
        self.app = app
        self.conf = conf

    def __call__(self, env, start_response):
        """
        The entry point for your middleware, this get's called with
        every request to Swift.
        """

        # Return the result from calling the next middleware in the pipeline
        # If you don't care about inspecting the response on the way out
        # you can omit defining _start_response, and just pass start_response
        # in the following call.
        return self.app(env, start_response)

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
        MIDDLEWARE_NAME,
        key1=conf.get('key1'),
        key2=conf.get('key2'))

    # You may also register the middlware in a privileged admin section.
    # info regsitered in this way will not be discoverable unless a
    # valid HMAC is provided, ensuring that only authorized clients have
    # access to it.
    register_swift_info(
        MIDDLEWARE_NAME,
        admin=True,
        secretkey1=conf.get('secretkey1'))

    def sample_filter(app):
        """
        @app the next middleware in the pipeline.
        """
        return SimpleMiddleware(app, conf)
    return sample_filter
