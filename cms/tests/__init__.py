# -*- coding: utf-8 -*-


import unittest
import doctest
from django.conf import settings


# doc testing in some modules
from cms.utils import urlutils
from cms.tests.page import PagesTestCase
from cms.tests.permmod import PermissionModeratorTestCase
from cms.tests.site import SiteTestCase
from cms.tests.navextender import NavExtenderTestCase
from cms.tests.nonroot import NonRootCase

if "cms.plugins.text" in settings.INSTALLED_APPS:
    from cms.tests.plugins import PluginsTestCase
    if "reversion" in settings.INSTALLED_APPS:
        from cms.tests.reversion_tests import ReversionTestCase

from cms.tests.reversion_tests import ReversionTestCase
        
from cms.tests.menu import MenusTestCase
from cms.tests.rendering import RenderingTestCase
from cms.tests.placeholder import PlaceholderTestCase
from cms.tests.docs import DocsTestCase

settings.CMS_PERMISSION = True
settings.CMS_MODERATOR = True
settings.CMS_NAVIGATION_EXTENDERS = (
    ('testapp.sampleapp.menu_extender.get_nodes', 'SampleApp Menu'),
)

settings.CMS_FLAT_URLS = False
settings.CMS_MENU_TITLE_OVERWRITE = True
settings.CMS_HIDE_UNTRANSLATED = False
settings.CMS_URL_OVERWRITE = True
if not "testapp.sampleapp" in settings.INSTALLED_APPS:
    settings.INSTALLED_APPS = list(settings.INSTALLED_APPS) + ["testapp.sampleapp"]

def suite():
    s = unittest.TestSuite()
    s.addTest(doctest.DocTestSuite(urlutils))
    s.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(PagesTestCase))
    
    s.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(SiteTestCase))
    s.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(NavExtenderTestCase))
    s.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(NonRootCase))
    if "cms.plugins.text" in settings.INSTALLED_APPS:
        s.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(PluginsTestCase))
        if "reversion" in settings.INSTALLED_APPS:
            s.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ReversionTestCase))
    s.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(PermissionModeratorTestCase))
    s.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(MenusTestCase))
    s.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(RenderingTestCase))
    s.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(PlaceholderTestCase))
    s.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(DocsTestCase))
    
    return s
        
def test_runner_with_coverage(test_labels, verbosity=1, interactive=True, extra_tests=[]):
    """Custom test runner.  Follows the django.test.simple.run_tests() interface."""
        
    import os, sys
     
    # Look for coverage.py in __file__/lib as well as sys.path
    sys.path = [os.path.join(os.path.dirname(__file__), "lib")] + sys.path

    import coverage
    from django.test.utils import get_runner
    from django.conf import settings
    
    django_test_runner = get_runner(settings)(verbosity=verbosity, interactive=interactive)
    
    # Start code coverage before anything else if necessary
    #if hasattr(settings, 'COVERAGE_MODULES') and not test_labels:
    coverage.use_cache(0) # Do not cache any of the coverage.py stuff
    coverage.start()
 
    test_results = django_test_runner(test_labels, extra_tests=extra_tests)
 
    return test_results