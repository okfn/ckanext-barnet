import webtest
from pylons import config

import ckan.config.middleware
from ckan.new_tests import helpers


# Backport of helpers from ckan/master that aren't in 2.2
def _get_test_app():
    '''Return a webtest.TestApp for CKAN, with legacy templates disabled.

    For functional tests that need to request CKAN pages or post to the API.
    Unit tests shouldn't need this.

    '''
    config['ckan.legacy_templates'] = False
    app = ckan.config.middleware.make_app(config['global_conf'], **config)
    app = webtest.TestApp(app)
    return app


class FunctionalTestBase(object):
    '''A base class for functional test classes to inherit from.

    Allows configuration changes by overriding _apply_config_changes and
    resetting the CKAN config after your test class has run. It creates a
    webtest.TestApp at self.app for your class to use to make HTTP requests
    to the CKAN web UI or API.

    If you're overriding methods that this class provides, like setup_class()
    and teardown_class(), make sure to use super() to call this class's methods
    at the top of yours!

    '''
    @classmethod
    def _get_test_app(cls):  # leading _ because nose is terrible
        # FIXME: remove this method and switch to using helpers.get_test_app
        # in each test once the old functional tests are fixed or removed
        if not hasattr(cls, '_test_app'):
            cls._test_app = _get_test_app()
        return cls._test_app

    @classmethod
    def setup_class(cls):
        # Make a copy of the Pylons config, so we can restore it in teardown.
        cls._original_config = dict(config)
        cls._apply_config_changes(config)
        cls._get_test_app()

    @classmethod
    def _apply_config_changes(cls, cfg):
        pass

    def setup(self):
        helpers.reset_db()

    @classmethod
    def teardown_class(cls):
        # Restore the Pylons config to its original values, in case any tests
        # changed any config settings.
        config.clear()
        config.update(cls._original_config)
