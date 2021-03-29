import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    layout="wide",
)


@st.cache
def get_iris() -> pd.DataFrame:
    return pd.read_csv(
        "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv"
    )


iris = get_iris()

# generate sidbar
st.sidebar.header("Feature Filter")

min_sepal_length, max_sepal_length = st.sidebar.slider(
    "Select sepal length range:",
    min(iris.sepal_length),
    min(iris.sepal_length),
    (min(iris.sepal_length), max(iris.sepal_length)),
)
min_sepal_width, max_sepal_width = st.sidebar.slider(
    "Select sepal length range:",
    min(iris.sepal_width),
    min(iris.sepal_width),
    (min(iris.sepal_width), max(iris.sepal_width)),
)
min_petal_length, max_petal_length = st.sidebar.slider(
    "Select sepal length range:",
    min(iris.petal_length),
    min(iris.petal_length),
    (min(iris.petal_length), max(iris.petal_length)),
)
min_petal_width, max_petal_width = st.sidebar.slider(
    "Select sepal length range:",
    min(iris.petal_width),
    min(iris.petal_width),
    (min(iris.petal_width), max(iris.petal_width)),
)

species = st.sidebar.multiselect(
    "Select species:", list(iris.species.unique()), list(iris.species.unique())
)

restrict = pd.DataFrame(
    data=[
        ["sepal_length", min_sepal_length, max_sepal_length],
        ["sepal_width", min_sepal_width, max_sepal_width],
        ["petal_length", min_petal_length, max_petal_length],
        ["petal_width", min_petal_width, max_petal_width],
    ],
    columns=["feature", "minimal", "maximal"],
)

filtered_iris = iris.loc[
    iris.sepal_length.between(min_sepal_length, max_sepal_length)
    & iris.sepal_width.between(min_sepal_width, max_sepal_width)
    & iris.petal_length.between(min_petal_length, max_petal_length)
    & iris.petal_width.between(min_petal_width, max_petal_width)
    & iris.species.isin(species)
]

st.markdown(
    f"""
<style>
    .reportview-container .main .block-container{{
        max-width: 1400px;
    }}
</style>
""",
    unsafe_allow_html=True,
)

st.title("Streamlit Test App")
st.write(
    """
Some *basic* [__Streamlit__](https://www.streamlit.io/) App to explore Data!
"""
)

st.write("### Iris Dataset")
st.write(f"Using following restrictions:")
st.dataframe(restrict)
st.write(f"Selected Species: __{species}__")

st.write("Resulting Dataframe:")
st.dataframe(filtered_iris)

st.write("## Plotting the Data")
feature_list = [
    "sepal_length",
    "sepal_width",
    "petal_length",
    "petal_width",
]

features = st.multiselect("Select Features:", feature_list, feature_list[0:2])
fig = px.scatter_matrix(
    filtered_iris, dimensions=features, color="species", height=800
)

st.plotly_chart(fig, use_container_width=True)
