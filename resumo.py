def iniciar_resumo():
   
    print("Atuador 'Resumo' iniciado.")
    return True

def atuar_sobre_resumo(acao, dispositivo, comando_completo):
  
    if acao == "gerar" and dispositivo == "resumo":
        
      
        print(f"\n[ATUADOR RESUMO]: Executando '{acao} {dispositivo}'")
        print("  -> GERANDO RESUMO DE PENDÊNCIAS:\n     - [ ] Lista de Exercícios IA\n     - [ ] Projeto de Redes")
            
    else:
        pass