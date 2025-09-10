import pytest
import logging
import os
from selenium import webdriver

# --------------------------
# Logging
# --------------------------
logger = logging.getLogger("TestLogger")
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# --------------------------
# Fixture Selenium
# --------------------------
@pytest.fixture
def driver(request):
    options = webdriver.ChromeOptions()
    options.add_argument("--incognito")
    options.add_argument("--disable-extensions")
    options.add_argument("--start-maximized")
    options.add_argument("--user-data-dir=/tmp/selenium_clean_profile")

    driver = webdriver.Chrome(options=options)

    def fin():
        if request.node.rep_call.failed:
            os.makedirs("screenshots", exist_ok=True)
            screenshot_path = f"screenshots/{request.node.name}.png"
            driver.save_screenshot(screenshot_path)
            logger.error(f"Screenshot guardado: {screenshot_path}")
            if request.config.pluginmanager.hasplugin("html"):
                extra = getattr(request.node, "extra", [])
                extra.append(pytest.html.extras.png(screenshot_path))
                request.node.extra = extra
        driver.quit()

    request.addfinalizer(fin)
    return driver

# --------------------------
# Hook Pytest
# --------------------------
@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
