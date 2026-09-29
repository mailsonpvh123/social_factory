import streamlit as st
from google import genai
from google.genai import types
import os
import json
import time

st.set_page_config(page_title="Social Factory", page_icon="🏭", layout="centered")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

if GEMINI_API_KEY:
    client = genai.Client(api_key=GEMINI_API_KEY)
else:
    client = None

st.title("🏭 Social Factory")
st.write("A sua máquina de conteúdo automatizada. Selecione o que deseja gerar hoje:")

tab1, tab2 = st.tabs(["🖼️ Carrossel", "🎬 Reel (Modelagem)"])

with tab1:
    st.subheader("Gerar Novo Carrossel")
    nicho_c = st.text_input("Nicho da Página (ex: Receitas, Finanças, Estoicismo):")
    tema_c = st.text_input("Tema do Post (ex: 3 lanches rápidos para secar):")
    link_base_c = st.text_input("Link da Publicação Base (Opcional - para remodelar):")
    
    if st.button("Fabricar Roteiro", type="primary", use_container_width=True):
        if not GEMINI_API_KEY:
            st.error("Aviso: Configure a GEMINI_API_KEY nas variáveis de ambiente do Easypanel.")
        elif nicho_c and tema_c:
            
            instrucao_extra = ""
            if link_base_c:
                instrucao_extra = f"\nUse o conteúdo deste link como inspiração: {link_base_c}\nCrie algo melhor, mantendo a essência viral."

            prompt = f"""
            Atue como copywriter de elite no Instagram, nicho de {nicho_c}.
            Escreva um carrossel viral sobre: '{tema_c}'.{instrucao_extra}
            
            Retorne APENAS um JSON válido com esta estrutura exata:
            {{
                "slide_1": "Título gancho",
                "prompt_img_1": "Prompt em inglês, ultra-realista, descrevendo a imagem de fundo para o slide 1",
                "slide_2": "Conteúdo parte 1",
                "prompt_img_2": "Prompt em inglês para imagem do slide 2",
                "slide_3": "Conteúdo parte 2",
                "prompt_img_3": "Prompt em inglês para imagem do slide 3",
                "slide_4": "Conteúdo parte 3",
                "prompt_img_4": "Prompt em inglês para imagem do slide 4",
                "slide_5": "Chamada para ação (CTA)",
                "prompt_img_5": "Prompt em inglês para imagem do slide 5",
                "legenda": "Legenda persuasiva com 5 hashtags"
            }}
            """
            
            status_placeholder = st.empty()
            max_tentativas = 3
            
            for tentativa in range(1, max_tentativas + 1):
                try:
                    status_placeholder.info(f"A processar copys e prompts visuais... (Tentativa {tentativa}/{max_tentativas})")
                    
                    response = client.models.generate_content(
                        model='gemini-3.8-flash',
                        contents=prompt,
                        config=types.GenerateContentConfig(
                            response_mime_type="application/json",
                        ),
                    )
                    
                    roteiro = json.loads(response.text)
                    status_placeholder.success("Roteiro e prompts gerados com sucesso!")
                    
                    for i in range(1, 6):
                        slide_key = f"slide_{i}"
                        prompt_key = f"prompt_img_{i}"
                        if slide_key in roteiro:
                            st.info(f"**Slide {i}**: {roteiro[slide_key]}")
                        if prompt_key in roteiro:
                            st.caption(f"🎨 **Prompt da Imagem:** {roteiro[prompt_key]}")
                    
                    st.text_area("Legenda pronta para copiar:", roteiro.get("legenda", ""), height=150)
                    break
                    
                except Exception as e:
                    erro_str = str(e)
                    if "503" in erro_str and tentativa < max_tentativas:
                        status_placeholder.warning("Servidor ocupado. Tentando novamente em 4s...")
                        time.sleep(4)
                    else:
                        status_placeholder.error(f"Erro na IA: {e}")
                        break
        else:
            st.warning("Preencha o nicho e o tema para prosseguir.")

with tab2:
    st.subheader("Remodelar Reel Viral")
    link_r = st.text_input("Link do Reel Concorrente:")
    nicho_r = st.text_input("Seu Nicho (Para adaptar a copy):")
    
    if st.button("Clonar e Remodelar", type="primary", use_container_width=True):
        if link_r and nicho_r:
            st.success(f"Em breve: Download de {link_r} e reescrita para {nicho_r}.")
        else:
            st.warning("Preencha o link e o seu nicho.")
