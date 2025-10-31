def iniciar_plano():
 
    print("Atuador 'Plano' iniciado.")
    return True

def atuar_sobre_plano(acao, dispositivo, comando_completo):
   
    if acao == "mostrar" and dispositivo == "plano":
        
      
        print(f"\n[ATUADOR PLANO]: Executando '{acao} {dispositivo}'")
        print("  -> MOSTRANDO PLANO DE HOJE:\n     - 09:00: Aula de Redes Neurais\n     - 11:00: Estudar Cálculo")
    
    else:
       
        pass 