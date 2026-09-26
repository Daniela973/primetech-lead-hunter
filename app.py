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
        /* Container do Cabeçalho 3D */
        .hero-container {
            text-align: center;
            padding: 20px 0;
            margin-bottom: 20px;
        }

        /* Efeito 3D Chamativo para Prime Tech */
        .prime-3d {
            font-size: 3.5rem;
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
            margin-bottom: 10px;
            animation: floatEffect 3s ease-in-out infinite;
        }

        /* Animação suave flutuante */
        @keyframes floatEffect {
            0% { transform: translateY(0px); }
            50% { transform: translateY(-8px); }
            100% { transform: translateY(0px); }
        }

        /* Letreiro rotativo de frases */
        .rotating-text {
            font-size: 1.3rem;
            font-weight: 600;
            background: linear-gradient(90deg, #00FF88, #00C6FF);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            height: 35px;
            display: inline-block;
            animation: fadeInOut 4s ease-in-out infinite;
        }

        @keyframes fadeInOut {
            0% { opacity: 0; transform: scale(0.95); }
            50% { opacity: 1; transform: scale(1); }
            100% { opacity: 0; transform: scale(0.95); }
        }
    </style>

    <div class="hero-container">
        <div class="prime-3d">PRIME TECH</div>
        <div class="rotating-text">⚡ Soluções Inteligentes &nbsp;|&nbsp; 🚀 Agilidade &nbsp;|&nbsp; 💎 Alta Performance &nbsp;|&nbsp; 🎯 Prospecção Ativa</div>
    </div>
""",
    unsafe_allow_html=True,
)

# Menu Lateral (Intacto e focado na usabilidade)
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
st.sidebar.info("Sistema conectado e pronto para uso.")

# --- ROTEAMENTO DAS SEÇÕES DO SISTEMA ---

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
    cidade = st.text_input("Cidade e Estado", "Palmas - TO")
    quantidade = st.slider("Quantidade de Leads", 10, 200, 50)

    if st.button("🚀 Executar Busca Automática"):
        st.success(
            f"Iniciando busca por {segmento} em {cidade} (Limite: {quantidade})..."
        )

elif menu == "🎯 CRM e Qualificação":
    st.header("🎯 CRM de Leads e Qualificação")
    st.write(
        "Gerencie o estágio de cada lead, visualize scores e notas de qualificação."
    )

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
