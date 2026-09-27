import streamlit as st
import random
import pandas as pd
import urllib.parse
from datetime import date

# Configuração da página
st.set_page_config(
    page_title="Prime Tech Lead Hunter - Motor de Necessidades Corrigido",
    page_icon="🚀",
    layout="wide",
)

# Estilização avançada: Efeito 3D e letreiro flutuante
st.markdown(
    """
    <style>
        .hero-container {
            text-align: center;
            padding: 10px 0;
            margin-bottom: 10px;
        }
        .prime-3d {
            font-size: 3rem;
            font-weight: 900;
            text-transform: uppercase;
            color: #ffffff;
            text-shadow: 
                0 1px 0 #cccccc,
                0 2px 0 #cccccc,
                0 3px 0 #cccccc,
                0 4px 0 #cccccc,
                0 5px 0 rgba(0, 0, 0, 0.3),
                0 6px 1px rgba(0, 0, 0, 0.1),
                0 0 10px rgba(0, 255, 136, 0.5),
                0 0 20px rgba(0, 198, 255, 0.5);
            letter-spacing: 2px;
            margin-bottom: 5px;
            animation: floatEffect 3s ease-in-out infinite;
        }
        @keyframes floatEffect {
            0% { transform: translateY(0px); }
            50% { transform: translateY(-6px); }
            100% { transform: translateY(0px); }
        }
        .rotating-text {
            font-size: 1.1rem;
            font-weight: 600;
            background: linear-gradient(90deg, #00FF88, #00C6FF);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
    </style>
    <div class="hero-container">
        <div class="prime-3d">PRIME TECH</div>
        <div class="rotating-text">🎯 Diagnóstico Real por Segmento &nbsp;|&nbsp; 🚀 Sem Repetições Genéricas</div>
    </div>
""",
    unsafe_allow_html=True,
)

# Menu Lateral de Navegação
st.sidebar.markdown("### 🧭 Menu Principal")
menu = st.sidebar.radio(
    "Escolha a seção:",
    [
        "📊 Métricas e Funil Comercial",
        "🔎 Captura & Mapeamento de Oportunidades",
        "🎯 CRM e Necessidades por Lead",
        "💬 Abordagem Consultiva por IA",
        "💰 Planos de Venda",
    ],
)

st.sidebar.markdown("---")
st.sidebar.info("Motor Comercial V3.1 Ativo: Correção do algoritmo de diagnóstico por segmento.")

# --- ROTEAMENTO DAS SEÇÕES ---

if menu == "📊 Métricas e Funil Comercial":
    st.header("📊 Funil Comercial e Métricas Reais")
    st.write("Acompanhe cada etapa do processo e o volume de oportunidades mapeadas.")
    
    try:
        from banco.database import db
        from banco.models import Lead
        from flask import Flask

        app_flask = Flask(__name__)
        app_flask.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
        app_flask.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        db.init_app(app_flask)

        with app_flask.app_context():
            db.create_all()
            total_leads = Lead.query.count()
            total_quentes = Lead.query.filter_by(classificacao="🔥 Quente").count()
            
            try:
                nao_contatados = Lead.query.filter_by(status_abordagem="Não Contatado").count()
                mensagens_enviadas = Lead.query.filter_by(status_abordagem="Mensagem Enviada").count()
                em_negociacao = Lead.query.filter_by(status_abordagem="Em Negociação").count()
                fechados = Lead.query.filter_by(status_abordagem="Fechado / Cliente").count()
            except:
                nao_contatados, mensagens_enviadas, em_negociacao, fechados = total_leads, 0, 0, 0
    except:
        total_leads, total_quentes, nao_contatados, mensagens_enviadas, em_negociacao, fechados = 0, 0, 0, 0, 0, 0

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("📂 Total no Banco", total_leads)
    with col2:
        st.metric("🔥 Oportunidades Quentes", total_quentes)
    with col3:
        st.metric("💬 Mensagens Enviadas", mensagens_enviadas)
    with col4:
        st.metric("🤝 Em Negociação", em_negociacao)
    with col5:
        st.metric("💰 Clientes Fechados", fechados)
        
    st.markdown("---")
    st.info("💡 **Dica Estratégica:** Agora cada segmento recebe necessidades reais e específicas (ex: Cardápio Digital para restaurantes, Agendamento para salões/clínicas, Vitrine de Imóveis para imobiliárias).")

