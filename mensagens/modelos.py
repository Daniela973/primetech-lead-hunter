# Módulo de Mensagens e Abordagem Personalizada

def gerar_mensagem_abordagem(lead):
    """
    Gera uma mensagem personalizada para o WhatsApp do lead com base na análise,
    oferecendo os seus serviços de desenvolvimento de sites e sistemas.
    """
    nome_empresa = lead.get('nome', 'Empresa')
    segmento = lead.get('segmento', 'seu segmento')
    possui_site = lead.get('possui_site', False)
    
    if not possui_site:
        mensagem = (
            f"Olá, tudo bem? Aqui é da Prime Tech! "
            f"Notei que a *{nome_empresa}* é referência em {segmento} aqui em {lead.get('cidade')}, "
            f"mas percebi que vocês ainda não possuem um site profissional na internet. "
            f"Hoje em dia, muitos clientes procuram por {segmento} no Google e acabam fechando com a concorrência que aparece online. "
            f"Nós criamos sites modernos, rápidos e focados em trazer clientes para o seu negócio. "
            f"Podemos te mostrar uma demonstração gratuita de como ficaria um site para a {nome_empresa}?"
        )
    else:
        mensagem = (
            f"Olá, tudo bem? Sou da Prime Tech! "
            f"Estava analisando o site da *{nome_empresa}* e vi o trabalho incrível de vocês em {segmento}. "
            f"Nós desenvolvemos projetos de programação e melhorias avançadas (como otimização mobile, velocidade e sistemas personalizados) "
            f"que ajudam empresas como a de vocês a venderem muito mais na internet. "
            f"Vocês teriam 5 minutos esta semana para conhecer nossas soluções?"
        )
        
    return mensagem
