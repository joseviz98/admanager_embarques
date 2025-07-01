from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# funcion para hacer login en el sistema
def test_login(driver): 
    driver.get("https://test.admanagerembarques.adventa.solutions/")

    # Se ubica el elmento de usuario
    campo_username = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "login")))
    
    # Se ubica el elemento password
    campo_password = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "password")))
    
    # Se ubica el botón de entrar
    boton_login = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "loginbtn")))

    # Se ingresa el usuario
    campo_username.send_keys("support@tepachesoft.com")
    
    # Se ingresa la contraseña
    campo_password.send_keys("secretos")
    
    # Se da clic en el boton para acceder
    boton_login.click()

    # Se ubica el elemento para validar que se haya logeado correctamente
    usuario_logeado = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "pr")))
    
    # Validamos que la varibale usuario_logeado contenga la clase pr
    assert "pr" in usuario_logeado.get_attribute("class")
    print("Prueba exitosa")