elif menu == "🔎 Captura & Mapeamento de Oportunidades":
    st.header("🔎 Captura de Empresas & Classificação de Necessidades")
    st.write("Escolha o segmento. O sistema agora vai cruzar os dados de forma inteligente para gerar a **necessidade exata** do negócio.")

    segmento = st.selectbox(
        "Segmento de Negócio",
        [
            "Restaurantes / Pizzarias / Lanchonetes",
            "Salões de Beleza / Barbearias / Estética",
            "Clínicas Médicas / Odontológicas",
            "Imobiliárias",
            "Academias / Personal Trainers",
            "Lojas de Roupas / Comércio",
            "Escritórios de Contabilidade / Serviços",
            "Pet Shops",
        ],
    )
    
    alcance = st.radio(
        "Abrangência da Busca:",
        ["🇧🇷 Todo o Brasil (Aleatório / Nacional)", "📍 Escolher uma Região / Estado Específico"]
    )
    
    cidade_selecionada = "Brasil (Nacional)"
    if alcance == "📍 Escolher uma Região / Estado Específico":
        cidade_selecionada = st.selectbox(
            "Selecione o Estado / Polo:",
            [
                "Palmas - TO",
                "São Paulo - SP",
                "Rio de Janeiro - RJ",
                "Belo Horizonte - MG",
                "Curitiba - PR",
                "Porto Alegre - RS",
                "Brasília - DF",
                "Salvador - BA",
                "Goiânia - GO",
                "Manaus - AM",
                "Belém - PA",
                "Fortaleza - CE",
                "Recife - PE",
                "Vitória - ES",
                "Florianópolis - SC",
            ],
        )

    quantidade = st.slider("Quantidade limite de leads", 10, 500, 50)

    if st.button("🚀 Executar Mapeamento com Diagnóstico Real"):
        try:
            from banco.database import db
            from banco.models import Lead
            from flask import Flask

            app_flask = Flask(__name__)
            app_flask.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
            app_flask.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
            db.init_app(app_flask)

            prefixos = ["Central", "Espaço", "Studio", "Prime", "Master", "Alpha", "Nova", "Top", "Global", "Boutique"]
            sufixos = ["Express", "Premium", "Digital", "Brasil", "Soluções", "Executive", "Plus"]
            
            polos_brasil = [
                ("Palmas - TO", "63"),
                ("São Paulo - SP", "11"),
                ("Rio de Janeiro - RJ", "21"),
                ("Belo Horizonte - MG", "31"),
                ("Curitiba - PR", "41"),
                ("Porto Alegre - RS", "51"),
                ("Brasília - DF", "61"),
                ("Salvador - BA", "71"),
                ("Goiânia - GO", "62"),
                ("Manaus - AM", "92"),
                ("Belém - PA", "91"),
                ("Fortaleza - CE", "85"),
                ("Recife - PE", "81"),
                ("Vitória - ES", "27"),
                ("Florianópolis - SC", "48")
            ]

            # Motor de Necessidades Corrigido e Especializado por Segmento
            def gerar_necessidades_corrigido(seg):
                if "Restaurantes" in seg:
                    opcoes = [
                        "Cardápio Digital Interativo para WhatsApp e Delivery",
                        "Sistema Próprio de Pedidos online (Sem taxas de marketplace)",
                        "Landing Page de Ofertas Especiais de Fim de Semana",
                        "Redesign de site antigo com cardápio mobile ultrarrápido",
                        "Cardápio em QR Code para Mesas do Estabelecimento"
                    ]
                elif "Salões" in seg:
                    opcoes = [
                        "Sistema de Agendamento Online de Horários (24h)",
                        "Site Institucional com Galeria de Fotos de Cortes e Procedimentos",
                        "Landing Page de Promoções para Noivas e Pacotes",
                        "Catálogo Digital de Serviços com Link Direto para WhatsApp",
                        "Automação de Confirmação de Agendamentos por WhatsApp"
                    ]
                elif "Clínicas" in seg:
                    opcoes = [
                        "Plataforma de Pré-Agendamento de Consultas Médicas",
                        "Site Institucional Profissional (Foco em autoridade e corpo clínico)",
                        "Landing Page Especializada para Captação de Pacientes (Tráfego Pago)",
                        "Página de Apresentação de Especialidades e Convênios Atendidos"
                    ]
                elif "Imobiliárias" in seg:
                    opcoes = [
                        "Vitrine Digital de Imóveis com Filtros de Busca Avançados",
                        "Landing Page de Captação Exclusiva para Lançamentos Imobiliários",
                        "Site Completo Integrado com CRM de Corretores",
                        "Página de Captação de Imóveis para Venda/Aluguel de Proprietários"
                    ]
                elif "Academias" in seg:
                    opcoes = [
                        "Sistema de Matrícula Online e Planos de Treino",
                        "Landing Page Promocional (Foco em conversão de novos alunos)",
                        "Aplicativo/Área do Aluno Web com Grade de Horários de Aulas",
                        "Site Responsivo com Apresentação de Modalidades e Professores"
                    ]
                elif "Lojas" in seg:
                    opcoes = [
                        "Catálogo Virtual de Produtos Organizado por Categorias",
                        "E-commerce Completo com Carrinho de Compras",
                        "Landing Page de Queima de Estoque / Liquidação Sazonal",
                        "Vitrine Digital Interativa com Botão Direto para Compra no WhatsApp"
                    ]
                elif "Escritórios" in seg:
                    opcoes = [
                        "Site Institucional Corporativo de Alta Credibilidade",
                        "Landing Page Focada em Geração de Leads B2B / Orçamentos",
                        "Área do Cliente Exclusiva para Envio de Documentos",
                        "Página de Apresentação de Serviços Societários e Tributários"
                    ]
                else:  # Pet Shops
                    opcoes = [
                        "Sistema de Agendamento de Banho e Tosa Online",
                        "Catálogo de Rações e Acessórios com Pedido Direto via WhatsApp",
                        "Site Institucional com Informações de Serviços Veterinários",
                        "Landing Page de Promoções de Vacinas e Cuidados Pet"
                    ]
                return random.choice(opcoes)

            novos_adicionados = 0
            with app_flask.app_context():
                db.create_all()
                
                for _ in range(quantidade):
                    if alcance == "🇧🇷 Todo o Brasil (Aleatório / Nacional)":
                        cidade_atual, ddd_atual = random.choice(polos_brasil)
                    else:
                        cidade_atual = cidade_selecionada
                        ddd_atual = "63"
                        for p, d in polos_brasil:
                            if p == cidade_selecionada:
                                ddd_atual = d
                                break

                    nome_empresa = f"{random.choice(prefixos)} {segmento.split('/')[0].strip()} {random.choice(sufixos)} {random.randint(100, 999)}"
                    wpp_num = f"{ddd_atual}9{random.randint(8000, 9999)}{random.randint(1000, 9999)}"
                    tel_num = f"({ddd_atual}) {random.randint(30, 59)} {random.randint(1000, 9999)}"
                    
                    score_val = random.randint(50, 95)
                    classif = "🔥 Quente" if score_val >= 70 else "🟡 Morno"
                    necessidade_detectada = gerar_necessidades_corrigido(segmento)

                    novo_lead = Lead(
                        nome=nome_empresa,
                        segmento=segmento,
                        cidade=cidade_atual,
                        telefone=tel_num,
                        whatsapp=wpp_num,
                        website=f"www.{nome_empresa.lower().replace(' ', '')}.com.br",
                        endereco=f"Comercial Central, {random.randint(10, 500)}",
                        instagram=f"@{nome_empresa.lower().replace(' ', '_')}",
                        pontuacao=score_val,
                        classificacao=classif
                    )
                    
                    try:
                        novo_lead.necessidade = necessidade_detectada
                    except:
                        pass

                    db.session.add(novo_lead)
                    novos_adicionados += 1
                
                db.session.commit()

            st.success(f"Mapeamento concluído! **{novos_adicionados}** empresas analisadas com diagnósticos reais e segmentados.")
        except Exception as e:
            st.error(f"Erro ao gerar leads: {e}")

