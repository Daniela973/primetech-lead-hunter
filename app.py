import streamlit as st

# Configuração da página
st.set_page_config(
    page_title="Prime Tech Lead Hunter",
    page_icon="🚀",
    layout="wide",
)

# Estilização avançada: Efeito 3D para "Prime Tech" e letreiro flutuante de frases
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
        <div class="rotating-text">⚡ Soluções Inteligentes &nbsp;|&nbsp; 🚀 Agilidade &nbsp;|&nbsp; 💎 Alta Performance &nbsp;|&nbsp; 🎯 Prospecção Ativa</div>
    </div>
""",
    unsafe_allow_html=True,
)

# Menu Lateral de Navegação
st.sidebar.markdown("### 🧭 Menu Principal")
menu = st.sidebar.radio(
    "Escolha a seção:",
    [
        "📊 Métricas e Dashboard",
        "🔎 Captura Automática",
        "🎯 CRM e Qualificação",
        "💬 Mensagens e Abordagem",
        "💰 Planos de Venda",
    ],
)

st.sidebar.markdown("---")
st.sidebar.info("Sistema conectado e operacional.")

# --- ROTEAMENTO DAS SEÇÕES ---

if menu == "📊 Métricas e Dashboard":
    st.header("📊 Painel de Métricas Gerais")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🔥 Leads Quentes", "31")
    with col2:
        st.metric("🟡 Leads Mornos", "37")
    with col3:
        st.metric("⚪ Leads Frios", "20")
    with col4:
        st.metric("💰 Propostas", "5")
    st.markdown("---")
    st.info("Acompanhamento em tempo real das oportunidades.")

elif menu == "🔎 Captura Automática":
    st.header("🔎 Módulo de Captura Automática")
    segmento = st.selectbox(
        "Segmento de Negócio",
        [
            "Restaurantes",
            "Salões de Beleza",
            "Clínicas",
            "Imobiliárias",
            "Academias",
        ],
    )
    cidade = st.selectbox(
        "Cidade / Região",
        [
            "Palmas - TO",
            "Gurupi - TO",
            "Paraíso do Tocantins - TO",
            "Araguaína - TO",
        ],
    )
    quantidade = st.slider("Quantidade limite de leads", 10, 200, 50)

    if st.button("🚀 Executar Busca Automática"):
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
                
                # Adiciona alguns leads de exemplo baseados na busca para popular o banco
                exemplo_leads = [
                    Lead(nome=f"Empresa Exemplo 1 ({segmento})", segmento=segmento, cidade=cidade, whatsapp="63999991111", pontuacao=88, classificacao="🔥 Quente"),
                    Lead(nome=f"Comércio Local ({segmento})", segmento=segmento, cidade=cidade, whatsapp="63999992222", pontuacao=75, classificacao="🟡 Morno"),
                    Lead(nome=f"Serviços & Cia ({segmento})", segmento=segmento, cidade=cidade, whatsapp="63999993333", pontuacao=50, classificacao="⚪ Frio")
                ]
                
                for lead in exemplo_leads:
                    db.session.add(lead)
                db.session.commit()

            st.success(f"Busca concluída com sucesso para {segmento} em {cidade}! Novos leads adicionados ao CRM.")
        except Exception as e:
            st.error(f"Erro ao salvar leads no banco: {e}")

elif menu == "🎯 CRM e Qualificação":
    st.header("🎯 CRM de Leads e Qualificação")
    st.write(
        "Gerenciamento e listagem dos leads capturados e armazenados no banco de dados:"
    )

    try:
        from banco.database import db
        from banco.models import Lead
        from flask import Flask
        import pandas as pd

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
                    lista_dados.append(
                        {
                            "ID": l.id,
                            "Empresa": l.nome,
                            "Segmento": l.segmento,
                            "Cidade": l.cidade,
                            "WhatsApp": l.whatsapp,
                            "Score": l.pontuacao,
                            "Classificação": l.classificacao,
                        }
                    )
                df_leads = pd.DataFrame(lista_dados)
                st.dataframe(df_leads, use_container_width=True)
            else:
                st.info(
                    "O banco de dados está vazio. Utilize a aba 'Captura Automática' para buscar e salvar novos registros."
                )

    except Exception as e:
        st.warning(
            f"Aviso de contexto do banco: {e}. Exibindo modo de compatibilidade."
        )
        import pandas as pd

        dados_exemplo = pd.DataFrame(
            {
                "Empresa": [
                    "Pizzaria Bella",
                    "Salão Glamour",
                    "Clínica Vida",
                ],
                "Segmento": ["Restaurantes", "Salões", "Clínicas"],
                "Cidade": [
                    "Palmas - TO",
                    "Gurupi - TO",
                    "Paraíso - TO",
                ],
                "Score": [85, 72, 68],
                "Status": ["🔥 Quente", "🟡 Morno", "⚪ Frio"],
            }
        )
        st.dataframe(dados_exemplo, use_container_width=True)

elif menu == "💬 Mensagens e Abordagem":
    st.header("💬 Gerador de Abordagem Comercial")
    st.write(
        "Selecione um lead para gerar e copiar a mensagem de contato personalizada."
    )

elif menu == "💰 Planos de Venda":
    st.header("💰 Propostas e Planos Comerciais")
    try:
        from propostas.planos import PLANOS_SITE

        for nome, dados in PLANOS_SITE.items():
            with st.expander(
                f"{nome} — Preço: {str(dados['preco'])}"
            ):
                st.write(f"**Descrição:** {dados['descricao']}")
    except Exception as e:
        st.error(f"Erro ao carregar os planos: {e}")
