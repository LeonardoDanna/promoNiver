import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime

# Mensagem inicial
print("Iniciando o script...")

# Configurações do Selenium
try:
    print("Configurando o navegador Chrome...")
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')  # Inicia o navegador maximizado
    options.add_argument('--user-data-dir=/caminho/para/perfil/chrome')  # Usa um perfil persistente
    driver = webdriver.Chrome(options=options)
    print("Navegador Chrome configurado com sucesso!")
except Exception as e:
    print(f"Erro ao configurar o navegador: {e}")
    exit()

# Função para enviar mensagem no WhatsApp
def enviar_mensagem_whatsapp(telefone, mensagem):
    try:
        print(f"Iniciando envio de mensagem para {telefone}...")
        driver.get(f'https://web.whatsapp.com/send?phone={telefone}')
        print("Aguardando carregamento do WhatsApp Web...")

        # Espera até que a caixa de texto esteja presente na página
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]'))
        )
        print("Caixa de texto localizada. Digitando a mensagem...")

        caixa_de_texto = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]')
        caixa_de_texto.send_keys(mensagem)
        caixa_de_texto.send_keys(Keys.ENTER)
        print("Mensagem enviada com sucesso!")
        time.sleep(2)
    except Exception as e:
        print(f"Erro ao enviar mensagem para {telefone}: {e}")

# Ler o arquivo CSV
try:
    print("Lendo o arquivo CSV...")
    contatos_df = pd.read_csv('contatos.csv')
    print("Arquivo CSV lido com sucesso!")
except Exception as e:
    print(f"Erro ao ler o arquivo CSV: {e}")
    driver.quit()
    exit()

# Obter a data atual
hoje = datetime.now().strftime('%m-%d')
print(f"Data atual: {hoje}")

# Iterar sobre os contatos
print("Iniciando iteração sobre os contatos...")
for index, contato in contatos_df.iterrows():
    try:
        print(f"\nProcessando contato: {contato['nome']}")
        aniversario = datetime.strptime(contato['aniversario'], '%Y-%m-%d').strftime('%m-%d')
        print(f"Aniversário do contato: {aniversario}")
        
        if aniversario == hoje:
            print("Aniversário hoje! Preparando mensagem...")
            mensagem = f"Olá {contato['nome']}, feliz aniversário! Parabens!\nPara comemorar, temos uma promoção especial para você: 20% de desconto em toda a loja!"
            print(f"Mensagem preparada: {mensagem}")
            enviar_mensagem_whatsapp(contato['telefone'], mensagem)
        else:
            print("Hoje não é o aniversário deste contato.")
    except Exception as e:
        print(f"Erro ao processar contato {contato['nome']}: {e}")

# Fechar o navegador
print("Fechando o navegador...")
driver.quit()
print("Navegador fechado. Script finalizado!")