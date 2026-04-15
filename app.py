import pandas as pd
import plotly.express as px
import streamlit as st


# PAGE CONFIGURATION
st.set_page_config(page_title="Vehicle Analysis App", layout="wide")

st.title("🚗 Vehicle Data Analysis")


# LOAD DATA
@st.cache_data
def load_data():
    return pd.read_csv('vehicles.csv')

car_data = load_data()


# SIDEBAR FILTERS
st.sidebar.header("Filters")

# price filter
price_range = st.sidebar.slider(
    "Price Range",
    int(car_data.price.min()),
    int(car_data.price.max()),
    (int(car_data.price.min()), int(car_data.price.max()))
)

# mileage filter
mileage_range = st.sidebar.slider(
    "Mileage Range",
    int(car_data.odometer.min()),
    int(car_data.odometer.max()),
    (int(car_data.odometer.min()), int(car_data.odometer.max()))
)

# apply filters
filtered_data = car_data[
    (car_data["price"].between(price_range[0], price_range[1])) &
    (car_data["odometer"].between(mileage_range[0], mileage_range[1]))
]


# CHART SELECTION
st.subheader("Select Visualization")

show_histogram = st.checkbox("Show Histogram")
show_scatter = st.checkbox("Show Scatter Plot")


# LAYOUT
col1, col2 = st.columns(2)

# HISTOGRAM
if show_histogram:
    with col1:
        st.write("### Mileage Distribution")

        fig = px.histogram(
            filtered_data,
            x="odometer",
            nbins=40,
            title="Mileage Distribution",
            labels={
                "odometer": "Mileage (km)",
                "count": "Count"
            },
            color_discrete_sequence=px.colors.qualitative.Set2
        )

        fig.update_layout(template="plotly_white")

        st.plotly_chart(fig, use_container_width=True)


# SCATTER PLOT
if show_scatter:
    with col2:
        st.write("### Price vs Mileage")

        fig = px.scatter(
            filtered_data,
            x="odometer",
            y="price",
            color="condition",
            size="price",
            hover_data=["model_year"],
            title="Price vs Mileage",
            labels={
                "odometer": "Mileage (km)",
                "price": "Price ($)",
                "condition": "Condition"
            },
            color_discrete_sequence=px.colors.qualitative.Set2,
            opacity=0.7
        )

        fig.update_layout(template="plotly_white")

        st.plotly_chart(fig, use_container_width=True)


# SUMMARY METRICS
st.subheader("Summary")

col1, col2, col3 = st.columns(3)

col1.metric("Total Vehicles", len(filtered_data))
col2.metric("Average Price", f"${int(filtered_data.price.mean())}")
col3.metric("Average Mileage", f"{int(filtered_data.odometer.mean())} km") 