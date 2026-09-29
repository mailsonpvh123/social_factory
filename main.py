import streamlit as st
import google.generativeai as genai
import os
import json

# Configuração da página
st.set_page_config(page_title="Social Factory", page_icon="🏭", layout="centered")

# Captura a chave do Gemini configurada no Easypanel
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# Inicializa o cérebro da IA se a chave existir
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    # Usando o flash: super rápido e barato/gratuito
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    model = None

st.title("🏭 Social Factory")
st.write("Sua máquina de conteúdo automatizada. Selecione o que deseja gerar hoje:")

tab1, tab2 = st.tabs(["🖼️ Carrossel", "🎬 Reel (Modelagem)"])

# Aba 1: A Fábrica de Carrossel
with tab1:
    st.subheader("Gerar Novo Carrossel")
    nicho_c = st.text_input("Nicho da Página (ex: Receitas, Finanças, Estoicismo):")
    tema_c = st.text_input("Tema do Post (ex: 3 lanches rápidos para secar):")
    
    if st.button("Fabricar Roteiro", type="primary", use_container_width=True):
        if not GEMINI_API_KEY:
            st.error("Aviso: Configure a GEMINI_API_KEY nas variáveis de ambiente do Easypanel.")
        elif nicho_c and tema_c:
            with st.spinner("O cérebro da IA está processando as copies..."):
                # O prompt rigoroso forçando a saída em JSON
                prompt = f"""
                Você é um copywriter de elite no Instagram, especialista em páginas dark do nicho de {nicho_c}.
                Escreva o conteúdo para um carrossel magnético e viral sobre o tema: '{tema_c}'.
                
                REGRA ABSOLUTA: Retorne APENAS um objeto JSON válido, sem textos antes ou depois, seguindo esta estrutura exata:
                {{
                    "slide_1": "Título impossível de ser ignorado (gancho)",
                    "slide_2": "Conteúdo de alto valor - Parte 1",
                    "slide_3": "Conteúdo de alto valor - Parte 2",
                    "slide_4": "Conteúdo de alto valor - Parte 3",
                    "slide_5": "Chamada para ação (CTA) forte mandando para o link da bio",
                    "legenda": "Legenda persuasiva estruturada com quebra de linhas e 5 hashtags relevantes"
                }}
                """
                
                try:
                    response = model.generate_content(prompt)
                    
                    # Limpa a formatação markdown que a IA costuma colocar em volta do JSON
                    texto_limpo = response.text.replace("```json", "").replace("```", "").strip()
                    roteiro = json.loads(texto_limpo)
                    
                    st.success("Cópia gerada com sucesso!")
                    
                    # Exibe o resultado de forma limpa na tela do seu celular
                    for chave, valor in roteiro.items():
                        if chave != "legenda":
                            st.info(f"**{chave.replace('_', ' ').title()}**: {valor}")
                    
                    st.text_area("Legenda pronta para copiar:", roteiro.get("legenda", ""), height=200)
                    
                except Exception as e:
                    st.error(f"Erro na comunicação com a IA ou no formato do JSON: {e}")
        else:
            st.warning("Preencha o nicho e o tema para prosseguir.")

# Aba 2: A Fábrica de Reels (Estrutura base mantida)
with tab2:
    st.subheader("Remodelar Reel Viral")
    link_r = st.text_input("Link do Reel Concorrente:")
    nicho_r = st.text_input("Seu Nicho (Para adaptar a copy):")
    
    if st.button("Clonar e Remodelar", type="primary", use_container_width=True):
        if link_r and nicho_r:
            st.success(f"Em breve: O sistema vai baixar {link_r} e reescrever para {nicho_r}.")
        else:
            st.warning("Preencha o link e o seu nicho.")
