""" Edit form
"""

from zope.formlib.form import Fields
from eea.app.visualization.facets.edit import Edit as EditForm
from eea.app.visualization.facets.list.interfaces import IListProperties

class Edit(EditForm):
    """ Edit form
    """
    form_fields = Fields(IListProperties)
