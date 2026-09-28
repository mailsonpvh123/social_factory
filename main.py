import streamlit as st

# Configuração da página para ficar com cara de App
st.set_page_config(page_title="Social Factory", page_icon="🏭", layout="centered")

st.title("🏭 Social Factory")
st.write("Sua máquina de conteúdo automatizada. Selecione o que deseja gerar hoje:")

# Cria duas abas na interface
tab1, tab2 = st.tabs(["🖼️ Carrossel", "🎬 Reel (Modelagem)"])

# Aba 1: Fábrica de Carrossel
with tab1:
    st.subheader("Gerar Novo Carrossel")
    nicho_c = st.text_input("Nicho da Página (ex: Saúde, Estoicismo):")
    tema_c = st.text_input("Tema do Post (ex: 3 dicas para secar):")
    
    if st.button("Fabricar Carrossel", type="primary", use_container_width=True):
        if nicho_c and tema_c:
            st.success(f"Comando recebido! Em breve o sistema vai gerar as imagens de '{tema_c}' para o nicho de {nicho_c}.")
        else:
            st.warning("Por favor, preencha o nicho e o tema antes de gerar.")

# Aba 2: Fábrica de Reels
with tab2:
    st.subheader("Remodelar Reel Viral")
    link_r = st.text_input("Link do Reel Concorrente:")
    nicho_r = st.text_input("Seu Nicho (Para adaptar a copy):")
    
    if st.button("Clonar e Remodelar", type="primary", use_container_width=True):
        if link_r and nicho_r:
            st.success(f"Comando recebido! O sistema vai baixar o vídeo do link e aplicar a narrativa do nicho de {nicho_r}.")
        else:
            st.warning("Por favor, preencha o link e o seu nicho.")
