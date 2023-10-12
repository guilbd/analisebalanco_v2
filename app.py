from flask import Flask, render_template, request

app = Flask(__name__)

def calc_indices_financeiros(data):
    # Extrair dados do formulário
    ativo_circulante = float(data['ativo_circulante'])
    estoque = float(data['estoque'])
    ativo_nao_circulante = float(data['ativo_nao_circulante'])
    passivo_circulante = float(data['passivo_circulante'])
    passivo_nao_circulante = float(data['passivo_nao_circulante'])
    patrimonio_liquido = float(data['patrimonio_liquido'])
    receita_liquida = float(data['receita_liquida'])
    custo_produtos_vendidos = float(data['custo_produtos_vendidos'])
    despesas_operacionais = float(data['despesas_operacionais'])
    despesas_financeiras = float(data['despesas_financeiras'])
    lucro_liquido = float(data['lucro_liquido'])

    # Calcula índices
    liquidez_corrente = ativo_circulante / passivo_circulante
    liquidez_seca = (ativo_circulante - estoque) / passivo_circulante
    margem_liquida = (lucro_liquido / receita_liquida) * 100
    roe = (lucro_liquido / patrimonio_liquido) * 100
    roa = (lucro_liquido / (ativo_circulante + ativo_nao_circulante)) * 100
    
    # EBITDA e Margem EBITDA
    ebitda = lucro_liquido + despesas_financeiras + despesas_operacionais
    margem_ebitda = (ebitda / receita_liquida) * 100

    indices = {
        'liquidez_corrente': liquidez_corrente,
        'liquidez_seca': liquidez_seca,
        'margem_liquida': margem_liquida,
        'roe': roe,
        'roa': roa,
        'ebitda': ebitda,
        'margem_ebitda': margem_ebitda
    }

    return indices

def recomenda(indices):
    recomendacoes = {}
    
    if indices['liquidez_corrente'] >= 1:
        recomendacoes['liquidez_corrente'] = ("Boa Liquidez Corrente. A empresa possui ativos suficientes para cobrir suas dívidas de curto prazo.")
    else:
        recomendacoes['liquidez_corrente'] = ("Baixa Liquidez Corrente. A empresa pode ter problemas para cobrir suas dívidas de curto prazo.")
        
    # Liquidez Seca
    if indices['liquidez_seca'] >= 1:
        recomendacoes['liquidez_seca'] = ("Boa Liquidez Seca. A empresa tem capacidade de pagar suas dívidas de curto prazo, mesmo sem depender da venda de estoques.")
    else:
        recomendacoes['liquidez_seca'] = ("Baixa Liquidez Seca. A empresa pode enfrentar problemas se não conseguir vender seu estoque rapidamente.")
        
    # Margem Líquida
    if indices['margem_liquida'] > 0:
        recomendacoes['margem_liquida'] = ("Margem Líquida Positiva. A empresa é lucrativa.")
    else:
        recomendacoes['margem_liquida'] = ("Margem Líquida Negativa. A empresa não está gerando lucro.")
        
    # ROE
    if indices['roe'] > 0:
        recomendacoes['roe'] = ("ROE Positivo. A empresa está gerando retorno positivo sobre o patrimônio líquido.")
    else:
        recomendacoes['roe'] = ("ROE Negativo. A empresa está perdendo valor.")
        
    # ROA
    if indices['roa'] > 0:
        recomendacoes['roa'] = ("ROA Positivo. A empresa está usando seus ativos de forma eficaz para gerar lucro.")
    else:
        recomendacoes['roa'] = ("ROA Negativo. Os ativos da empresa não estão contribuindo para a geração de lucro.")
        
    # EBITDA
    if indices['ebitda'] > 0:
        recomendacoes['ebitda'] = ("EBITDA Positivo. A empresa tem um bom desempenho operacional antes de considerar as despesas financeiras.")
    else:
        recomendacoes['ebitda'] = ("EBITDA Negativo. A empresa pode estar enfrentando problemas em seu desempenho operacional.")

    # Margem EBITDA
    if indices['margem_ebitda'] > 0:
        recomendacoes['margem_ebitda'] = ("Margem EBITDA Positiva. A empresa está convertendo uma boa porcentagem da receita em EBITDA.")
    else:
        recomendacoes['margem_ebitda'] = ("Margem EBITDA Negativa. A empresa não está convertendo receita em EBITDA de forma eficaz.")

        
    return recomendacoes

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        data = request.form
        indices = calc_indices_financeiros(data)
        recomendacoes = recomenda(indices)
        return render_template('resultado.html', indices=indices, recomendacoes=recomendacoes)
        
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
