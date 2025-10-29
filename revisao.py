def iniciar_revisao():
    """
    Sinaliza que o atuador 'Revisão' está pronto.
    """
    print("Atuador 'Revisão' iniciado.")
    return True

def atuar_sobre_revisao(acao, dispositivo, comando_completo):
    """
    Verifica se o comando é para este atuador específico.
    """
    
    # Este atuador só responde se a 'acao' for 'adicionar' E o 'dispositivo' for 'revisão'
    if acao == "adicionar" and dispositivo == "revisão":
        
        # 'comando_completo' será algo como: ['adicionar', 'revisão', 'matemática', '18', 'horas']
        try:
            # Pega tudo após "adicionar revisão" (índice 2 em diante)
            parametros = " ".join(comando_completo[2:]) 
            print(f"\n[ATUADOR REVISÃO]: Executando '{acao} {dispositivo}'")
            print(f"  -> ADICIONANDO REVISÃO: '{parametros}'")
        except Exception as e:
            print(f"[ATUADOR REVISÃO]: Erro ao processar 'adicionar revisão': {e}")
    
    else:
        pass # Não faz nada, pois o comando não é para este atuador.