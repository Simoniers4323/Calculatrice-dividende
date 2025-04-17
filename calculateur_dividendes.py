import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Calculateur de Dividendes", layout="wide")

st.title("📈 Calculateur de Dividendes")


# --- Entrées utilisateur ---
col1, col2 = st.columns(2)

with col1:
    capital_initial = st.number_input("Capital initial :", min_value=0.0, value=10000.0, step=1000.0, format="%.2f")
    taux_imposition = st.slider("Taux d'imposition sur les dividendes :", 0.0, 50.0, 0.0, step=0.1, format="%.1f") / 100
    contribution_annuelle = st.number_input("Contribution annuelle :", min_value=0.0, value=10000.0, step=1000.0, format="%.2f")
    duree_investissement = st.number_input("Nombre d'années d'investissement :", min_value=1, value=20, step=1)

with col2:
    rendement_annuel = st.slider("Rendement annuel des dividendes (%) :", 0.0, 20.0, 5.0, step=0.1) / 100
    augmentation_dividendes = st.slider("Augmentation annuelle prévue des dividendes (%) :", 0.0, 20.0, 10.0, step=0.5) / 100
    appreciation_action = st.slider("Appréciation annuelle prévue du prix de l'action (%) :", 0.0, 20.0, 10.0, step=0.5) / 100
    reinvestissement = st.radio("Réinvestissement automatique des dividendes (DRIP) :", ["Oui", "Non"]) == "Oui"
    compte_imposable = st.radio("Compte imposable :", ["Oui", "Non"]) == "Oui"
    frequence_paiement = st.selectbox("Fréquence des paiements de dividendes :", ["Trimestrielle", "Annuelle", "Mensuelle"], index=0)


# Fréquence en nombre de périodes par an
frequence_map = {"Annuelle": 1, "Trimestrielle": 4, "Mensuelle": 12}
nb_periodes = duree_investissement * frequence_map[frequence_paiement]
rendement_par_periode = rendement_annuel / frequence_map[frequence_paiement]
augmentation_par_periode = (1 + augmentation_dividendes) ** (1 / frequence_map[frequence_paiement]) - 1
appreciation_par_periode = (1 + appreciation_action) ** (1 / frequence_map[frequence_paiement]) - 1
contribution_par_periode = contribution_annuelle / frequence_map[frequence_paiement]



# --- Calculs ---
valeurs_portefeuille = []
revenus_dividendes = []
rendement_sur_cout = []
nombre_actions = capital_initial / 100  # Prix initial de l'action : 100$
prix_action = 100.0
cout_total = nombre_actions * prix_action

total_dividendes = 0.0

for periode in range(nb_periodes):
    dividende_par_action = prix_action * rendement_par_periode
    revenu_dividende = nombre_actions * dividende_par_action

    if compte_imposable:
        revenu_dividende *= (1 - taux_imposition)

    total_dividendes += revenu_dividende
    if reinvestissement:
        nombre_actions += revenu_dividende / prix_action

    nombre_actions += contribution_par_periode / prix_action
    prix_action *= (1 + appreciation_par_periode)

    cout_total += contribution_par_periode
    valeur_portefeuille = nombre_actions * prix_action

    valeurs_portefeuille.append(valeur_portefeuille)
    revenus_dividendes.append(total_dividendes)
    rendement_sur_cout.append((total_dividendes / cout_total) * 100)

    # Appliquer la croissance des dividendes
    rendement_par_periode *= (1 + augmentation_par_periode)


# --- Graphiques ---

# Axe X basé sur les années
x_axis = list(range(1, duree_investissement + 1))

# Réduction des listes : on prend 1 valeur par année (la dernière de chaque année)
valeurs_portefeuille = [valeurs_portefeuille[i * frequence_map[frequence_paiement] - 1] for i in x_axis]
revenus_dividendes = [revenus_dividendes[i * frequence_map[frequence_paiement] - 1] for i in x_axis]
rendement_sur_cout = [rendement_sur_cout[i * frequence_map[frequence_paiement] - 1] for i in x_axis]
formatter = plt.FuncFormatter(lambda x, _: f'{x:,.0f}')

fig1, ax1 = plt.subplots()
ax1.plot(x_axis, valeurs_portefeuille)
ax1.set_title("Valeur du portefeuille")
ax1.set_ylabel("$")
ax1.get_yaxis().set_major_formatter(formatter)

fig2, ax2 = plt.subplots()
ax2.plot(x_axis, revenus_dividendes, color='green')
ax2.set_title("Revenus de dividendes")
ax2.set_ylabel("$")
ax2.get_yaxis().set_major_formatter(formatter)

fig3, ax3 = plt.subplots()
ax3.plot(x_axis, rendement_sur_cout, color='gold')
ax3.set_title("Rendement sur coût")
ax3.set_ylabel("%")
ax3.get_yaxis().set_major_formatter(formatter)



# --- Affichage ---
st.markdown("---")
colA, colB, colC = st.columns(3)
with colA:
    st.pyplot(fig1)
with colB:
    st.pyplot(fig2)
with colC:
    st.pyplot(fig3)

st.markdown("""
<style>
    .stSlider > div > div > div > div {
        background: linear-gradient(90deg, #00b4d8, #90e0ef);
    }
</style>
""", unsafe_allow_html=True)
