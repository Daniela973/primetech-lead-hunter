from flask import Flask, render_template_string, redirect, url_for
from config import Config
from banco.database import db
from banco.models import Lead
from qualificacao.analisador import analisar_site, analisar_redes_sociais
from qualificacao.pontuacao import calcular_pontuacao, classificar_lead

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
            body { font-family: Arial, sans-serif; margin: 40px; background: #f4f6f9; color: #333; }
            h1 { color: #0f172a; }
            .cards { display: flex; gap: 20px; margin-bottom: 30px; }
            .card { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); flex: 1; text-align: center; }
            table { width: 100%; border-collapse: collapse; background: white; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
            th, td { padding: 12px 15px; text-align: left; border-bottom: 1px solid #ddd; }
            th { background: #1e293b; color: white; }
            .btn { background: #3b82f6; color: white; padding: 10px 15px; text-decoration: none; border-radius: 4px; display: inline-block; margin-bottom: 20px; font-weight: bold;}
        </style>
    </head>
    <body>
        <h1>🚀 PRIME TECH — LEAD HUNTER</h1>
        <a href="/simular_busca" class="btn">🔍 Simular Nova Captura Automática</a>
        
        <div class="cards">
            <div class="card"><h3>Total Leads</h3><p>{{ total }}</p></div>
            <div class="card" style="color: #dc2626;"><h3>🔥 Quentes</h3><p>{{ quentes }}</p></div>
            <div class="card" style="color: #d97706;"><h3>🟡 Mornos</h3><p>{{ mornos }}</p></div>
            <div class="card" style="color: #64748b;"><h3>⚪ Frios</h3><p>{{ frios }}</p></div>
        </div>

        <h2>📊 Base de Leads Cadastrados</h2>
        <table>
            <tr>
                <th>Nome</th>
                <th>Segmento</th>
                <th>Cidade</th>
                <th>Website</th>
                <th>Instagram</th>
                <th>Classificação</th>
                <th>Status CRM</th>
            </tr>
            {% for l in leads %}
            <tr>
                <td>{{ l.nome }}</td>
                <td>{{ l.segmento }}</td>
                <td>{{ l.cidade }}</td>
                <td>{{ l.website or 'Não possui' }}</td>
                <td>{{ l.instagram or 'Não possui' }}</td>
                <td><b>{{ l.classificacao }}</b></td>
                <td>{{ l.status_crm }}</td>
            </tr>
            {% endfor %}
        </table>
    </body>
    </html>
    """
    return render_template_string(html, total=total_encontrados, quentes=quentes, mornos=mornos, frios=frios, leads=leads)

@app.route('/simular_busca')
def simular_busca():
    exemplo_lead = {
        "nome": "Pizzaria Bella Vista",
        "segmento": "Pizzarias",
        "cidade": "Palmas - TO",
        "telefone": "63999998888",
        "whatsapp": "63999998888",
        "website": "", # Sem site vira um lead super quente para você vender um site!
        "instagram": "@pizzariabellavista",
        "endereco": "Av. JK, 1000"
    }
    
    analise = analisar_site(exemplo_lead["website"])
    possui_insta = analisar_redes_sociais(exemplo_lead["instagram"])
    pontos = calcular_pontuacao(analise, possui_insta)
    classificacao = classificar_lead(pontos)
    
    novo = Lead(
        nome=exemplo_lead["nome"],
        segmento=exemplo_lead["segmento"],
        cidade=exemplo_lead["cidade"],
        telefone=exemplo_lead["telefone"],
        whatsapp=exemplo_lead["whatsapp"],
        website=exemplo_lead["website"],
        instagram=exemplo_lead["instagram"],
        endereco=exemplo_lead["endereco"],
        origem="Busca Automática",
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

if __name__ == '__main__':
    app.run(debug=True, port=5000)
