import os.path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
import json
import time
from selenium.webdriver.common.action_chains import ActionChains
import pygame
from selenium.common.exceptions import TimeoutException
import threading
import logging

# Configuração do logging
logging.basicConfig(
    level=logging.INFO,  # Níveis: DEBUG, INFO, WARNING, ERROR, CRITICAL
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="rewards_errors.log",  # Salva os logs em um arquivo
    filemode="a"  # "a" para anexar ao arquivo, "w" para sobrescrever
)

user_data = os.path.join(os.getcwd(), "usuario")

# Configurações do navegador
chrome_options = Options()
chrome_options.add_argument("--headless")  # Executa em segundo plano
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--enable-unsafe-swiftshader")
chrome_options.add_argument(f"user-data-dir={user_data}")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Inicializa o navegador e as configurações de espera
wait = WebDriverWait(driver, 20)  # Ajuste o tempo conforme necessário

action = ActionChains(driver)

if not os.path.exists("usuario"):
    os.mkdir("usuario")

audios_path = os.path.join(os.getcwd(), "audios")
print("Audios path:", audios_path)


def tocar_audio(caminho_audio):
    try:
        pygame.mixer.init()
    except Exception as e:
        print("Erro ao iniciar pygame. Continuando...")
        print(e)

    """
    Função para tocar um áudio.
    """
    pygame.mixer.music.load(caminho_audio)  # Carrega o arquivo de áudio
    pygame.mixer.music.play()  # Reproduz o áudio
    while pygame.mixer.music.get_busy():  # Aguarda o áudio terminar
        time.sleep(0.1)
    pygame.mixer.music.stop()
    pygame.mixer.quit()


def ler_creds():
    credenciais = os.path.join("pass.json")
    with open(credenciais, "r") as cred:
        creds = json.load(cred)

    email = creds["e"]
    senha = creds["p"]
    return email, senha


def login_to_rewards():
    email, senha = ler_creds()
    time.sleep(5)
    state = driver.execute_script("return document.readyState")
    if state == "loading":
        print("A página ainda não foi carregada corretamente. Recarregando...")
        driver.execute_script("window.location.reload()")  # Simula um reload da página

    # Preencher o campo de email
    email_field = wait.until(EC.element_to_be_clickable((By.NAME, "loginfmt")))  # Use o seletor correto
    print("Preenchendo campo de email")
    email_field.send_keys(email)  # Preenche o campo com o email

    # Clique no botão "Próximo" após preencher o email
    next_button = driver.find_element(By.ID, "idSIButton9")  # Seletor para o botão "Próximo"
    print("Clicando em próximo")
    next_button.click()
    sleep(3)  # Aguarde a página carregar

    # Preencher o campo de senha
    password_field = wait.until(EC.element_to_be_clickable((By.NAME, "passwd")))  # Use o seletor correto
    print("Preenchendo campo de senha")
    password_field.send_keys(senha)  # Preenche o campo com a senha

    # Clique no botão "Entrar"
    sign_in_button = driver.find_element(By.ID, "idSIButton9")  # Seletor para o botão "Entrar"
    print("Clicando em 'Entrar'")
    sign_in_button.click()
    sleep(3)  # Aguarde a página carregar

    # Opcional: Clique no botão "Sim" se aparecer para manter a sessão
    try:
        print("Clicando em 'Sim' para permanecer conectado")
        stay_signed_in_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='acceptButton']")))
        stay_signed_in_button.click()
    except Exception:
        print("Não apareceu o botão 'Manter conectado'.")

    # Verifica se a tela de confirmar informações de recuperação de conta apareceu
    confirmar_informacoes()

    print("Login realizado com sucesso.")


