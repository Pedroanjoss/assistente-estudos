# Arquivo: testes.py
import unittest
import torch
from assistenteEstudos import *
from transcritor import carregar_fala, transcrever_fala 


MOSTRAR_PLANO = "C:\\Users\\Pedro\\Documents\\atividade\\assistente-estudos\\audios\\plano-estudo.wav"
ADD_REVISAO = "C:\\Users\\Pedro\\Documents\\atividade\\assistente-estudos\\audios\\adicionar-revisao.wav" 
MARCAR_TAREFA = "C:\\Users\\Pedro\\Documents\\atividade\\assistente-estudos\\audios\\marcar-tarefa.wav" 
GERAR_RESUMO = "C:\\Users\\Pedro\\Documents\\atividade\\assistente-estudos\\audios\\gerar-resumo.wav" 

class TestesTutor(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dispositivo = "cuda:0" if torch.cuda.is_available() else "cpu"
        
        
        cls.iniciado, cls.processador, cls.modelo, _, cls.palavras_de_parada, cls.acoes = iniciar(cls.dispositivo)
    
    def testar_01_modelo_iniciado(self):
        self.assertTrue(self.iniciado)
        
    def _executar_teste_comando(self, caminho_audio, acao_esperada, dispositivo_esperado):
       
        print(f"\n--- Testando: {caminho_audio} ---")
        fala = carregar_fala(caminho_audio)
        self.assertIsNotNone(fala)
        
        transcricao = transcrever_fala(self.dispositivo, fala, self.modelo, self.processador)
        self.assertIsNotNone(transcricao)
        print(f"Transcrição: '{transcricao}'")
        
        comando = processar_transcricao(transcricao, self.palavras_de_parada)
        self.assertIsNotNone(comando)
        print(f"Comando tokenizado: {comando}")
        
        valido, acao, dispositivo_alvo = validar_comando(comando, self.acoes)
        
       
        self.assertTrue(valido, "O comando foi considerado inválido")
        self.assertEqual(acao, acao_esperada)
        self.assertEqual(dispositivo_alvo, dispositivo_esperado)
        
    def testar_02_mostrar_plano(self):
        self._executar_teste_comando(MOSTRAR_PLANO, "mostrar", "plano")
        
    def testar_03_adicionar_revisao(self):
        self._executar_teste_comando(ADD_REVISAO, "adicionar", "revisão")
        
    def testar_04_marcar_tarefa(self):
        self._executar_teste_comando(MARCAR_TAREFA, "marcar", "tarefa")
        
    def testar_05_gerar_resumo(self):
        self._executar_teste_comando(GERAR_RESUMO, "gerar", "resumo")

if __name__ == "__main__":
    unittest.main()