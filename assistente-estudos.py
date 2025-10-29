# Arquivo: tutor.py

def iniciar_tutor():
    """
    Inicializa o módulo de tutoria. 
    (No futuro, poderia carregar um BD de tarefas, mas para o trabalho, um print basta).
    """
    print("Atuador 'Tutor de Estudos' iniciado.")
    return True

def atuar_sobre_tutor(acao, dispositivo, comando_completo):
    """
    Esta é a função de atuação principal.
    Ela recebe o comando completo para poder extrair os parâmetros.
    'comando_completo' é uma lista de tokens, ex: ['adicionar', 'revisão', 'matemática', '18', 'horas']
    """
    
    try:
        if acao == "mostrar" and dispositivo == "plano":
            # Comando: "Mostrar plano de estudos de hoje"
            # Tokens: ['mostrar', 'plano', 'estudos', 'hoje']
            print(f"\n[ATUADOR TUTOR]:  Executando '{acao} {dispositivo}'")
            print("  -> Mostrando plano de hoje:\n     - 09:00: Redes Neurais\n     - 11:00: Cálculo")
        
        elif acao == "adicionar" and dispositivo == "revisão":
            # Comando: "Adicionar revisão de matemática às 18 horas"
            # Tokens: ['adicionar', 'revisão', 'matemática', '18', 'horas']
            parametros = " ".join(comando_completo[2:]) # Pega tudo após "adicionar revisão"
            print(f"\n[ATUADOR TUTOR]: Executando '{acao} {dispositivo}'")
            print(f"  -> Revisão adicionada: '{parametros}'")

        elif acao == "marcar" and dispositivo == "tarefa":
            # Comando: "Marcar tarefa de redes neurais como concluída"
            # Tokens: ['marcar', 'tarefa', 'redes', 'neurais', 'concluída']
            # Pega do índice 2 (após "marcar tarefa") até o penúltimo (antes de "concluída")
            tarefa = " ".join(comando_completo[2:-1]) 
            print(f"\n[ATUADOR TUTOR]: Executando '{acao} {dispositivo}'")
            print(f"  -> Tarefa marcada como concluída: '{tarefa}'")
            
        elif acao == "gerar" and dispositivo == "resumo":
            # Comando: "Gerar resumo das atividades pendentes"
            # Tokens: ['gerar', 'resumo', 'atividades', 'pendentes']
            print(f"\n[ATUADOR TUTOR]: Executando '{acao} {dispositivo}'")
            print("  -> Resumo de pendências:\n     - [ ] Prova de IA\n     - [ ] Lista de Cálculo")
            
        else:
            # A função foi chamada, mas o comando não é para este atuador
            # (Útil se você tivesse múltiplos atuadores)
            pass
            
    except Exception as e:
        print(f"[ATUADOR TUTOR]: Erro ao processar comando '{' '.join(comando_completo)}': {e}")