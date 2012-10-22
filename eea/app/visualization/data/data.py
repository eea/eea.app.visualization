""" Adapters to provide data
"""
import csv
import logging
from StringIO import StringIO
from zope.interface import implements
from zope.component import queryUtility
from Products.ATContentTypes.interface import IATCTTool
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

class Collection(Data):
    """ Data adapter for plone.app.collection
    """
    @property
    def data(self):
        """ Returns the list of brains as a CSV table
        """
        brains = self.context.queryCatalog(batch=False)
        atool = queryUtility(IATCTTool)
        metadata = atool.getAllMetadata(True)

        output = StringIO()
        writter = csv.writer(output, dialect='eea.app.visualization.tsv')

        metadata.insert(0, 'url')
        metadata.insert(0, 'label')

        writter.writerow(metadata)
        for brain in brains:
            row = []
            for key in metadata:
                if key == 'label':
                    key = 'getId'

                if key == 'url':
                    val = brain.getURL()
                else:
                    val = getattr(brain, key, '')
                row.append(val if (val and val != "None") else "")
            writter.writerow(row)

        output.seek(0)
        return output.read()
