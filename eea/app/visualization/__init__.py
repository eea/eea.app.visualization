""" Visualization API
"""
def initialize(context):
    """ Zope2 init
    """
    from eea.app.visualization.controlpanel import initialize as cpinitialize
    cpinitialize(context)
    return
