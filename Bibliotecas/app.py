import streamlit as st
import pandas as pd
import plotly.express as px

# 1. AJUSTE DO NOME DO APP (Mais simples e direto)
st.title("⚽ Football Analytics")
st.subheader("Painel de análise de atributos de atletas.")

# CARREGA OS DADOS (Função simples de cache)
@st.cache_data
def carregar_dados():
    return pd.read_csv("players_metrics.csv")

df_jogadores = carregar_dados()

# 2. FILTROS NA BARRA LATERAL
st.sidebar.header("🔍 Filtros")

# Filtro de País
paises = sorted(df_jogadores['País'].unique())
pais_selecionado = st.sidebar.selectbox("Selecione o País:", paises)

# Filtrando a tabela para mostrar apenas os jogadores do país escolhido com QUERY
df_pais = df_jogadores.query("País == @pais_selecionado")

# Filtro de Jogador
jogadores = sorted(df_pais['Nome'].unique())
jogador_selecionado = st.selectbox("Escolha o Atleta:", jogadores)

# Pegando a linha do jogador selecionado (Ficha individual)
dados_jogador = df_pais.query("Nome == @jogador_selecionado").iloc[0]

# 3. PERFIL DO JOGADOR (Visual em 3 colunas simples)
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    if pd.notna(dados_jogador['Foto_URL']):
        st.image(dados_jogador['Foto_URL'], width=150)
    else:
        st.warning("📷 Foto não disponível")

with col2:
    st.markdown(f"## {dados_jogador['Nome']}")
    st.write(f"🏃‍♂️ **Posição:** {dados_jogador['Posição']}")
    st.write(f"🏢 **Clube Atual:** {dados_jogador['Clube']}")
    st.write(f"🎂 **Idade:** {dados_jogador['Idade']} anos")

with col3:
    st.markdown("### 🏆 Copas do Mundo")
    copas = int(dados_jogador['Copas_Jogadas'])
    st.metric(label="Copas Disputadas", value=copas)

# 4. CAPTURANDO OS ATRIBUTOS INDIVIDUAIS
ritmo = dados_jogador['Ritmo']
finalizacao = dados_jogador['Finalização']
passe = dados_jogador['Passe']
drible = dados_jogador['Drible']
defesa = dados_jogador['Defesa']
fisico = dados_jogador['Físico']

# 5. CÁLCULOS ESTATÍSTICOS USANDO APENAS PANDAS
st.markdown("---")
st.markdown("### 📈 Resumo Estatístico")

atributos_jogador = dados_jogador[['Ritmo', 'Finalização', 'Passe', 'Drible', 'Defesa', 'Físico']]

# Calculamos a média e o valor máximo diretamente pelos métodos nativos do Pandas
media_geral = atributos_jogador.mean()
maior_nota = atributos_jogador.max()

# Descobrimos o nome do melhor atributo com a lógica IF/ELIF
melhor_atributo = ""
if maior_nota == ritmo:
    melhor_atributo = "Ritmo"
elif maior_nota == finalizacao:
    melhor_atributo = "Finalização"
elif maior_nota == passe:
    melhor_atributo = "Passe"
elif maior_nota == drible:
    melhor_atributo = "Drible"
elif maior_nota == defesa:
    melhor_atributo = "Defesa"
else:
    melhor_atributo = "Físico"

m1, m2 = st.columns(2)
m1.metric("📊 Média Geral", f"{media_geral:.1f} / 100")
m2.metric("🚀 Maior Destaque", f"{melhor_atributo} ({maior_nota} pts)")

# 6. GRÁFICO DE RADAR CORRIGIDO
st.markdown("---")
st.markdown("### 📊 Gráfico de Habilidades")

# Criamos as listas para alimentar o gráfico
categorias = ['Ritmo', 'Finalização', 'Passe', 'Drible', 'Defesa', 'Físico']
valores_radar = [ritmo, finalizacao, passe, drible, defesa, fisico]

# DataFrame do gráfico montado de forma simples
df_grafico = pd.DataFrame({
    'Atributo': categorias + [categorias[0]],
    'Pontuação': valores_radar + [valores_radar[0]],
    'Texto_Exibido': [str(ritmo), str(finalizacao), str(passe), str(drible), str(defesa), str(fisico), ""]
})

fig_radar = px.line_polar(
    df_grafico,
    r='Pontuação',
    theta='Atributo',
    line_close=True,
    template="plotly_white"
)

fig_radar.update_traces(
    mode='lines+markers+text',
    text=df_grafico['Texto_Exibido'],
    textposition='top center',
    fill='toself',
    fillcolor='rgba(31, 119, 180, 0.2)'
)

fig_radar.update_layout(
    polar=dict(
        radialaxis=dict(range=[0, 100])
    ),
    height=450
)

st.plotly_chart(fig_radar, use_container_width=True)