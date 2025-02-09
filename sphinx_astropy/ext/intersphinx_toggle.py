# Licensed under a 3-clause BSD style license - see LICENSE.rst

"""
The purpose of this extension is to provide a configuration value that can be
used to disable intersphinx on the command-line without editing conf.py. To use,
you can build documentation with::

    sphinx-build ... -D disable_intersphinx=1

This is used e.g. by astropy-helpers when using the build_docs command.
"""
from packaging.version import Version

from sphinx import __version__

SPHINX_LT_18 = Version(__version__) < Version('1.8')


def disable_intersphinx(app, config=None):

    from sphinx.util.console import bold

    from sphinx.util import logging
    info = logging.getLogger(__name__).info

    if app.config.disable_intersphinx:
        info(bold('disabling intersphinx...'))
        app.config.intersphinx_mapping.clear()


def setup(app):

    # Note that the config-inited setting was only added in Sphinx 1.8. For
    # earlier versions we use builder-inited but we need to be careful in what
    # order the extensions are declared so that this happens before intersphinx.
    if SPHINX_LT_18:
        app.connect('builder-inited', disable_intersphinx)
    else:
        app.connect('config-inited', disable_intersphinx)

    app.add_config_value('disable_intersphinx', 0, True)

    return {'parallel_read_safe': True,
            'parallel_write_safe': True}
