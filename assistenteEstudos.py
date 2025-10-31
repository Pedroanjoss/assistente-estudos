import nltk 
from nltk import word_tokenize, corpus
from inicializador_modelo import *
from transcritor import *
import secrets
import pyaudio
import wave
import os
import json
import torch 
from threading import Thread



from plano import *
from revisao import *
from tarefa import *
from resumo import *

LINGUAGEM = "portuguese"
FORMATO = pyaudio.paInt16
CANAIS = 1
AMOSTRAS = 1024
TEMPO_GRAVACAO = 5

CAMINHO_AUDIO_FALAS = "C:\\Users\\Pedro\\Documents\\atividade\\assistente-estudos\\temp"
CONFIGURACOES = "C:\\Users\\Pedro\\Documents\\atividade\\assistente-estudos\\config.json"
 

def iniciar(dispositivo):
   
    modelo_iniciado, processador, modelo = iniciar_modelo(MODELOS[0], dispositivo)

    gravador = pyaudio.PyAudio()
    
    palavras_de_parada = set(corpus.stopwords.words(LINGUAGEM))
    
    with open(CONFIGURACOES, "r", encoding="utf-8") as arquivo_configuracoes:
        configuracoes = json.load(arquivo_configuracoes)
        acoes = configuracoes["acoes"]
        
        arquivo_configuracoes.close

    return modelo_iniciado, processador, modelo, gravador, palavras_de_parada, acoes

def iniciar_atuadores():
   
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
    tokens = word_tokenize(transcricao, language=LINGUAGEM)
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



def atuar(acao, dispositivo, atuadores, comando_completo):
   
    for atuador in atuadores:
        print(f"Enviando comando para {atuador['nome']}")
        
       
        atuacao = Thread(target=atuador["atuacao"], args=[acao, dispositivo, comando_completo])
        atuacao.start()
        
        


def ativar_linha_de_comando():
   
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
              
                atuar(acao, dispositivo_alvo, atuadores, comando)    
            else:
                print("comando inválido")
            
          

        else:
            print("ocorreu um erro gravando a fala")

if __name__ == "__main__":
    dispositivo = "cuda:0" if torch.cuda.is_available() else "cpu"

    iniciado, processador, modelo, gravador, palavras_de_parada, acoes = iniciar(dispositivo)

    if iniciado:
      
        atuadores = iniciar_atuadores()
        
       
        ativar_linha_de_comando()
             
    else:
        print("ocorre um erro de inicialização")