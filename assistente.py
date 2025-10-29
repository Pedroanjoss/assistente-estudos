from nltk import word_tokenize, corpus
from inicializador_modelo import *
from transcritor import *
import secrets
import pyaudio
import wave
import os
import json
import torch # Adicionado para o __main__
from threading import Thread
from flask import Flask, Response, request, send_from_directory

# --- NOVOS ATUADORES ---
from plano import *
from revisao import *
from tarefa import *
from resumo import *
# --- ATUADORES ANTIGOS REMOVIDOS ---
# from lampada import *
# from som import *

LINGUAGEM = "portuguese"
FORMATO = pyaudio.paInt16
CANAIS = 1
AMOSTRAS = 1024
TEMPO_GRAVACAO = 5
# Use os caminhos exatos do seu computador
CAMINHO_AUDIO_FALAS = "C:\\Users\\rebec\\OneDrive\\Documentos\\BSI\\Semestre 6\\Inteligencia Artificial\\assistente virtual\\temp"
CONFIGURACOES = "C:\\Users\\rebec\\OneDrive\\Documentos\\BSI\\Semestre 6\\Inteligencia Artificial\\assistente virtual\\config.json"
MODO_LINHA_DE_COMANDO = 1
MODO_WEB = 2
MODO_DE_FUNCIONAMETO = MODO_LINHA_DE_COMANDO # Mude para MODO_WEB quando precisar

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
    # MODIFICADO: Carrega os 4 novos atuadores
    atuadores = []
    
    if iniciar_plano():
        atuadores.append({"nome": "Plano",
                         "atuacao": atuar_sobre_plano})
                         
    if iniciar_revisao():
        atuadores.append({"nome": "Revisão",
                         "atuacao": atuar_sobre_revisao})

    if iniciar_tarefa():
        atuadores.append({"nome": "Tarefa",
                         "atuacao": atuar_sobre_tarefa})
                         
    if iniciar_resumo():
        atuadores.append({"nome": "Resumo",
                         "atuacao": atuar_sobre_resumo})
                         
    return atuadores

# --- Funções Inalteradas (capturar_fala, gravar_fala, processar_transcricao, validar_comando) ---
# Estas funções são genéricas e funcionam perfeitamente com seu novo tema.
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
    # Esta função agora envia todos os tokens (ex: 'matemática 18 horas')
    # para TODOS os atuadores. Cada atuador decidirá se deve agir.
    for atuador in atuadores:
        print(f"Enviando comando para {atuador['nome']}")
        
        # MODIFICADO: Passa 'acao', 'dispositivo', e 'comando_completo'
        atuacao = Thread(target=atuador["atuacao"], args=[acao, dispositivo, comando_completo])
        atuacao.start()
        
        
########## linha de comando ##########

def ativar_linha_de_comando():
    # MODIFICADO: Passa 'comando' (tokens) para a função 'atuar'
    while True:
        fala = capturar_fala(gravador)
        gravado, arquivo = gravar_fala(gravador, fala)
        if gravado:
            fala = carregar_fala(arquivo)
            transcricao = transcrever_fala(dispositivo, fala, modelo, processador)

            if os.path.exists(arquivo):
                    os.remove(arquivo)
                    
            comando = processar_transcricao(transcricao, palavras_de_parada)      
            
            print(f"comando tokenizado: {comando}")
            
            valido, acao, dispositivo_alvo = validar_comando(comando, acoes)
            
            if valido:
                print(f"executando {acao} sobre {dispositivo_alvo}")
                # MODIFICADO: Passa 'comando' (a lista de tokens) como 'comando_completo'
                atuar(acao, dispositivo_alvo, atuadores, comando)    
            else:
                print("comando inválido")
            
            # A chamada 'atuar' foi movida para dentro do 'if valido:'

        else:
            print("ocorreu um erro gravando a fala")