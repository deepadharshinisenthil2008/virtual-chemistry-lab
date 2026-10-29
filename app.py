import streamlit as st
from rdkit import Chem
from rdkit.Chem import Draw, Descriptors, rdMolDescriptors

# -------------------------------
# PAGE CONFIGURATION
# -------------------------------
st.set_page_config(
    page_title="Molecule Explorer",
    page_icon="🧪",
    layout="wide"
)

# -------------------------------
# APP DESIGN
# -------------------------------
st.markdown("""
<style>
.stApp {
    background-color: #f4f7fb;
}
.title {
    font-size: 38px;
    font-weight: bold;
    color: #17365d;
    text-align: center;
}
.subtitle {
    font-size: 18px;
    color: #52657a;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">🧪 Molecule Explorer Lab</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">An Interactive Cheminformatics Learning App for Students</div>',
    unsafe_allow_html=True
)
st.divider()

# -------------------------------
# SAMPLE MOLECULES
# -------------------------------
molecules = {
    "Water": "O",
    "Methane": "C",
    "Ethanol": "CCO",
    "Glucose": "C(C1C(C(C(C(O1)O)O)O)O)O",
    "Acetic Acid": "CC(=O)O",
    "Benzene": "c1ccccc1",
    "Caffeine": "Cn1c(=O)c2c(ncn2C)n(C)c1=O",
    "Aspirin": "CC(=O)OC1=CC=CC=C1C(=O)O",
    "Ethene": "C=C",
    "Ethane": "CC",
    "Propane": "CCC",
    "Butane": "CCCC"
}

# -------------------------------
# MOLECULE INFORMATION
# -------------------------------
def get_molecule_info(smiles):
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None

    return {
        "molecule": mol,
        "formula": rdMolDescriptors.CalcMolFormula(mol),
        "weight": Descriptors.MolWt(mol),
        "atoms": mol.GetNumAtoms(),
        "bonds": mol.GetNumBonds(),
        "canonical_smiles": Chem.MolToSmiles(mol)
    }

# -------------------------------
# MOLECULE DISPLAY
# -------------------------------
def display_molecule(name, smiles):
    info = get_molecule_info(smiles)
    if info is None:
        st.error("Invalid SMILES notation. Please check your input.")
        return None

    st.subheader("🧬 " + name)
    image = Draw.MolToImage(info["molecule"], size=(400, 300))
    st.image(image, caption=f"2D structure of {name}", width=400)
    st.success("Molecule loaded successfully!")

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Molecular Formula", info["formula"])
        st.metric("Number of Atoms", info["atoms"])
    with col2:
        st.metric("Molecular Weight", f'{info["weight"]:.2f} g/mol')
        st.metric("Number of Bonds", info["bonds"])

    with st.expander("View canonical SMILES notation"):
        st.code(info["canonical_smiles"])
    return info

# -------------------------------
# SIDEBAR
# -------------------------------
st.sidebar.title("🔬 Lab Menu")
page = st.sidebar.radio(
    "Choose an activity",
    [
        "Home",
        "Explore a Molecule",
        "Compare Two Molecules",
        "Build Your Own Molecule",
        "About the Project"
    ]
)

# -------------------------------
# HOME PAGE
# -------------------------------
if page == "Home":
    st.header("Welcome to Molecule Explorer!")
    st.write("""
    This application helps students understand chemical molecules
    through interactive molecular structure visualization.

    ### What can you do?
    - Explore common chemical molecules.
    - View their 2D structures.
    - Learn their molecular formulas.
    - Calculate molecular weights.
    - Count atoms and bonds.
    - Compare two molecules.
    - Enter your own SMILES notation.
    """)

    col1, col2, col3 = st.columns(3)
    col1.info("🧪 Explore Molecules")
    col2.info("🔍 Compare Structures")
    col3.info("📚 Learn Chemistry")

    st.subheader("Available Molecules")
    st.write(", ".join(molecules.keys()))

# -------------------------------
# EXPLORE MOLECULE
# -------------------------------
elif page == "Explore a Molecule":
    st.header("Explore a Chemical Molecule")
    selected = st.selectbox("Select a molecule", list(molecules.keys()))
    custom_smiles = st.text_input(
        "Or enter your own SMILES notation",
        placeholder="Example: CCO"
    )

    if st.button("Show Molecule", type="primary"):
        if custom_smiles.strip():
            display_molecule("Custom Molecule", custom_smiles.strip())
        else:
            display_molecule(selected, molecules[selected])

# -------------------------------
# COMPARE TWO MOLECULES
# -------------------------------
elif page == "Compare Two Molecules":
    st.header("Compare Two Chemical Molecules")
    col1, col2 = st.columns(2)

    with col1:
        molecule_a = st.selectbox("Select Molecule A", list(molecules.keys()), index=2)
    with col2:
        molecule_b = st.selectbox("Select Molecule B", list(molecules.keys()), index=3)

    if st.button("Compare Molecules", type="primary"):
        info_a = get_molecule_info(molecules[molecule_a])
        info_b = get_molecule_info(molecules[molecule_b])

        if info_a and info_b:
            left, right = st.columns(2)
            with left:
                display_molecule("Molecule A: " + molecule_a, molecules[molecule_a])
            with right:
                display_molecule("Molecule B: " + molecule_b, molecules[molecule_b])

            st.divider()
            st.subheader("Comparison Results")
            comparison = {
                "Property": [
                    "Molecular Formula",
                    "Molecular Weight (g/mol)",
                    "Number of Atoms",
                    "Number of Bonds"
                ],
                molecule_a: [
                    info_a["formula"],
                    round(info_a["weight"], 2),
                    info_a["atoms"],
                    info_a["bonds"]
                ],
                molecule_b: [
                    info_b["formula"],
                    round(info_b["weight"], 2),
                    info_b["atoms"],
                    info_b["bonds"]
                ]
            }
            st.table(comparison)

            if info_a["canonical_smiles"] == info_b["canonical_smiles"]:
                st.success("Both inputs represent the same canonical structure.")
            elif info_a["formula"] == info_b["formula"]:
                st.info(
                    "Both molecules have the same molecular formula. "
                    "They may be structural isomers; compare their structures."
                )
            else:
                st.info("The molecules have different molecular formulas.")

# -------------------------------
# BUILD YOUR OWN MOLECULE
# -------------------------------
elif page == "Build Your Own Molecule":
    st.header("Enter Your Own Molecule")
    st.write("""
    Enter the SMILES representation of a molecule. The application will
    display its structure and calculate basic molecular properties.
    """)

    smiles_input = st.text_input(
        "Enter SMILES",
        placeholder="Examples: CCO, CC, c1ccccc1"
    )

    if st.button("Analyze Molecule", type="primary"):
        if smiles_input.strip():
            info = get_molecule_info(smiles_input.strip())
            if info:
                display_molecule("Your Molecule", smiles_input.strip())
            else:
                st.error("Invalid SMILES. Please enter a valid chemical structure.")
        else:
            st.warning("Please enter a SMILES notation first.")

# -------------------------------
# ABOUT THE PROJECT
# -------------------------------
elif page == "About the Project":
    st.header("About This Project")
    st.write("""
    ### Project Title
    Molecule Explorer Lab: An Interactive Cheminformatics Application

    ### Objective
    To develop an interactive learning application that helps students
    explore, visualize, and compare chemical molecules.

    ### Technologies Used
    - Python
    - Streamlit
    - RDKit
    - SMILES notation

    ### Applications
    - Chemistry education
    - Cheminformatics learning
    - Molecular structure exploration
    - Basic molecular property analysis

    ### Conclusion
    This application provides a simple way to study molecular structures
    and understand their basic chemical properties.
    """)

st.divider()
st.caption("Molecule Explorer Lab | Educational Cheminformatics Project")
