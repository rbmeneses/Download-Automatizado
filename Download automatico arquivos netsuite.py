from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Configurar WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")  # Abre o navegador maximizado
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 15)  # Espera até 15 segundos por elementos

# URL da página de documentos do NetSuite
url = "https://6730950.app.netsuite.com/app/common/media/mediaitemfolders.nl?sc=-63&whence="
driver.get(url)

def baixar_todos_arquivos():
    """Baixa todos os arquivos da página atual."""
    try:
        arquivos = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//a[text()='Fazer download']")))

        for arquivo in arquivos:
            try:
                driver.execute_script("arguments[0].scrollIntoView();", arquivo)  # Garante que o link esteja visível
                arquivo.click()  # Clica para iniciar o download
                print(f"Download iniciado: {arquivo.get_attribute('href')}")
                time.sleep(2)  # Pequeno delay entre os downloads
            except Exception as e:
                print(f"Erro ao baixar arquivo: {e}")

    except Exception as e:
        print(f"Erro ao listar arquivos: {e}")

def proxima_pagina():
    """Navega para a próxima página se possível."""
    try:
        # Aguarda até que o botão esteja visível
        next_button = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='segment_sel_fs']/span[2]/button[2]")))

        # Verifica se o botão está desativado
        if "disabled" in next_button.get_attribute("class") or not next_button.is_displayed():
            print("Botão 'Próximo' desativado ou oculto. Finalizando downloads.")
            return False

        # Rola a página até o botão
        driver.execute_script("arguments[0].scrollIntoView();", next_button)
        time.sleep(1)

        # Clica no botão para ir para a próxima página
        next_button.click()
        print("Navegando para a próxima página...")
        time.sleep(5)  # Tempo para carregar a próxima página

    except Exception as e:
        print(f"Erro ao tentar avançar para a próxima página: {e}")
        return False  # Indica que não há mais páginas
    return True

# Loop principal para baixar 50 arquivos por vez até atingir 30.000
try:
    input("Pressione Enter para iniciar os downloads...")  # Aguarda o usuário pressionar Enter
    
    total_baixados = 0
    limite_total = 30000  # Limite total de downloads
    
    while total_baixados < limite_total:
        baixar_todos_arquivos()
        
        # Contabiliza os arquivos baixados
        arquivos_baixados_essa_pagina = len(driver.find_elements(By.XPATH, "//a[text()='Fazer download']"))
        total_baixados += arquivos_baixados_essa_pagina
        print(f"Total baixado até agora: {total_baixados}")

        if total_baixados >= limite_total or not proxima_pagina():
            break

    print("Download concluído!")

except KeyboardInterrupt:
    print("Download interrompido pelo usuário.")
except Exception as e:
    print(f"Ocorreu um erro inesperado: {e}")
finally:
    driver.quit()  # Fecha o navegador no final, independentemente de erros

