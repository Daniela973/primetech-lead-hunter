# Módulo de Filtro Automático e Deduplicação

def remover_duplicados(leads_lista):
    """
    Remove empresas duplicadas com base no nome e na cidade,
    garantindo que cada lead seja único na base.
    """
    vistos = set()
    unicos = []
    
    for lead in leads_lista:
        # Cria uma chave única com o nome e a cidade da empresa (em minúsculas)
        identificador = (
            lead.get('nome', '').lower().strip(), 
            lead.get('cidade', '').lower().strip()
        )
        
        if identificador not in vistos:
            vistos.add(identificador)
            unicos.append(lead)
            
    return unicos
