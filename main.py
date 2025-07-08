import requests
from bs4 import BeautifulSoup
from datetime import datetime

# CONFIGURAÇÕES DO TELEGRAM
BOT_TOKEN = "8002177542:AAGgQ3_QzbC2JMalg1QQtsw18h_sRKuu8RI"
CHAT_ID = "824040117"
TELEGRAM_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

# PALAVRAS-CHAVE
PALAVRAS_CHAVE = [
    "gestão de contratos",
    "gestão fornecedores",
    "analista de logística",
    "especialista de logística",
    "supervisor de logística",
    "logística",
    "custo",
    "controller",
    "florestal",
    "colheita"
]

# EMPRESAS (somente Gupy por enquanto)
EMPRESAS = {
    "Klabin": "https://klabin.gupy.io/",
    "CMPC": "https://cmpc.gupy.io/",
    "Eldorado": "https://eldoradobrasil.gupy.io/"
}

# Função para envio ao Telegram
def enviar_telegram(mensagem):
    payload = {
        'chat_id': CHAT_ID,
        'text': mensagem,
        'parse_mode': 'Markdown'
    }
    try:
        response = requests.post(TELEGRAM_URL, data=payload)
        if response.status_code == 200:
            print("✅ Alerta enviado ao Telegram!")
        else:
            print(f"❌ Erro ao enviar alerta: {response.text}")
    except Exception as e:
        print(f"❌ Erro na requisição: {e}")

# Função principal de busca
def buscar_vagas():
    vagas_encontradas = 0

    for empresa, url in EMPRESAS.items():
        try:
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.text, "html.parser")
            vagas = soup.find_all("a", href=True)

            for vaga in vagas:
                titulo = vaga.get_text(strip=True).lower()
                link = vaga["href"]
                for palavra in PALAVRAS_CHAVE:
                    if palavra in titulo:
                        mensagem = (
                            f"🔔 *Vaga Encontrada!*\n\n"
                            f"*Empresa:* {empresa}\n"
                            f"*Cargo:* {titulo.title()}\n"
                            f"*Link:* {link}\n\n"
                            f"_Detectado por palavra-chave:_ *{palavra}*\n"
                            f"_Hora:_ {datetime.now().strftime('%H:%M:%S - %d/%m/%Y')}"
                        )
                        enviar_telegram(mensagem)
                        vagas_encontradas += 1
                        break  # para não mandar repetida
        except Exception as e:
            print(f"❌ Erro ao buscar vagas em {empresa}: {e}")

    if vagas_encontradas == 0:
        print("🔍 Nenhuma vaga encontrada no momento.")

if __name__ == "__main__":
    buscar_vagas()
