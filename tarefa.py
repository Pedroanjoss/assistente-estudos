def iniciar_tarefa():
    """
    Sinaliza que o atuador 'Tarefa' está pronto.
    """
    print("Atuador 'Tarefa' iniciado.")
    return True

def atuar_sobre_tarefa(acao, dispositivo, comando_completo):
    """
    Verifica se o comando é para este atuador específico.
    """
    
    # Este atuador só responde se a 'acao' for 'marcar' E o 'dispositivo' for 'tarefa'
    if acao == "marcar" and dispositivo == "tarefa":
        
        # 'comando_completo' será algo como: ['marcar', 'tarefa', 'redes', 'neurais', 'concluída']
        try:
            # Pega do índice 2 (após "marcar tarefa") até o penúltimo (antes de "concluída")
            tarefa = " ".join(comando_completo[2:-1]) 
            print(f"\n[ATUADOR TAREFA]: Executando '{acao} {dispositivo}'")
            print(f"  -> MARCANDO TAREFA COMO CONCLUÍDA: '{tarefa}'")
        except Exception as e:
            print(f"[ATUADOR TAREFA]: Erro ao processar 'marcar tarefa': {e}")
            
    else:
        pass