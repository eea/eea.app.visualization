""" Events handlers
"""
def set_default_layout(doc, evt):
    """ EVENT: Visualization enabled
    """
    if hasattr(doc, 'setLayout'):
        doc.setLayout('daviz-view.html')
    if hasattr(doc, 'reindexObject'):
        doc.reindexObject(['object_provides', ])

def unset_default_layout(doc, evt):
    """ EVENT: Visualization disabled
    """
    if doc.hasProperty('layout'):
        doc.manage_delProperties(['layout'])
    if hasattr(doc, 'reindexObject'):
        doc.reindexObject(['object_provides', ])
