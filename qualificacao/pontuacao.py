def calcular_pontuacao(analise, possui_instagram):
    pontos = 0
    
    # Critérios de Oportunidade de Venda
    if not analise["possui_site"]:
        pontos += 40
    elif not analise["site_funcionando"]:
        pontos += 30
    elif not analise["https"]:
        pontos += 15
        
    if not analise["mobile"]:
        pontos += 15
        
    # Se tem rede social, demonstra que o negócio é ativo e quer clientes online
    if possui_instagram:
        pontos += 20
        
    return pontos

def classificar_lead(pontos):
    if pontos >= 50:
        return "🔥 lead quente"
    elif pontos >= 25:
        return "🟡 lead morno"
    else:
        return "⚪ lead frio"
