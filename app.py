import pandas as pd
import streamlit as st
import plotly.express as px

# Page setup
st.set_page_config(page_title="Titanic Data Dashboard", layout="wide")
st.title("🛳️ Titanic Data Analysis Dashboard")
st.markdown("---")

# Load and prepare data
df = pd.read_csv("cleaned_data_final.csv")

df["Survived"] = df["Survived"].astype(int)
df["Status"] = df["Survived"].map({
    1: "Survived",
    0: "Not Survived"
})

df["Class"] = df["Pclass"].astype(str).map({
    "1": "First Class",
    "2": "Second Class",
    "3": "Third Class"
})

df["Port"] = df["Embarked"].map({
    "C": "Cherbourg",
    "Q": "Queenstown",
    "S": "Southampton"
})

df["Family_Size"] = df["SibSp"] + df["Parch"] + 1

df["Alone_vs_Family"] = df["Family_Size"].apply(
    lambda x: "Alone" if x == 1 else "With Family"
)

bins = [0, 12, 18, 35, 60, 100]
labels = [
    "Children (0-12)",
    "Teenagers (13-18)",
    "Young Adults (19-35)",
    "Adults (36-60)",
    "Seniors (60+)"
]

df["Age_Group"] = pd.cut(
    df["Age"],
    bins=bins,
    labels=labels,
    right=False
)

# Filters
st.sidebar.header("🔍 Data Filters")

gender_options = ["All"] + list(df["Sex"].dropna().unique())
selected_gender = st.sidebar.selectbox(
    "Select Gender:",
    gender_options
)

class_options = list(df["Class"].dropna().unique())
selected_classes = st.sidebar.multiselect(
    "Select Class:",
    class_options,
    default=class_options
)

min_age = float(df["Age"].min())
max_age = float(df["Age"].max())

selected_age_range = st.sidebar.slider(
    "Select Age Range:",
    min_value=min_age,
    max_value=max_age,
    value=(min_age, max_age)
)

# Apply filters
filtered_df = df.copy()

if selected_gender != "All":
    filtered_df = filtered_df[
        filtered_df["Sex"] == selected_gender
    ]

filtered_df = filtered_df[
    filtered_df["Class"].isin(selected_classes)
]

filtered_df = filtered_df[
    (filtered_df["Age"] >= selected_age_range[0]) &
    (filtered_df["Age"] <= selected_age_range[1])
]

# KPIs
total_people = len(filtered_df)

total_survivors = filtered_df[
    filtered_df["Survived"] == 1
].shape[0]

survival_rate = (
    total_survivors / total_people * 100
    if total_people > 0
    else 0
)

col1, col2, col3 = st.columns(3)

col1.metric(
    label="👥 Total Passengers",
    value=total_people
)

col2.metric(
    label="✅ Total Survivors",
    value=total_survivors
)

col3.metric(
    label="📈 Survival Rate",
    value=f"{survival_rate:.1f}%"
)

st.markdown("---")

# Charts
if filtered_df.empty:
    st.warning("No data matches the selected filters.")
else:
    c1, c2 = st.columns(2)

    with c1:
        st.subheader("1. Survival Rate by Age Group")

        age_surv = (
            filtered_df
            .groupby("Age_Group", observed=False)["Survived"]
            .mean()
            .reset_index()
        )

        age_surv["Survival Rate (%)"] = age_surv["Survived"] * 100

        fig_age = px.bar(
            age_surv,
            x="Age_Group",
            y="Survival Rate (%)",
            text_auto=".1f",
            color="Survival Rate (%)",
            color_continuous_scale="Blues",
            labels={
                "Age_Group": "Age Group"
            }
        )

        st.plotly_chart(
            fig_age,
            use_container_width=True
        )

    with c2:
        st.subheader("2. Survival Rate by Embarkation Port")

        port_surv = (
            filtered_df
            .dropna(subset=["Port"])
            .groupby("Port", observed=False)["Survived"]
            .mean()
            .reset_index()
        )

        port_surv["Survival Rate (%)"] = port_surv["Survived"] * 100

        fig_port = px.bar(
            port_surv,
            x="Port",
            y="Survival Rate (%)",
            text_auto=".1f",
            color="Survival Rate (%)",
            color_continuous_scale="Teal",
            labels={
                "Port": "Embarkation Port"
            }
        )

        st.plotly_chart(
            fig_port,
            use_container_width=True
        )

    st.markdown("---")

    c3, c4 = st.columns(2)

    with c3:
        st.subheader("3. Survival Rate: Alone vs With Family")

        alone_surv = (
            filtered_df
            .groupby("Alone_vs_Family", observed=False)["Survived"]
            .mean()
            .reset_index()
        )

        alone_surv["Survival Rate (%)"] = (
            alone_surv["Survived"] * 100
        )

        fig_alone = px.bar(
            alone_surv,
            x="Alone_vs_Family",
            y="Survival Rate (%)",
            text_auto=".1f",
            color="Alone_vs_Family",
            color_discrete_sequence=[
                "#ff9999",
                "#66b3ff"
            ],
            labels={
                "Alone_vs_Family": "Travel Status"
            }
        )

        st.plotly_chart(
            fig_alone,
            use_container_width=True
        )

    with c4:
        st.subheader("4. Family Size vs Survival Rate")

        fam_surv = (
            filtered_df
            .groupby("Family_Size", observed=False)["Survived"]
            .mean()
            .reset_index()
        )

        fam_surv["Survival Rate (%)"] = (
            fam_surv["Survived"] * 100
        )

        fig_fam = px.line(
            fam_surv,
            x="Family_Size",
            y="Survival Rate (%)",
            markers=True,
            line_shape="spline",
            labels={
                "Family_Size": "Family Size",
                "Survival Rate (%)": "Survival Rate (%)"
            }
        )

        st.plotly_chart(
            fig_fam,
            use_container_width=True
        )

    st.markdown("---")

    c5, c6 = st.columns(2)

    with c5:
        st.subheader("5. Fare Distribution by Class")

        fig_box = px.box(
            filtered_df,
            x="Class",
            y="Fare",
            color="Class",
            labels={
                "Class": "Passenger Class",
                "Fare": "Fare ($)"
            }
        )

        st.plotly_chart(
            fig_box,
            use_container_width=True
        )

    with c6:
        st.subheader("6. Age vs Fare")

        fig_scatter = px.scatter(
            filtered_df,
            x="Age",
            y="Fare",
            color="Status",
            opacity=0.7,
            color_discrete_sequence=[
                "#ef553b",
                "#00cc96"
            ],
            labels={
                "Age": "Age",
                "Fare": "Fare ($)",
                "Status": "Survival Status"
            }
        )

        st.plotly_chart(
            fig_scatter,
            use_container_width=True
        )

