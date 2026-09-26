from flask import Flask, render_template_string, redirect, url_for
from config import Config
from banco.database import db
from banco.models import Lead
from qualificacao.analisador import analisar_site, analisar_redes_sociais
from qualificacao.pontuacao import calcular_pontuacao, classificar_lead
from captacao.buscador import BuscadorLeads
from captacao.deduplicador import remover_duplicados
from mensagens.modelos import gerar_mensagem_abordagem
from propostas.planos import PLANOS_SITE

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def dashboard():
    leads = Lead.query.all()
    total_encontrados = len(leads)
    quentes = Lead.query.filter_by(classificacao="🔥 lead quente").count()
    mornos = Lead.query.filter_by(classificacao="🟡 lead morno").count()
    frios = Lead.query.filter_by(classificacao="⚪ lead frio").count()
    
    html = """
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
        <meta charset="UTF-8">
        <title>Prime Tech — Lead Hunter</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 30px; background: #f4f6f9; color: #333; }
            h1 { color: #0f172a; }
            .cards { display: flex; gap: 15px; margin-bottom: 25px; flex-wrap: wrap; }
            .card { background: white; padding: 15px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); flex: 1; min-width: 120px; text-align: center; }
            table { width: 100%; border-collapse: collapse; background: white; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-top: 15px; font-size: 14px; }
            th, td { padding: 10px 12px; text-align: left; border-bottom: 1px solid #ddd; }
            th { background: #1e293b; color: white; }
            .btn { background: #3b82f6; color: white; padding: 10px 15px; text-decoration: none; border-radius: 4px; display: inline-block; margin-right: 10px; margin-bottom: 15px; font-weight: bold; }
            .btn-green { background: #10b981; }
            .msg-box { background: #fff; padding: 15px; border-left: 4px solid #3b82f6; margin-top: 20px; border-radius: 4px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
        </style>
    </head>
    <body>
        <h1>🚀 PRIME TECH — LEAD HUNTER</h1>
        <div>
            <a href="/executar_busca" class="btn">🔍 Executar Captura Automática</a>
            <a href="/ver_planos" class="btn btn-green">💰 Ver Planos de Venda</a>
        </div>
        
        <div class="cards">
            <div class="card"><h3>Total Leads</h3><p>{{ total }}</p></div>
            <div class="card" style="color: #dc2626;"><h3>🔥 Quentes</h3><p>{{ quentes }}</p></div>
            <div class="card" style="color: #d97706;"><h3>🟡 Mornos</h3><p>{{ mornos }}</p></div>
            <div class="card" style="color: #64748b;"><h3>⚪ Frios</h3><p>{{ frios }}</p></div>
        </div>

        <h2>📊 Base de Leads Cadastrados no CRM</h2>
        <table>
            <tr>
                <th>Nome</th>
                <th>Segmento</th>
                <th>Cidade</th>
                <th>Website</th>
                <th>Instagram</th>
                <th>Classificação</th>
                <th>Ações</th>
            </tr>
            {% for l in leads %}
            <tr>
                <td><b>{{ l.nome }}</b></td>
                <td>{{ l.segmento }}</td>
                <td>{{ l.cidade }}</td>
                <td>{{ l.website or 'Não possui' }}</td>
                <td>{{ l.instagram or 'Não possui' }}</td>
                <td><b>{{ l.classificacao }}</b></td>
                <td><a href="/mensagem/{{ l.id }}" style="color: #3b82f6; text-decoration: none; font-weight: bold;">💬 Ver Abordagem</a></td>
            </tr>
            {% endfor %}
        </table>
    </body>
    </html>
    """
    return render_template_string(html, total=total_encontrados, quentes=quentes, mornos=mornos, frios=frios, leads=leads)

