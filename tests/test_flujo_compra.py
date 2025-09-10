from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from conftest import logger

def test_flujo_compra_completa(driver):
    wait = WebDriverWait(driver, 10)

    logger.info("🔹 Abrir página Saucedemo")
    driver.get("https://www.saucedemo.com/")

    # Login
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "inventory_list")))
    logger.info("✅ Login exitoso")

    # Agregar productos
    driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()
    driver.find_element(By.ID, "add-to-cart-sauce-labs-bike-light").click()
    #driver.find_element(By.ID, "add-to-cart-sauce-labs-onesie").click() #For failed  test case discomment this line
    badge = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "shopping_cart_badge")))
    assert badge.text == "2"
    logger.info("✅ Productos agregados al carrito")

    # Ir al carrito
    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    productos = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "cart_item")))
    assert len(productos) == 2
    logger.info("✅ Productos confirmados en carrito")

    # Checkout
    driver.find_element(By.ID, "checkout").click()
    wait.until(EC.presence_of_element_located((By.ID, "first-name")))
    driver.find_element(By.ID, "first-name").send_keys("Jonathan")
    driver.find_element(By.ID, "last-name").send_keys("Lopez")
    driver.find_element(By.ID, "postal-code").send_keys("12345")
    driver.find_element(By.ID, "continue").click()
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "summary_info")))
    logger.info("✅ Checkout completado")

    # Finalizar compra
    driver.find_element(By.ID, "finish").click()
    mensaje = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "complete-header"))).text
    assert "THANK YOU FOR YOUR ORDER" in mensaje.upper()
    logger.info("✅ Compra completada con éxito 🎉")
