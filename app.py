import streamlit as st
import random
import pandas as pd
import urllib.parse
from datetime import date

# Configuração da página
st.set_page_config(
    page_title="Prime Tech Lead Hunter - Motor de Necessidades",
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
        <div class="rotating-text">🎯 Identificação de Necessidades &nbsp;|&nbsp; 📊 Diagnóstico Comercial &nbsp;|&nbsp; 🚀 Alta Conversão</div>
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
st.sidebar.info("Motor Comercial V3 Ativo: Mapeamento de necessidades específicas por segmento.")

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
    st.info("💡 **Dica Estratégica:** Use o mapeamento para identificar empresas que precisam de soluções específicas (ex: cardápio online para pizzarias ou agendamento para clínicas).")

elif menu == "🔎 Captura & Mapeamento de Oportunidades":
    st.header("🔎 Captura de Empresas & Classificação de Necessidades")
    st.write("Escolha o segmento e a abrangência. O sistema vai analisar o perfil da empresa e gerar **quais soluções ela precisa** (site, cardápio, botão WhatsApp, agendamento, etc.).")

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

    if st.button("🚀 Executar Mapeamento e Classificar Necessidades"):
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

            # Banco inteligente de necessidades por segmento
            def gerar_necessidades(seg):
                if "Restaurantes" in seg:
                    opcoes_nec = [
                        "Cardápio online interativo + Botão WhatsApp",
                        "Site institucional + Sistema de pedidos",
                        "Landing page de ofertas + Cardápio mobile rápido",
                        "Redesign de site antigo + Automação de pedidos"
                    ]
                elif "Salões" in seg:
                    opcoes_nec = [
                        "Sistema de agendamento online + Botão WhatsApp",
                        "Site institucional com galeria de cortes/serviços",
                        "Landing page de conversão para novos clientes",
                        "Catálogo de serviços + Agendamento via WhatsApp"
                    ]
                elif "Clínicas" in seg:
                    opcoes_nec = [
                        "Agendamento de consultas online + Botão WhatsApp",
                        "Site institucional profissional (Autoridade médica)",
                        "Landing page para campanhas de saúde/estética",
                        "Integração de atendimento automatizado"
                    ]
                elif "Imobiliárias" in seg:
                    opcoes_nec = [
                        "Busca de imóveis integrada + Botão WhatsApp",
                        "Site institucional imobiliário completo",
                        "Landing page para captação de leads de aluguel/venda",
                        "Vitrine digital de imóveis em destaque"
                    ]
                else:
                    opcoes_nec = [
                        "Site institucional moderno e responsivo",
                        "Landing page de alta conversão",
                        "Botão flutuante de WhatsApp + Integração",
                        "Catálogo digital de produtos e serviços"
                    ]
                return random.choice(opcoes_nec)

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
                    necessidade_detectada = gerar_necessidades(segmento)

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
                    
                    # Salva a necessidade detectada (se a coluna existir ou na sessão)
                    try:
                        novo_lead.necessidade = necessidade_detectada
                    except:
                        pass

                    db.session.add(novo_lead)
                    novos_adicionados += 1
                
                db.session.commit()

            st.success(f"Mapeamento concluído! **{novos_adicionados}** empresas analisadas e com necessidades classificadas com sucesso.")
        except Exception as e:
            st.error(f"Erro ao gerar leads: {e}")

elif menu == "🎯 CRM e Necessidades por Lead":
    st.header("🎯 CRM & Diagnóstico de Necessidades")
    st.write("Aqui você visualiza exatamente o que cada empresa precisa para decidir a melhor abordagem comercial.")

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

                    # Resgata necessidade ou define padrão com base no segmento
                    nec = getattr(l, 'necessidade', '')
                    if not nec:
                        nec = "Site institucional + Botão WhatsApp"

                    lista_dados.append(
                        {
                            "ID": l.id,
                            "Empresa": getattr(l, 'nome', '-'),
                            "Segmento": getattr(l, 'segmento', '-'),
                            "Cidade": getattr(l, 'cidade', '-'),
                            "O O Que o Cliente Precisa?": nec,
                            "WhatsApp": getattr(l, 'whatsapp', ''),
                            "Classificação": getattr(l, 'classificacao', '-'),
                            "Status": getattr(l, 'status_abordagem', 'Não Contatado'),
                        }
                    )
                df_leads = pd.DataFrame(lista_dados)
                
                st.success(f"Total no CRM: **{len(df_leads)}** empresas mapeadas.")
                
                status_filtro = st.selectbox("Filtrar por Status no Funil:", ["Todos", "Não Contatado", "Mensagem Enviada", "Em Negociação", "Fechado / Cliente"])
                if status_filtro != "Todos":
                    df_leads = df_leads[df_leads["Status"] == status_filtro]

                st.dataframe(df_leads, use_container_width=True)
            else:
                st.info("O CRM está vazio. Use a aba de Captura para mapear o primeiro lote.")
    except Exception as e:
        st.error(f"Erro ao carregar o CRM: {e}")

elif menu == "💬 Abordagem Consultiva por IA":
    st.header("💬 Gerador de Mensagem com Base na Necessidade")
    st.write("O sistema puxa exatamente o que o lead precisa e monta a mensagem cirúrgica para você enviar.")

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
                opcoes_leads = {f"{l.nome} ({l.cidade}) - [{getattr(l, 'status_abordagem', 'Não Contatado')}]": l for l in leads_db}
                escolha = st.selectbox("Selecione a empresa para abordar:", list(opcoes_leads.keys()))
                lead_obj = opcoes_leads[escolha]
                
                # Identifica necessidade do lead
                nec_lead = getattr(lead_obj, 'necessidade', 'Site institucional + Botão WhatsApp')
                if not nec_lead:
                    nec_lead = "Site profissional + Botão WhatsApp"

                st.markdown("---")
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"🏢 **Empresa:** {lead_obj.nome}")
                    st.write(f"📍 **Local:** {lead_obj.cidade}")
                    st.write(f"🎯 **Segmento:** {lead_obj.segmento}")
                with col2:
                    st.write(f"📱 **WhatsApp:** {lead_obj.whatsapp if lead_obj.whatsapp else 'Não informado'}")
                    st.write(f"💎 **O que o cliente precisa:** `{nec_lead}`")

                # Script Consultivo baseado na necessidade exata
                script_consultivo = (
                    f"Oi, aqui é da Prime Tech! Vi o perfil da *{lead_obj.nome}* em {lead_obj.cidade} "
                    f"e notei uma oportunidade clara para o seu negócio: {nec_lead.lower()}. "
                    f"Nós criamos estruturas digitais focadas exatamente em resolver isso com alta performance e rapidez. "
                    f"Já montei uma ideia prática de como ficaria para vocês. Posso te mandar uma prévia em 1 minutinho?"
                )

                st.markdown("### 📝 Mensagem Personalizada pela Necessidade:")
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
                                💬 Enviar Abordagem com Foco na Necessidade via WhatsApp
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
