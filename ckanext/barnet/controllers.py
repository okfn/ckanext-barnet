import json
import os.path
import inspect

import ckan.model as model
import ckan.plugins.toolkit as toolkit
from ckan.controllers.user import UserController
from ckan import new_authz

import ckanapi_exporter.exporter as exporter
import losser.losser


def this_directory():
    """Return the path to this Python file's directory.

    Return the full filesystem path to the directory containing this
    controllers.py file.

    """
    return os.path.dirname(os.path.abspath(
        inspect.getfile(inspect.currentframe())))


def export(columns):
    """Export all the datasets from the Barnet site to a CSV table.

    A CSV table is a list of OrderedDicts in which each dict has the same keys.

    We implement our own version of ckanapi-exporter's export() function
    because we want to get the data as a table, not as a CSV string.

    """
    datasets = exporter.get_datasets_from_ckan(
        "https://open.barnet.gov.uk/", apikey=None)
    exporter.extras_to_dicts(datasets)
    csv_table = losser.losser.table(
        datasets, columns, csv=False, pretty=False)
    return csv_table


def get_user_name(user_id):
    """Return the user name for the given user ID.

    We implement our own function (and access CKAN's model directly) because
    CKAN's user_show() action is too slow.

    """
    import ckan.model as model
    user_object = model.User.get(user_id)
    return user_object.fullname or user_object.name or user_object.id


def convert_user_ids_to_user_names(csv_table):
    """Convert the user IDs in the given table to user names.

    Convert the user ID in the "Uploaded By" key of each dict in the given
    table (list of dicts) into the corresponding user name.

    """
    for csv_dict in csv_table:
        user_id = csv_dict.get("Uploaded By")
        if not user_id:
            continue
        user_name = get_user_name(user_id)
        if user_name:
            csv_dict["Uploaded By"] = user_name


def convert_csv_table_to_csv_string(csv_table):
    """Return a CSV-formatted string for the given table (list of dicts)."""
    csv_string = losser.losser._table_to_csv(csv_table)
    return csv_string


class CSVExportController(toolkit.BaseController):

    def export(self):

        context = {'model': model, 'user': toolkit.c.user,
                   'auth_user_obj': toolkit.c.userobj}
        try:
            toolkit.check_access('export_csv', context, {})
        except toolkit.NotAuthorized:
            toolkit.abort(401, toolkit._(
                'Need to be organization administrator to export as CSV')
            )
        columns = os.path.join(this_directory(), "columns.json")

        csv_table = export(columns)

        # export() returns user IDs not user names in the "Uploaded By" column
        # because that's all the dataset dicts that package_search() returns
        # contain. Convert these IDs to user names ourselves.
        convert_user_ids_to_user_names(csv_table)

        csv_string = convert_csv_table_to_csv_string(csv_table)

        toolkit.response.headers["Content-type"] = "text/csv"
        toolkit.response.headers["Content-disposition"] = (
            "attachment; filename=export.csv")
        return csv_string


class BarnetUserController(UserController):
    def new(self, data=None, errors=None, error_summary=None):
        '''This is a modified version of the core user controller

        We have removed the lines redirecting the user the logout page
        if they are already logged in, this allows sysadmins to create
        users as we have disabled user registration unless they are
        sys admins'''
        context = {'model': model, 'session': model.Session,
                   'user': toolkit.c.user or toolkit.c.author,
                   'auth_user_obj': toolkit.c.userobj,
                   'schema': self._new_form_to_db_schema(),
                   'save': 'save' in toolkit.request.params}

        try:
            toolkit.check_access('user_create', context)
        except toolkit.NotAuthorized:
            toolkit.abort(401, toolkit._('Unauthorized to create a user'))

        if context['save'] and not data:
            return self._save_new(context)

        data = data or {}
        errors = errors or {}
        error_summary = error_summary or {}
        vars = {'data': data, 'errors': errors, 'error_summary': error_summary}

        toolkit.c.is_sysadmin = new_authz.is_sysadmin(toolkit.c.user)
        toolkit.c.form = toolkit.render(self.new_user_form, extra_vars=vars)
        return toolkit.render('user/new.html')
