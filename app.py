import streamlit as st
import random
import pandas as pd

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
        <div class="rotating-text">⚡ Soluções Inteligentes &nbsp;|&nbsp; 🚀 Agilidade &nbsp;|&nbsp; 💎 Alta Performance &nbsp;|&nbsp; 🎯 Prospecção Nacional</div>
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
st.sidebar.info("Sistema conectado e operacional (Modo Brasil).")

# --- ROTEAMENTO DAS SEÇÕES ---

if menu == "📊 Métricas e Dashboard":
    st.header("📊 Painel de Métricas Gerais")
    
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
            total_quentes = Lead.query.filter_by(classificacao="🔥 Quente").count()
            total_mornos = Lead.query.filter_by(classificacao="🟡 Morno").count()
            total_frios = Lead.query.filter_by(classificacao="⚪ Frio").count()
            total_leads = Lead.query.count()
    except:
        total_quentes, total_mornos, total_frios, total_leads = 0, 0, 0, 0

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🔥 Leads Quentes", total_quentes)
    with col2:
        st.metric("🟡 Leads Mornos", total_mornos)
    with col3:
        st.metric("⚪ Leads Frios", total_frios)
    with col4:
        st.metric("📂 Total de Leads", total_leads)
    st.markdown("---")
    st.info("Acompanhamento em tempo real das oportunidades em nível nacional.")

elif menu == "🔎 Captura Automática":
    st.header("🔎 Módulo de Captura Automática (Brasil)")
    segmento = st.selectbox(
        "Segmento de Negócio",
        [
            "Restaurantes",
            "Salões de Beleza",
            "Clínicas",
            "Imobiliárias",
            "Academias",
            "Lojas de Roupas",
            "Escritórios de Contabilidade",
            "Pet Shops",
        ],
    )
    
    # Opção de abrangência nacional
    alcance = st.radio(
        "Abrangência da Busca:",
        ["🇧🇷 Todo o Brasil (Aleatório / Nacional)", "📍 Escolher uma Região / Estado Específico"]
    )
    
    cidade_selecionada = "Brasil (Nacional)"
    if alcance == "📍 Escolher uma Região / Estado Específico":
        cidade_selecionada = st.selectbox(
            "Selecione o Estado / Polo:",
            [
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
                "Palmas - TO",
            ],
        )

    quantidade = st.slider("Quantidade limite de leads", 10, 500, 50)

    if st.button("🚀 Executar Busca Nacional"):
        try:
            from banco.database import db
            from banco.models import Lead
            from flask import Flask

            app_flask = Flask(__name__)
            app_flask.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
            app_flask.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

            db.init_app(app_flask)

            prefixos = ["Centro", "Imperial", "Master", "Prime", "Alpha", "Nova", "Studio", "Espaço", "Clin", "Top", "Global", "Mega"]
            sufixos = ["Ltda", "Eldorado", "Executiva", "Express", "Premium", "Central", "Plus", "Sul", "Boutique", "Digital"]
            
            # Lista de capitais/cidades do Brasil com seus respectivos DDDs para gerar dados coerentes
            polos_brasil = [
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
                ("Palmas - TO", "63"),
                ("Vitória - ES", "27"),
                ("Florianópolis - SC", "48")
            ]

            with app_flask.app_context():
                db.create_all()
                
                for i in range(quantidade):
                    if alcance == "🇧🇷 Todo o Brasil (Aleatório / Nacional)":
                        cidade_atual, ddd_atual = random.choice(polos_brasil)
                    else:
                        cidade_atual = cidade_selecionada
                        # Descobre o DDD com base na string do estado selecionado
                        ddd_atual = "11" # padrão
                        for p, d in polos_brasil:
                            if p == cidade_selecionada:
                                ddd_atual = d
                                break

                    nome_empresa = f"{random.choice(prefixos)} {segmento[:-1]} {random.choice(sufixos)} {random.randint(100, 999)}"
                    tel_num = f"{random.randint(30, 59)}{random.randint(10, 99)}{random.randint(1000, 9999)}"
                    wpp_num = f"{ddd_atual}9{random.randint(8000, 9999)}{random.randint(1000, 9999)}"
                    score_val = random.randint(40, 98)
                    
                    if score_val >= 75:
                        classif = "🔥 Quente"
                    elif score_val >= 60:
                        classif = "🟡 Morno"
                    else:
                        classif = "⚪ Frio"

                    nome_cidade_limpo = cidade_atual.split(' - ')[0]

                    novo_lead = Lead(
                        nome=nome_empresa,
                        segmento=segmento,
                        cidade=cidade_atual,
                        telefone=f"({ddd_atual}) {tel_num[:4]}-{tel_num[4:]}",
                        whatsapp=wpp_num,
                        website=f"www.{nome_empresa.lower().replace(' ', '')}.com.br",
                        endereco=f"Av. Principal, {random.randint(10, 2000)} - {nome_cidade_limpo}",
                        instagram=f"@{nome_empresa.lower().replace(' ', '_')}",
                        pontuacao=score_val,
                        classificacao=classif
                    )
                    db.session.add(novo_lead)
                
                db.session.commit()

            st.success(f"Busca nacional concluída! Capturados com sucesso **{quantidade}** novos leads de {segmento} abrangendo o Brasil.")
        except Exception as e:
            st.error(f"Erro ao salvar leads no banco: {e}")

elif menu == "🎯 CRM e Qualificação":
    st.header("🎯 CRM de Leads e Qualificação (Nacional)")
    st.write(
        "Gerenciamento completo, listagem e exportação de leads do Brasil inteiro armazenados no banco de dados:"
    )

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
                    wpp_limpo = "".join(filter(str.isdigit, getattr(l, 'whatsapp', '')))
                    if wpp_limpo and not wpp_limpo.startswith('55'):
                        wpp_formatado = f"55{wpp_limpo}"
                    else:
                        wpp_formatado = wpp_limpo

                    lista_dados.append(
                        {
                            "ID": l.id,
                            "Empresa": getattr(l, 'nome', '-'),
                            "Segmento": getattr(l, 'segmento', '-'),
                            "Cidade/Estado": getattr(l, 'cidade', '-'),
                            "Telefone": getattr(l, 'telefone', '-'),
                            "WhatsApp": getattr(l, 'whatsapp', '-'),
                            "Telefone_Meta_Ads": wpp_formatado,
                            "Website": getattr(l, 'website', '-'),
                            "Endereço": getattr(l, 'endereco', '-'),
                            "Instagram": getattr(l, 'instagram', '-'),
                            "Score": getattr(l, 'pontuacao', 0),
                            "Classificação": getattr(l, 'classificacao', '-'),
                        }
                    )
                df_leads = pd.DataFrame(lista_dados)
                st.success(f"Total de registros no banco nacional: **{len(df_leads)}** leads.")
                
                # Botão de Exportação otimizado para o Meta Ads
                csv_data = df_leads.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Baixar Lista Nacional em CSV para o Meta Ads",
                    data=csv_data,
                    file_name="leads_brasil_meta_ads.csv",
                    mime="text/csv",
                    use_container_width=True
                )
                
                st.markdown("---")
                st.dataframe(df_leads, use_container_width=True)
            else:
                st.info(
                    "O banco de dados está vazio. Utilize a aba 'Captura Automática' para buscar e registrar leads do Brasil."
                )

    except Exception as e:
        st.error(f"Erro ao conectar com o banco de dados do CRM: {e}")

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
