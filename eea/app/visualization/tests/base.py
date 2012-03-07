""" Testing
"""
from  plone.app.testing import PloneSandboxLayer
#from  plone.app.testing import applyProfile
from  plone.app.testing import PLONE_FIXTURE
from plone.app.testing import FunctionalTesting
from zope.configuration import xmlconfig

class EEAFixture(PloneSandboxLayer):
    """ EEA Testing Policy
    """
    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        """ Setup Zope
        """
        import eea.app.visualization
        xmlconfig.file('configure.zcml',
                       eea.app.visualization,
                       context=configurationContext
                       )

    def setUpPloneSite(self, portal):
        """ Setup Plone
        """
        #applyProfile(portal, 'eea.app.visualization:default')

EEAFIXTURE = EEAFixture()
FUNCTIONAL_TESTING = FunctionalTesting(bases=(EEAFIXTURE,),
                                       name='EEAVisualization:Functional')
