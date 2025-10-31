def iniciar_revisao():
   
    print("Atuador 'Revisão' iniciado.")
    return True

def atuar_sobre_revisao(acao, dispositivo, comando_completo):
   
    

    if acao == "adicionar" and dispositivo == "revisão":
        
  
        try:
       
            parametros = " ".join(comando_completo[2:]) 
            print(f"\n[ATUADOR REVISÃO]: Executando '{acao} {dispositivo}'")
            print(f"  -> ADICIONANDO REVISÃO: '{parametros}'")
        except Exception as e:
            print(f"[ATUADOR REVISÃO]: Erro ao processar 'adicionar revisão': {e}")
    
    else:
        pass 