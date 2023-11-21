import streamlit as st
from src.process.train_process import process_train 
from src.process.inference_process import inference

def interface_execute_preprocess(force=False):
    st.write(f"Exécution de preprocess.")
    if force:
        st.write("Option --force activée")
    path = st.text_input("Entrez le chemin pour preprocess:", "")
    if st.button('Lancer Preprocess'):
        process_train(path, force)
        st.success("Preprocess exécuté avec succès.")

def interface_execute_inference(benchmark=False):
    st.write(f"Exécution de inference.")
    if benchmark:
        st.write("Benchmark activé")
    path = st.text_input("Entrez le chemin pour inference:", "")
    if st.button('Lancer Inference'):
        inference(path, benchmark)
        st.success("Inference exécuté avec succès.")

st.title('Form Reconizer - DGFiP')

st.subheader('Preprocess')
force = st.checkbox("Activer Force pour Preprocess")
interface_execute_preprocess(force=force)

st.subheader('Inference')
benchmark = st.checkbox("Activer Benchmark pour Inference")
interface_execute_inference(benchmark=benchmark)
