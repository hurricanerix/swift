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

from setuptools import setup, find_packages

from sample import name, version


setup(
    name=name,
    version=version,
    author="your name here",
    author_email="your.name@example.com",
    description="Reference proxy middleware for OpenStack Swift",
    keywords="openstack swift middleware",
    url="http://github.com/openstack/swift/examples/middleware",
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: OpenStack',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],
    install_requires=[],
    entry_points={
        'paste.filter_factory': [
            'swift_simple_middleware=sample.simple:filter_factory',
            'swift_webhook_middleware=sample.webhook:filter_factory',
        ],
    },
)
