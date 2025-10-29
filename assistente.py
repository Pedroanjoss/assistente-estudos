from nltk import word_tokenize, corpus
from inicializador_modelo import *
from transcritor import *
import secrets
import pyaudio
import wave
import os
import json
# from lampada import * # MODIFICADO: Removido
# from som import * # MODIFICADO: Removido
from tutor import * # MODIFICADO: Adicionado seu novo atuador
from threading import Thread
# from api import * # Mantido (mesmo estando vazio)
from flask import Flask, Response, request, send_from_directory
import torch # NOVO: Importado para o 'if __name__ == "__main__"'

LINGUAGEM = "portuguese"
FORMATO = pyaudio.paInt16
CANAIS = 1
AMOSTRAS = 1024
TEMPO_GRAVACAO = 5
CAMINHO_AUDIO_FALAS = "C:\\Users\\rebec\\OneDrive\\Documentos\\BSI\\Semestre 6\\Inteligencia Artificial\\assistente virtual\\temp"
CONFIGURACOES = "C:\\Users\\rebec\\OneDrive\\Documentos\\BSI\\Semestre 6\\Inteligencia Artificial\\assistente virtual\\config.json"
MODO_LINHA_DE_COMANDO = 1
MODO_WEB = 2
MODO_DE_FUNCIONAMETO = MODO_LINHA_DE_COMANDO # MODIFICADO: Mude para linha de comando para testar mais fácil

def iniciar(dispositivo):
    # Esta função está OK. Ela carrega o modelo e o NOVO config.json
    modelo_iniciado, processador, modelo = iniciar_modelo(MODELOS[0], dispositivo)

    gravador = pyaudio.PyAudio()
    
    palavras_de_parada = set(corpus.stopwords.words(LINGUAGEM))
    
    with open(CONFIGURACOES, "r", encoding="utf-8") as arquivo_configuracoes:
        configuracoes = json.load(arquivo_configuracoes)
        acoes = configuracoes["acoes"]
        
        arquivo_configuracoes.close

    return modelo_iniciado, processador, modelo, gravador, palavras_de_parada, acoes

def iniciar_atuadores():
    # MODIFICADO: Aponta para seu novo atuador 'tutor'
    atuadores = []
    
    if iniciar_tutor(): # Função do seu tutor.py
        atuadores.append({"nome": "Tutor de Estudos",
                         "atuacao": atuar_sobre_tutor}) # Função do seu tutor.py
    
    return atuadores


# --- Funções Inalteradas (capturar_fala, gravar_fala, processar_transcricao, validar_comando) ---
# Estas funções podem ser mantidas exatamente como estão no seu original.
# O 'validar_comando' funciona perfeitamente com seu novo JSON.
def capturar_fala(gravador):
    gravacao = gravador.open(format=FORMATO, channels=CANAIS, rate=TAXA_AMOSTRAGEM, input=True, frames_per_buffer=AMOSTRAS)
    print("fale alguma coisa...")
    fala = []
    for _ in range(0, int(TAXA_AMOSTRAGEM/AMOSTRAS*TEMPO_GRAVACAO)):
        fala.append(gravacao.read(AMOSTRAS))
    gravacao.stop_stream()
    gravacao.close()
    print("fala capturada")
    return fala

def gravar_fala(gravador, fala):
    gravado, arquivo = False, f"{CAMINHO_AUDIO_FALAS}\\{secrets.token_hex(32).lower()}.wav"
    try:
        wav = wave.open(arquivo, "wb")
        wav.setnchannels(CANAIS)
        wav.setsampwidth(gravador.get_sample_size(FORMATO))
        wav.setframerate(TAXA_AMOSTRAGEM)
        wav.writeframes(b"".join(fala))
        wav.close()
        gravado = True
    except Exception as e:
        print(f"erro gravando arquivo de fala: {str(e)}")
    return gravado, arquivo

def processar_transcricao(transcricao, palavras_de_parada):
    comando = []
    tokens = word_tokenize(transcricao)
    for token in tokens:
        if token not in palavras_de_parada:
            comando.append(token)
    return comando

def validar_comando(comando, acoes):
    valido, acao, dispositivo = False, None, None
    if len(comando) >= 2:
        acao = comando[0]
        dispositivo = comando[1]
        for acao_prevista in acoes:
            if acao == acao_prevista["nome"]:
                if dispositivo in acao_prevista["dispositivos"]:
                    valido = True
                    break
    return valido, acao, dispositivo

# --- Fim das Funções Inalteradas ---


def atuar(acao, dispositivo, atuadores, comando_completo):
    # MODIFICADO: Adicionado 'comando_completo'
    # Esta é a mudança mais importante.
    # Precisamos passar a lista inteira de tokens para o atuador.
    """
    Parâmetros:
    acao: 'adicionar'
    dispositivo: 'revisão'
    atuadores: Lista de atuadores iniciados
    comando_completo: ['adicionar', 'revisão', 'matemática', '18', 'horas']
    """
    for atuador in atuadores:
        print(f"enviando comando para {atuador['nome']}")
        
        # MODIFICADO: Adicionado 'comando_completo' aos args da Thread
        atuacao = Thread(target=atuador["atuacao"], args=[acao, dispositivo, comando_completo])
        atuacao.start()
        
        
########## linha de comando ##########

def ativar_linha_de_comando():
    # Esta função é chamada se MODO_DE_FUNCIONAMETO = MODO_LINHA_DE_COMANDO
    while True:
        fala = capturar_fala(gravador)
        gravado, arquivo = gravar_fala(gravador, fala)
        if gravado:
            fala = carregar_fala(arquivo)
            transcricao = transcrever_fala(dispositivo, fala, modelo, processador)

            if os.path.exists(arquivo):
                    os.remove(arquivo)
                    
            comando = processar_transcricao(transcricao, palavras_de_parada)      
            
            print(f"comando: {comando}")
            
            valido, acao, dispositivo_alvo = validar_comando(comando, acoes)
            
            if valido:
                print(f"executando {acao} sobre {dispositivo_alvo}")
                
                # MODIFICADO: Passa o 'comando' completo para o 'atuar'
                atuar(acao, dispositivo_alvo, atuadores, comando)    
            else:
                print("comando inválido")

        else:
            print("ocorreu um erro gravando a fala")