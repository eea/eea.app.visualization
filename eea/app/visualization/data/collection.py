""" Adapters to provide data
"""
import csv
from StringIO import StringIO
from eea.app.visualization.data.data import Data
from zope.component import queryUtility
from Products.ATContentTypes.interface import IATCTTool

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
