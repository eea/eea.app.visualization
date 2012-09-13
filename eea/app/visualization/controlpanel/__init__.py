""" Daviz settings
"""
def initialize(context):
    """ initialize DavizSettings
    """
    from AccessControl.Permissions import view_management_screens
    from eea.app.visualization.controlpanel.davizsettings import (DavizSettings,
                                                    zmi_addDavizSettings,
                                                    zmi_addDavizSettings_html)
    context.registerClass(
        DavizSettings,
        permission=view_management_screens,
        constructors=(zmi_addDavizSettings_html, zmi_addDavizSettings)
    )