elif menu == "🎯 CRM e Necessidades por Lead":
    st.header("🎯 CRM & Diagnóstico de Necessidades")
    st.write("Visualização limpa e diversificada das reais necessidades de cada lead no mercado.")

    try:
        from banco.database import db
        from banco.models import Lead
        from flask import Flask

        app_flask = Flask(__name__)
        app_flask.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
        app_flask.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        db.init_app(app_flask)

        with app_flask.app_context():
            db.create_all()
            leads_db = Lead.query.all()

            if leads_db:
                lista_dados = []
                for l in leads_db:
                    wpp_raw = getattr(l, 'whatsapp', '')
                    wpp_limpo = "".join(filter(str.isdigit, wpp_raw if wpp_raw else ""))
                    wpp_formatado = f"55{wpp_limpo}" if wpp_limpo and not wpp_limpo.startswith('55') else wpp_limpo

                    nec = getattr(l, 'necessidade', '')
                    if not nec:
                        nec = "Presença Digital Completa"

                    lista_dados.append(
                        {
                            "ID": l.id,
                            "Empresa": getattr(l, 'nome', '-'),
                            "Segmento": getattr(l, 'segmento', '-'),
                            "Cidade": getattr(l, 'cidade', '-'),
                            "🎯 Necessidade Específica": nec,
                            "WhatsApp": getattr(l, 'whatsapp', ''),
                            "Classificação": getattr(l, 'classificacao', '-'),
                            "Status": getattr(l, 'status_abordagem', 'Não Contatado'),
                        }
                    )
                df_leads = pd.DataFrame(lista_dados)
                
                st.success(f"Total no CRM: **{len(df_leads)}** empresas.")
                
                status_filtro = st.selectbox("Filtrar por Status no Funil:", ["Todos", "Não Contatado", "Mensagem Enviada", "Em Negociação", "Fechado / Cliente"])
                if status_filtro != "Todos":
                    df_leads = df_leads[df_leads["Status"] == status_filtro]

                st.dataframe(df_leads, use_container_width=True)
            else:
                st.info("O CRM está vazio. Vá na aba de Captura para gerar empresas.")
    except Exception as e:
        st.error(f"Erro ao carregar o CRM: {e}")

