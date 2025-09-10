from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from conftest import logger

def test_login_exitoso(driver):
    wait = WebDriverWait(driver, 10)

    logger.info("🔹 Abrir página Saucedemo")
    driver.get("https://www.saucedemo.com/")

    logger.info("🔹 Iniciando login")
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()

    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "inventory_list")))
    assert "inventory" in driver.current_url, "❌ Login falló"
    logger.info("✅ Login exitoso")
