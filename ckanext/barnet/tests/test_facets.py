from nose.tools import assert_false

from ckanext.barnet.tests.helpers import FunctionalTestBase

class TestFacets(FunctionalTestBase):
    def test_organization_facets_do_not_appear(self):
        response = self._test_app.get('/dataset', status=200)
        assert_false('Organization' in response)
