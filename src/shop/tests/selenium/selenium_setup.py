#!/usr/bin/env python
"""Set up for Selenium tests."""

# Third-party library imports
import pytest

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


__author__ = "Thomas Gwasira"
__date__ = "December 2021"
__version__ = "1.0.0"
__maintainer__ = "Thomas Gwasira"
__email__ = "tomgwasira@gmail.com"
__status__ = "Development"


@pytest.fixture(scope="session")
def chrome_browser_instance(request):
    """Provides a selenium webdriver instance.

    Creates a browser instance which can be used for selenium tests.
    """
    options = Options()
    options.headless = False  # used to make it run in background
    browser = webdriver.Chrome(
        ChromeDriverManager().install(), chrome_options=options
    )
    yield browser
    # browser.close()
