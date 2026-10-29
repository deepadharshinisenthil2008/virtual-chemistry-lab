import streamlit as st

st.set_page_config(
page_title="Virtual Chemistry Lab",
page_icon="🧪",
layout="wide"
)

st.title("🧪 Virtual Chemistry Lab")
st.write("Explore molecules and learn chemistry interactively!")

st.sidebar.header("Lab Menu")

choice = st.sidebar.selectbox(
"Choose a section",
[
"Home",
"Molecule Explorer",
"Chemistry Facts",
"Molecular Calculator"
]
)

if choice == "Home":
st.header("Welcome to Your Virtual Lab!")
st.write("Learn chemistry through interactive activities.")

col1, col2, col3 = st.columns(3)

col1.metric("Chemistry", "Explore")
col2.metric("Molecules", "Discover")
col3.metric("Learning", "Interactive")

st.info(
    "Select a section from the Lab Menu to begin."
)

elif choice == "Molecule Explorer":
st.header("🔬 Molecule Explorer")

molecule = st.selectbox(
    "Choose a molecule",
    ["Water", "Carbon dioxide", "Oxygen", "Ammonia", "Methane"]
)

molecules = {
    "Water": ("H₂O", "18.015", "2 hydrogen atoms and 1 oxygen atom"),
    "Carbon dioxide": ("CO₂", "44.01", "1 carbon atom and 2 oxygen atoms"),
    "Oxygen": ("O₂", "32.00", "2 oxygen atoms"),
    "Ammonia": ("NH₃", "17.031", "1 nitrogen atom and 3 hydrogen atoms"),
    "Methane": ("CH₄", "16.043", "1 carbon atom and 4 hydrogen atoms")
}

formula, mass, description = molecules[molecule]

st.success(f"Selected molecule: {molecule}")
st.write(f"**Molecular formula:** {formula}")
st.write(f"**Molar mass:** {mass} g/mol")
st.write(f"**Composition:** {description}")

elif choice == "Chemistry Facts":
st.header("💡 Chemistry Facts")

st.write("1. Water has the chemical formula H₂O.")
st.write("2. Oxygen gas normally exists as O₂.")
st.write("3. The atomic number of carbon is 6.")
st.write("4. The pH scale is commonly shown from 0 to 14.")

elif choice == "Molecular Calculator":
st.header("🧮 Molecular Calculator")

st.write("Calculate the mass of a molecule from its composition.")

c1, c2, c3 = st.columns(3)

with c1:
    carbon = st.number_input(
        "Number of carbon atoms",
        min_value=0,
        value=1
    )

with c2:
    hydrogen = st.number_input(
        "Number of hydrogen atoms",
        min_value=0,
        value=4
    )

with c3:
    oxygen = st.number_input(
        "Number of oxygen atoms",
        min_value=0,
        value=0
    )

mass = carbon * 12.011 + hydrogen * 1.008 + oxygen * 15.999

st.write(f"**Approximate molar mass: {mass:.3f} g/mol**")

st.divider()
st.caption("Virtual Chemistry Lab | Educational Project")
