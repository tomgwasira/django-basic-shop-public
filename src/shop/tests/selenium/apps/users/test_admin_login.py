import pytest
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


@pytest.mark.selenium
def test_admin_login(live_server, db_setup, chrome_browser_instance):
    browser = chrome_browser_instance

    browser.get(("%s%s" % (live_server.url, "/admin/login/")))

    # Select elements on the page
    username = browser.find_element(By.NAME, "username")
    password = browser.find_element(By.NAME, "password")
    submit = browser.find_element(By.XPATH, '//input[@value="Log in"]')

    # Pass values to the elements
    username.send_keys("admin")
    password.send_keys("TomGwasira123")
    submit.send_keys(Keys.RETURN)

    assert "Site administration" in browser.page_source


# Installed pytest-django which comes with live_server which allows us to run django server in background during test
# so that we can run selenium.
# Need XPATH to select by value.
