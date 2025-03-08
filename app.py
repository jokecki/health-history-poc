import streamlit as st
import json

st.title("Health History POC")

# Charger la liste de codes (dont les 'condition')
with open("all_codes.json", "r", encoding="utf-8") as f:
    all_codes = json.load(f)

# Stocker les réponses dans st.session_state
if "answers" not in st.session_state:
    st.session_state.answers = {}

# Un "état" minimal pour naviguer entre la question et l'écran "autres"
if "current_step" not in st.session_state:
    st.session_state.current_step = "condition_question"

###############################################################################
# 1) 5 choix fréquents + "Autre..."
###############################################################################
# On prépare les 5 conditions fréquentes, telles que vous les avez listées
# (On pourrait aussi les extraire de all_codes.json, mais ici on les définit en dur.)

frequent_conditions = [
    {
        "label": "Hypertension artérielle",
        "code_display": "38341003",
        "terminology_display": "SNOMED CT"
    },
    {
        "label": "Accident vasculaire cérébral",
        "code_display": "230690007",
        "terminology_display": "SNOMED CT"
    },
    {
        "label": "Diabète de type 1",
        "code_display": "46635009",
        "terminology_display": "SNOMED CT"
    },
    {
        "label": "Diabète de type 2",
        "code_display": "44054006",
        "terminology_display": "SNOMED CT"
    },
    {
        "label": "Infarctus du myocarde",
        "code_display": "22298006",
        "terminology_display": "SNOMED CT"
    }
]

def condition_question():
    st.subheader("Souffrez-vous d'une des maladies suivantes ?")
    # On liste 5 labels + "Autre..."
    labels = [item["label"] for item in frequent_conditions] + ["Autre..."]
    choice = st.radio("Sélectionnez :", labels)

    if st.button("Valider"):
        if choice == "Autre...":
            # On va afficher la liste complète
            st.session_state.current_step = "other_conditions"
        else:
            # Récupérer l'élément sélectionné dans frequent_conditions
            selected = next((c for c in frequent_conditions if c["label"] == choice), None)
            # On stocke la réponse dans st.session_state.answers, par ex. "medical_condition"
            # On peut y mettre un mini-dict : code_display, label, etc.
            st.session_state.answers["medical_condition"] = {
                "label": selected["label"],
                "code_display": selected["code_display"],
                "terminology_display": selected["terminology_display"]
            }
            st.session_state.current_step = "recap"
        st.experimental_rerun()

###############################################################################
# 2) "Autre..." : l'utilisateur veut choisir dans la liste complète de category="condition"
###############################################################################
def other_conditions():
    st.subheader("Choisissez parmi la liste complète des maladies (conditions)")

    # Filtrer dans all_codes les entries où category="condition"
    condition_list = [c for c in all_codes if c.get("category") == "condition"]
    # Tri alphabétique par label
    condition_list_sorted = sorted(condition_list, key=lambda x: x["label"])
    # On propose un selectbox
    choice_label = st.selectbox("Conditions disponibles", [c["label"] for c in condition_list_sorted])

    if st.button("Valider (Autres)"):
        chosen = next((c for c in condition_list_sorted if c["label"] == choice_label), None)
        # On stocke la réponse
        st.session_state.answers["medical_condition"] = {
            "label": chosen["label"],
            "code_display": chosen["code_display"],
            "terminology_display": chosen["terminology_display"]
        }
        st.session_state.current_step = "recap"
        st.experimental_rerun()

###############################################################################
# 3) Récapitulatif
###############################################################################
def recap():
    st.subheader("Récapitulatif")
    st.write("Voici vos réponses :", st.session_state.answers)

    if st.button("Terminer"):
        st.write("Fin du POC !")
        st.stop()

    # (Optionnel) Bouton pour recommencer
    if st.button("Recommencer"):
        st.session_state.answers = {}
        st.session_state.current_step = "condition_question"
        st.experimental_rerun()

###############################################################################
# ROUTING
###############################################################################
if st.session_state.current_step == "condition_question":
    condition_question()
elif st.session_state.current_step == "other_conditions":
    other_conditions()
elif st.session_state.current_step == "recap":
    recap()
import streamlit as st

st.title("Hello from Streamlit")
st.write("Ceci est un test pour valider le setup Streamlit.")

if st.button("Clique moi"):
    st.write("Bouton cliqué !")

