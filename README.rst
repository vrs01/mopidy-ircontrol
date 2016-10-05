****************************
Mopidy-IRControl
****************************

.. image:: https://pypip.in/v/Mopidy-IRControl/badge.png
    :target: https://pypi.python.org/pypi/Mopidy-IRControl/
    :alt: Latest PyPI version

.. image:: https://pypip.in/d/Mopidy-IRControl/badge.png
    :target: https://pypi.python.org/pypi/Mopidy-IRControl/
    :alt: Number of PyPI downloads

.. image:: https://api.travis-ci.org/spjoe/mopidy-ircontrol.png?branch=master
    :target: https://travis-ci.org/spjoe/mopidy-ircontrol
    :alt: Travis CI build status

.. image:: https://coveralls.io/repos/spjoe/mopidy-ircontrol/badge.png?branch=master
   :target: https://coveralls.io/r/spjoe/mopidy-ircontrol?branch=master
   :alt: Test coverage


A Mopidy frontend to control mopidy with an infrared remote control. It is using lirc<http://www.lirc.org/> as IR receiver deamon.


Installation
============

Install the dependencies by running::

    sudo apt-get install python-dev lirc liblircclient-dev


Install by running::

    pip install Mopidy-IRControl

    

Or, if available, install the Debian/Ubuntu package from `apt.mopidy.com
<http://apt.mopidy.com/>`_.


Configuration
=============

Before starting Mopidy, you must add configuration for
Mopidy-IRControl to your Mopidy configuration file::

    [IRControl]
    enabled = true
    #look at your lircd.conf (/etc/lirc/lircd.conf) to find you configured buttons names
    mute = KEY_MUTE
    next = KEY_NEXT
    previous = KEY_PREVIOUS
    playpause = KEY_PLAYPAUSE
    stop = KEY_STOP
    volumeup = KEY_VOLUMEUP
    volumedown = KEY_VOLUMEDOWN

Project resources
=================

- `Source code <https://github.com/spjoe/mopidy-ircontrol>`_
- `Issue tracker <https://github.com/spjoe/mopidy-ircontrol/issues>`_
- `Download development snapshot <https://github.com/spjoe/mopidy-ircontrol/tarball/master#egg=Mopidy-IRControl-dev>`_


Changelog
=========

v0.1.0 - 08.10.2015
----------------------------------------

- Initial release.

Contributors
============
- `logogin <https://github.com/logogin>`_
