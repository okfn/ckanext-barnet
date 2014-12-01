import json
import os.path
import inspect

import ckan.model as model
import ckan.plugins.toolkit as toolkit
import ckanapi_exporter.exporter as exporter


def this_directory():
    """Return the path to this Python file's directory.

    Return the full filesystem path to the directory containing this
    controllers.py file.

    """
    return os.path.dirname(os.path.abspath(
        inspect.getfile(inspect.currentframe())))


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
        csv_string = exporter.export("https://open.barnet.gov.uk/",
                                     columns=columns)
        toolkit.response.headers["Content-type"] = "text/csv"
        toolkit.response.headers["Content-disposition"] = (
            "attachment; filename=export.csv")
        return csv_string
