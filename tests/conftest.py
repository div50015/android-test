import allure
import pytest
import allure_commons
from appium.options.android import UiAutomator2Options
from selene import browser, support
import os
import config
from utils import attach
from appium import webdriver


@pytest.fixture(scope='function', autouse=True)
def mobile_management():
    options = UiAutomator2Options().load_capabilities({
        "platformVersion": "10.0",
        "deviceName": "android",
        "app": "/opt/selenoid/app.apk",
        # "app": "/opt/selenoid/app.apk:ro",
    })

    # browser.config.driver_remote_url = 'http://hub.browserstack.com/wd/hub'
    # browser.config.driver_options = options
    with allure.step('init app session'):
        browser.config.driver = webdriver.Remote("http://87.117.11.241:4444/wd/hub", options=options)

    browser.config.timeout = float(os.getenv('timeout', '30.0'))

    browser.config._wait_decorator = support._logging.wait_with(
        context=allure_commons._allure.StepContext
    )

    yield

    attach.add_screenshot(browser)
    attach.add_logs(browser)
    attach.add_html(browser)
    attach.add_video(browser)

    browser.quit()






