from nose.tools import assert_true, assert_false, assert_equals

from ckan.new_tests import factories

from ckanext.barnet.tests.helpers import FunctionalTestBase

class TestDataset(FunctionalTestBase):
    def test_date_uploaded_is_in_dataset_additional_info(self):
        dataset = factories.Dataset(user=factories.User())
        response = self._test_app.get('/dataset/{0}'.format(dataset['name'],
                                      status=200))
        assert_true('Date Uploaded' in response.body)

    def test_custom_schema(self):
        '''Test that the custom schema shows up on the dataset page'''
        dataset = factories.Dataset(
            user=factories.User(),
            frequency_update_period='frequency update period',
            retention_count=1,
            retention_period='retention period',
            delivery_unit='delivery unit',
            service='service',
            next_update='next update',
            review_date='review date',
            coverage_start_date='coverage start date',
            coverage_end_date='coverage end date',
        )

        response = self._test_app.get('/dataset/{0}'.format(dataset['name'],
                                      status=200))
        assert_true('Frequency' in response.body)
        assert_true('Retention' in response.body)
        assert_true('Delivery Unit' in response.body)
        assert_true('Service' in response.body)

    def test_maintainer_field_is_not_on_dataset_page(self):
        user=factories.User()
        dataset = factories.Dataset(
            maintainer=user['name'],
        )
        response = self._test_app.get('/dataset/{0}'.format(dataset['name'],
                                      status=200))
        assert_false('Maintainer' in response.body)


class TestCsvExportButton(FunctionalTestBase):
    def test_export_button_appears_for_sysadmins(self):
        user = factories.Sysadmin()
        extra_environ = {'REMOTE_USER': str(user['name'])}
        response = self._test_app.get('/dataset', extra_environ=extra_environ)
        assert_true('Export as CSV' in response.body)

    def test_export_button_does_not_appear_non_logged_in_users(self):
        response = self._test_app.get('/dataset')
        assert_false('Export as CSV' in response.body)

    def test_export_button_does_not_appear_logged_in_normal_users(self):
        response = self._test_app.get('/dataset')
        user = factories.User()
        extra_environ = {'REMOTE_USER': str(user['name'])}
        response = self._test_app.get('/dataset', extra_environ=extra_environ)
        assert_false('Export as CSV' in response.body)


class TestOnlySysadminsCanCreateUsers(FunctionalTestBase):
    def test_anon_users_cannot_register(self):
        response = self._test_app.get('/user/register')
        assert_equals(302, response.status_int)
        assert_equals(
            'http://localhost/user/login?came_from=http://localhost/user/register',
            response.location
        )

    def test_users_cannot_register_users(self):
        user = factories.User()
        extra_environ = {'REMOTE_USER': str(user['name'])}
        response = self._test_app.get('/user/register', 
                                      extra_environ=extra_environ,
                                      expect_errors=True)
        assert_equals(401, response.status_int)

    def test_sysadmins_users_can_register_users(self):
        user = factories.Sysadmin()
        extra_environ = {'REMOTE_USER': str(user['name'])}
        response = self._test_app.get('/user/register', 
                                      extra_environ=extra_environ)
        assert_equals(200, response.status_int)
