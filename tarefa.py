def iniciar_tarefa():
   
    print("Atuador 'Tarefa' iniciado.")
    return True

def atuar_sobre_tarefa(acao, dispositivo, comando_completo):

    if (acao == "marcar" or acao == "marca") and dispositivo == "tarefa":

        try:
         
            tarefa = " ".join(comando_completo[2:-1]) 
            print(f"\n[ATUADOR TAREFA]: Executando '{acao} {dispositivo}'")
            print(f"  -> MARCANDO TAREFA COMO CONCLUÍDA: '{tarefa}'")
        except Exception as e:
            print(f"[ATUADOR TAREFA]: Erro ao processar 'marcar tarefa': {e}")
            
    else:
        pass