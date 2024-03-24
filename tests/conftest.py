import allure
import pytest
import allure_commons
from appium.options.android import UiAutomator2Options
from selene import browser, support
import os
from dotenv import load_dotenv
import config
import utils

from appium import webdriver


# @pytest.fixture(scope='session', autouse=True)
# def load_env():
#     load_dotenv()


@pytest.fixture(scope='function', autouse=True)
def mobile_management():
    # login = os.getenv('LOGIN')
    # password = os.getenv('PASSWORD')
    options = UiAutomator2Options().load_capabilities({
        # Specify device and os_version for testing
        # "platformName": "android",
        "platformVersion": "9.0",
        "deviceName": "Google Pixel 3",

        # Set URL of the application under test
        "app": "bs://sample.app",

        # Set other BrowserStack capabilities
        'bstack:options': {
            "projectName": "Mobile Tests Lesson 21",
            "buildName": "browserstack-build-1",
            "sessionName": "BStack android_test",

            # Set your access credentials
            "userName": f'{config.login}',
            "accessKey": f'{config.password}'
            # "userName": "bsuser_gEb24K",
            # "accessKey": "y2txdesxJgRFezzqc67Y"
            # "userName": "iakivkramarenko_qKHOLN",
            # "accessKey": "FSHAmndKHW3XsDkgm5zT"
        }
    })

    # browser.config.driver_remote_url = 'http://hub.browserstack.com/wd/hub'
    # browser.config.driver_options = options
    with allure.step('init app session'):
        browser.config.driver = webdriver.Remote(
            "http://hub.browserstack.com/wd/hub",
            options=options
        )

    browser.config.timeout = float(os.getenv('timeout', '10.0'))

    browser.config._wait_decorator = support._logging.wait_with(
        context=allure_commons._allure.StepContext
    )

    yield

    utils.allure.attach_bstack_screenshot()
    utils.allure.attach_bstack_page_source()

    session_id = browser.driver.session_id

    with allure.step('tear down app session'):
        browser.quit()

    utils.allure.attach_bstack_video(session_id)