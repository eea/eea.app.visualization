""" Adapters to provide data
"""
import logging
from zope.interface import implements
from eea.app.visualization.interfaces import IVisualizationData

logger = logging.getLogger('eea.app.visualization')

class Data(object):
    """ Abstract adapter to provide data
    """
    implements(IVisualizationData)

    def __init__(self, context):
        self.context = context

    @property
    def data(self):
        """ Data to be converted to JSON
        """
        return u''

    def __call__(self, **kwargs):
        return self.data

class OFSFile(Data):
    """ Data adapter for OFS.Image.File
    """
    @property
    def data(self):
        """ Data to be converted to JSON
        """
        return getattr(self.context, 'data', u'')

class Blob(Data):
    """ Data adapter for plone.app.blob.interfaces.IATBlobFile
    """
    @property
    def data(self):
        """ Data to be converted to JSON
        """
        if getattr(self.context, 'getFile', None):
            return getattr(self.context.getFile(), 'data', u'')
        return super(Blob, self).data
