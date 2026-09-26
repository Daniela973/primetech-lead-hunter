elif menu == "🎯 CRM e Qualificação":
    st.header("🎯 CRM de Leads e Qualificação")
    st.write("Gerenciamento e listagem dos leads capturados e armazenados no banco de dados:")

    try:
        from banco.models import Lead
        from flask import Flask
        import pandas as pd
        
        # Cria uma instância temporária do app Flask para fornecer o contexto do banco de dados
        app_flask = Flask(__name__)
        app_flask.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db' # Ajuste se o seu config usar outro caminho
        
        with app_flask.app_context():
            leads_db = Lead.query.all()

            if leads_db:
                lista_dados = []
                for l in leads_db:
                    lista_dados.append({
                        "ID": l.id,
                        "Empresa": l.nome,
                        "Segmento": l.segmento,
                        "Cidade": l.cidade,
                        "WhatsApp": l.whatsapp,
                        "Score": l.pontuacao,
                        "Classificação": l.classificacao
                    })
                df_leads = pd.DataFrame(lista_dados)
                st.dataframe(df_leads, use_container_width=True)
            else:
                st.info("O banco de dados está conectado com sucesso, mas ainda não há leads salvos. Utilize a 'Captura Automática' para adicionar registros.")

    except Exception as e:
        st.warning(f"Aviso de contexto do banco: {e}. Exibindo modo de compatibilidade.")
        import pandas as pd
        dados_exemplo = pd.DataFrame({
            "Empresa": ["Pizzaria Bella", "Salão Glamour", "Clínica Vida"],
            "Segmento": ["Restaurantes", "Salões", "Clínicas"],
            "Cidade": ["Palmas - TO", "Gurupi - TO", "Paraíso - TO"],
            "Score": [85, 72, 68],
            "Status": ["🔥 Quente", "🟡 Morno", "⚪ Frio"]
        })
        st.dataframe(dados_exemplo, use_container_width=True)
