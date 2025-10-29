def iniciar_resumo():
    """
    Sinaliza que o atuador 'Resumo' está pronto.
    """
    print("Atuador 'Resumo' iniciado.")
    return True

def atuar_sobre_resumo(acao, dispositivo, comando_completo):
    """
    Verifica se o comando é para este atuador específico.
    """
    
    # Este atuador só responde se a 'acao' for 'gerar' E o 'dispositivo' for 'resumo'
    if acao == "gerar" and dispositivo == "resumo":
        
        # 'comando_completo' será algo como: ['gerar', 'resumo', 'atividades', 'pendentes']
        print(f"\n[ATUADOR RESUMO]: Executando '{acao} {dispositivo}'")
        print("  -> GERANDO RESUMO DE PENDÊNCIAS:\n     - [ ] Lista de Exercícios IA\n     - [ ] Projeto de Redes")
            
    else:
        pass