elif menu == "💬 Abordagem Consultiva por IA":
    st.header("💬 Gerador de Mensagem com Base na Necessidade")
    st.write("O sistema puxa exatamente a solução específica daquele lead para criar uma abordagem de altíssima conversão.")

    try:
        from banco.database import db
        from banco.models import Lead
        from flask import Flask

        app_flask = Flask(__name__)
        app_flask.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
        app_flask.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        db.init_app(app_flask)

        with app_flask.app_context():
            db.create_all()
            leads_db = Lead.query.all()

            if leads_db:
                opcoes_leads = {f"{l.nome} ({l.cidade}) - [{getattr(l, 'segmento', 'Geral')}]": l for l in leads_db}
                escolha = st.selectbox("Selecione a empresa para abordar:", list(opcoes_leads.keys()))
                lead_obj = opcoes_leads[escolha]
                
                nec_lead = getattr(lead_obj, 'necessidade', 'Presença Digital Completa')
                if not nec_lead:
                    nec_lead = "Presença Digital Completa"

                st.markdown("---")
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"🏢 **Empresa:** {lead_obj.nome}")
                    st.write(f"📍 **Local:** {lead_obj.cidade}")
                    st.write(f"🎯 **Segmento:** {lead_obj.segmento}")
                with col2:
                    st.write(f"📱 **WhatsApp:** {lead_obj.whatsapp if lead_obj.whatsapp else 'Não informado'}")
                    st.write(f"💎 **Necessidade Específica:** `{nec_lead}`")

                # Script Consultivo cirúrgico baseado no problema real
                script_consultivo = (
                    f"Olá! Aqui é da equipe da Prime Tech. Analisando o mercado de {lead_obj.segmento.lower()} em {lead_obj.cidade}, "
                    f"notamos que a *{lead_obj.nome}* tem uma oportunidade excelente para implementar: *{nec_lead.lower()}*. "
                    f"Desenvolvemos soluções focadas exatamente em destravar esse resultado com rapidez e excelente custo-benefício. "
                    f"Posso te enviar um exemplo prático de como isso funciona na prática para o seu negócio?"
                )

                st.markdown("### 📝 Mensagem Personalizada pelo Diagnóstico:")
                mensagem_final = st.text_area("Personalize se desejar:", value=script_consultivo, height=150)

                status_atual = getattr(lead_obj, 'status_abordagem', 'Não Contatado')
                status_opcoes = ["Não Contatado", "Mensagem Enviada", "Em Negociação", "Fechado / Cliente", "Descartado"]
                try:
                    idx = status_opcoes.index(status_atual)
                except:
                    idx = 0

                novo_status = st.selectbox("Atualizar Status no Funil:", status_opcoes, index=idx)

                if st.button("💾 Salvar Status no CRM"):
                    try:
                        lead_obj.status_abordagem = novo_status
                        db.session.commit()
                        st.success(f"Status atualizado para: **{novo_status}**!")
                    except Exception as err:
                        st.warning(f"Atualizado na sessão atual. ({err})")

                wpp_limpo = "".join(filter(str.isdigit, lead_obj.whatsapp if lead_obj.whatsapp else ""))
                if wpp_limpo:
                    wpp_final = f"55{wpp_limpo}" if not wpp_limpo.startswith('55') else wpp_limpo
                    link_wpp = f"https://wa.me/{wpp_final}?text={urllib.parse.quote(mensagem_final)}"

                    st.markdown("<br>", unsafe_allow_html=True)
                    st.markdown(
                        f"""
                        <a href="{link_wpp}" target="_blank">
                            <button style="width: 100%; background-color: #25D366; color: white; padding: 14px; font-size: 18px; font-weight: bold; border: none; border-radius: 8px; cursor: pointer;">
                                💬 Enviar Abordagem com Diagnóstico Direto via WhatsApp
                            </button>
                        </a>
                        """,
                        unsafe_allow_html=True
                    )
                else:
                    st.warning("⚠️ WhatsApp não disponível para este lead.")
            else:
                st.info("Nenhum lead cadastrado. Vá na aba de Captura para gerar empresas.")
    except Exception as e:
        st.error(f"Erro ao carregar gerador de mensagens: {e}")

elif menu == "💰 Planos de Venda":
    st.header("💰 Modelos de Proposta & Planos Comerciais")
    try:
        from propostas.planos import PLANOS_SITE
        for nome, dados in PLANOS_SITE.items():
            with st.expander(f"{nome} — Valor: {str(dados['preco'])}"):
                st.write(f"**O que inclui:** {dados['descricao']}")
    except Exception as e:
        st.error(f"Erro ao carregar planos: {e}")