@app.route('/executar_busca')
def executar_busca():
    # Executa a busca simulada utilizando o módulo buscador
    buscador = BuscadorLeads(segmento="Restaurantes", cidade="Palmas - TO")
    brutos = buscador.buscar_empresas()
    
    # Aplica deduplicação
    leads_unicos = remover_duplicados(brutos)
    
    for lead_data in leads_unicos:
        # Verifica se já existe no banco pelo nome
        existe = Lead.query.filter_by(nome=lead_data["nome"]).first()
        if not existe:
            analise = analisar_site(lead_data["website"])
            possui_insta = analisar_redes_sociais(lead_data["instagram"])
            pontos = calcular_pontuacao(analise, possui_insta)
            classificacao = classificar_lead(pontos)
            
            novo = Lead(
                nome=lead_data["nome"],
                segmento=lead_data["segmento"],
                cidade=lead_data["cidade"],
                telefone=lead_data["telefone"],
                whatsapp=lead_data["whatsapp"],
                website=lead_data["website"],
                instagram=lead_data["instagram"],
                endereco=lead_data["endereco"],
                origem="Buscador Automático",
                possui_site=analise["possui_site"],
                site_funcionando=analise["site_funcionando"],
                https=analise["https"],
                mobile=analise["mobile"],
                possui_instagram=possui_insta,
                pontuacao=pontos,
                classificacao=classificacao
            )
            db.session.add(novo)
    db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/mensagem/<int:lead_id>')
def ver_mensagem(lead_id):
    lead = Lead.query.get_or_404(lead_id)
    # Transforma o lead em dicionário para gerar a mensagem
    lead_dict = {
        "nome": lead.nome,
        "segmento": lead.segmento,
        "cidade": lead.cidade,
        "possui_site": lead.possui_site
    }
    mensagem = gerar_mensagem_abordagem(lead_dict)
    
    html = """
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
        <meta charset="UTF-8">
        <title>Mensagem de Abordagem - Prime Tech</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #f4f6f9; color: #333; }
            .box { background: white; padding: 25px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); max-width: 600px; }
            textarea { width: 100%%; height: 150px; padding: 10px; margin-top: 10px; border-radius: 4px; border: 1px solid #ddd; font-family: inherit; }
            .btn { background: #3b82f6; color: white; padding: 10px 15px; text-decoration: none; border-radius: 4px; display: inline-block; margin-top: 15px; font-weight: bold; }
        </style>
    </head>
    <body>
        <div class="box">
            <h2>💬 Sugestão de Abordagem para: {{ lead.nome }}</h2>
            <p>Copie a mensagem abaixo e envie no WhatsApp do cliente:</p>
            <textarea readonly>{{ mensagem }}</textarea>
            <br>
            <a href="/" class="btn">⬅️ Voltar ao Painel</a>
        </div>
    </body>
    </html>
    """
    return render_template_string(html, lead=lead, mensagem=mensagem)

@app.route('/ver_planos')
def ver_planos():
    html = """
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
        <meta charset="UTF-8">
        <title>Planos Comerciais - Prime Tech</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #f4f6f9; color: #333; }
            .planos-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-top: 20px; }
            .plano-card { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); border-top: 4px solid #10b981; }
            .btn { background: #3b82f6; color: white; padding: 10px 15px; text-decoration: none; border-radius: 4px; display: inline-block; margin-top: 20px; font-weight: bold; }
            .preco { font-size: 20px; color: #10b981; font-weight: bold; margin: 10px 0; }
        </style>
    </head>
    <body>
        <h1>💰 Tabela de Planos de Serviços Web</h1>
        <p>Apresente estas opções em negociações com os seus leads capturados:</p>
        
        <div class="planos-grid">
            {% for nome, info in planos.items() %}
            <div class="plano-card">
                <h3>{{ nome }}</h3>
                <div class="preco">{% if info.preco is number %}R$ {{ "%.2f"|format(info.preco) }}{% else %}{{ info.preco }}{% endif %}</div>
                <p>{{ info.descricao }}</p>
            </div>
            {% endfor %}
        </div>
        <br>
        <a href="/" class="btn">⬅️ Voltar ao Painel</a>
    </body>
    </html>
    """
    return render_template_string(html, planos=PLANOS_SITE)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