# Caso apareça a tela para confirmar informações de recuperação de conta
def confirmar_informacoes():
    """
    Detecta e clica no botão 'iLooksGood' caso a tela de confirmação de informações apareça.
    """
    try:
        print("Verificando se a tela de confirmação de informações aparece...")
        i_looks_good_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="iLooksGood"]'))
        )
        print("Tela de confirmação encontrada. Clicando no botão 'Tudo certo'.")
        i_looks_good_button.click()
        time.sleep(2)  # Aguarde um pouco após o clique
    except TimeoutException:
        print("Tela de confirmação de informações não apareceu. Continuando o processo...")


def process_cards(container_xpath, container_name):
    """
    Processa os cards dentro de um contêiner específico.
    - container_xpath: O XPath do contêiner principal.
    - container_name: Nome do contêiner (apenas para log).
    """
    # Obter o identificador da guia principal
    main_window = driver.current_window_handle

    # Localizar o contêiner principal
    container = driver.find_element(By.XPATH, container_xpath)

    # Localizar todos os "cards" dentro do contêiner
    cards = container.find_elements(By.XPATH, './/mee-card')

    print(f"Encontrados {len(cards)} cards no contêiner '{container_name}'.")

    # Criar a instância de ActionChains
    action = ActionChains(driver)

    # Iterar sobre os cards encontrados
    for i, card in enumerate(cards, start=1):
        try:
            print(f"Interagindo com o card {i} no contêiner '{container_name}'")

            # Mover para o card e clicar
            n = 0
            while n < 10:
                try:
                    action.move_to_element(card).click().perform()
                    time.sleep(2)
                    break
                except Exception as e:
                    n += 1
                    logging.error(f"Tentativa {n}/10 falhou ao clicar no card {i}: {e}")

            # Esperar até a nova guia abrir
            windows = driver.window_handles
            if len(windows) > 1:
                # Alternar para a nova guia
                driver.switch_to.window(windows[-1])
                print(
                    f"Nova guia aberta para o card {i} no contêiner '{container_name}'. Realizando ações na nova guia...")

                # Fechar a nova guia
                driver.close()
                print(f"Guia do card {i} no contêiner '{container_name}' fechada.")

                # Voltar para a guia principal
                driver.switch_to.window(main_window)
                print(f"Voltando para a guia principal.")

            time.sleep(1)

        except Exception as e:
            logging.error(f"Erro ao interagir com o card {i} no contêiner '{container_name}': {e}")


def verificar_login():
    """
    Verifica se a tela de login está presente.
    Retorna True se a tela de login for encontrada, caso contrário, False.
    """
    try:
        # Aguarda até que o campo de e-mail seja encontrado na página (indicativo de tela de login)
        wait.until(EC.presence_of_element_located((By.NAME, "loginfmt")))  # Campo de e-mail
        print("Tela de login detectada.")
        return True
    except:
        print("Nenhuma tela de login detectada.")
        return False


def main():
    try:
        try:
            audio_thread = threading.Thread(target=tocar_audio,
                                            args=(os.path.join(audios_path, "Iniciando_daily_quests.mp3"),))
            audio_thread.start()
        except Exception as e:
            logging.error(f"Erro ao tocar audio: {e}")

        print("Acessando https://rewards.microsoft.com/")
        driver.get("https://rewards.microsoft.com/")  # Acesse a página de login

        if verificar_login():
            login_to_rewards()
        else:
            print("O usuário já está logado. Prosseguindo...")

        # Chamada para processar os dois contêineres
        try:
            process_cards('//*[@id="daily-sets"]', "daily-sets")
        except Exception as e:
            logging.error(f"Erro ao processar containers: {e}")

        try:
            process_cards('//*[@id="more-activities"]/div', "more-activities")
        except Exception as e:
            logging.error(f"Erro ao processar cards: {e}")

        try:
            audio_thread = threading.Thread(target=tocar_audio,
                                            args=(os.path.join(audios_path,
                                                               "processo_concluido (online-audio-converter.com).mp3"),))
            audio_thread.start()
        except Exception as e:
            logging.error(f"Erro ao executar áudio: {e}")

        print("Script executado")
        time.sleep(120)
    except Exception as e:
        logging.error(f"Erro geral: {e}")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
