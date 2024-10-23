import streamlit as st
import pandas as pd
import plotly.express as px

# Load the dataset
data = pd.read_csv("good_smartphones.csv")
data.drop(columns=['Unnamed: 0'],inplace=True)
st.set_page_config(page_title="Smartphone Data Dashboard", layout="wide")
st.sidebar.title('Type of Analysis')

gk=st.sidebar.selectbox('Menu',['Overall Analysis','Smartphone-Details','CategoryWise-Analysis'])
# Set Streamlit page configuration

if gk=='Smartphone-Details':
    st.title("📱 Smartphone Data Analysis Dashboard")
    st.markdown("Explore and compare smartphones across various features, prices, and performance metrics.")
    # Sidebar filters
    st.sidebar.header("Filter Options")

    # Filter by brand
    brands = st.sidebar.multiselect("Select Brand(s):", options=data["brand_name"].unique())

    # Filter by price range
    min_price, max_price = st.sidebar.slider("Select Price Range:",
                                             min_value=int(data["price"].min()),
                                             max_value=int(data["price"].max()),
                                             value=(10000, 50000))

    # Apply filters
    filtered_data = data[(data["price"] >= min_price) & (data["price"] <= max_price)]

    if brands:
        filtered_data = filtered_data[filtered_data["brand_name"].isin(brands)]

    ram = st.sidebar.multiselect("Select RAM Size (GB):", options=filtered_data["ram_capacity(GB)"].unique())
    storage = st.sidebar.multiselect("Select Storage (GB):", options=filtered_data["rom_capacity(GB)"].unique())
    refresh_rate = st.sidebar.multiselect("Select Refresh Rate (Hz):",
                                          options=filtered_data["display_refreshrate(Hz)"].unique())

    # Apply additional filters
    if ram:
        filtered_data = filtered_data[filtered_data["ram_capacity(GB)"].isin(ram)]
    if storage:
        filtered_data = filtered_data[filtered_data["rom_capacity(GB)"].isin(storage)]
    if refresh_rate:
        filtered_data = filtered_data[filtered_data["display_refreshrate(Hz)"].isin(refresh_rate)]

    # Display filtered data
    st.dataframe(filtered_data)
    st.subheader("📊 Price vs. Performance Scatter Plot")
    fig = px.scatter(
        filtered_data,
        x="price",
        y="performance_index",
        color="brand_name",
        hover_data=["model_name", "processor_name"],
        title="Price vs Performance"
    )
    st.plotly_chart(fig)
    st.subheader("🏆 Average Rating by Brand")
    avg_rating = filtered_data.groupby("brand_name")["rating_x"].mean().reset_index()
    fig = px.bar(avg_rating, x="brand_name", y="rating_x", title="Average Rating by Brand")
    st.plotly_chart(fig)
    st.subheader("📶 5G vs Non-5G Distribution")
    fig = px.pie(filtered_data, names="has_5g", title="Distribution of 5G Phones")
    st.plotly_chart(fig)
    st.sidebar.header("Compare Smartphones")
    comparison_models = st.sidebar.multiselect(
        "Select Smartphones to Compare:", options=filtered_data["model_name"].unique(), default=[]
    )

    if comparison_models:
        comparison_data = filtered_data[filtered_data["model_name"].isin(comparison_models)]
        st.subheader("📋 Comparison of Selected Smartphones")
        st.dataframe(comparison_data)
    st.subheader("🔍 Detailed Smartphone Information")

    for index, row in filtered_data.iterrows():
        with st.expander(f"{row['brand_name']} - {row['model_name']}"):
            st.write(f"**Price:** ₹{row['price']}")
            st.write(f"**Rating:** {row['rating_x']}")
            st.write(f"**Processor:** {row['processor_name']}")
            st.write(f"**Battery Capacity:** {row['battery_capacity(mAh)']} mAh")
            st.write(f"**Camera Resolution:** {row['rear_camera_resol']} (Rear) / {row['front_camera_resol']} (Front)")

    st.subheader("📊 Key Metrics for Brands")
    kpis = filtered_data.groupby("brand_name").agg(
        Avg_Rating=("rating_x", "mean"),
        Total_Models=("model_name", "count"),
        Avg_price=("price", "mean"),
        Avg_performanceIndex=("performance_index","mean")
    ).reset_index()
    st.dataframe(kpis)


    st.subheader("🔋 Battery vs Performance Correlation")
    fig = px.scatter(
        filtered_data,
        x="battery_capacity(mAh)",
        y="performance_index",
        color="brand_name",
        title="Battery Capacity vs Performance"
    )
    st.plotly_chart(fig)
    st.subheader("📈 Price vs Performance with Trendline")
    fig = px.scatter(
        filtered_data,
        x="price",
        y="performance_index",
        color="brand_name",
        trendline="ols",
        title="Price vs Performance with Trendline"
    )
    st.plotly_chart(fig)
    # Display Size Distribution
    st.subheader("📏 Display Size Distribution")
    fig = px.histogram(filtered_data, x="display_size", nbins=15, title="Distribution of Display Sizes")
    st.plotly_chart(fig)
    st.subheader("⚡ Fast Charging Analysis")
    fast_charging = filtered_data[["model_name", "rating_FC(W)", "battery_capacity(mAh)"]]
    fast_charging = fast_charging.sort_values(by="rating_FC(W)", ascending=False).head(10)
    st.dataframe(fast_charging)

    fig = px.scatter(filtered_data, x="rating_FC(W)", y="battery_capacity(mAh)",
                     title="Charging Speed vs Battery Capacity", color="brand_name")
    st.plotly_chart(fig)


elif gk=='CategoryWise-Analysis':
    st.sidebar.header("Select Price Category")
    category = st.sidebar.selectbox(
        "Choose a Price Category:",
        options=data["pricewise_cat"].unique(),
        index=0
    )

    # Filter data based on the selected category
    category_data = data[data["pricewise_cat"] == category]

    st.title(f"📱 {category} Smartphones")
    st.markdown(f"Explore **{category}** category smartphones with in-depth analytics.")
    # Display key metrics for the selected category
    total_phones = category_data.shape[0]
    avg_rating = category_data["rating_x"].mean()
    avg_price = category_data["price"].mean()

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Smartphones", total_phones)
    col2.metric("Average Rating", f"{avg_rating:.2f}")
    col3.metric("Average Price", f"₹{avg_price:,.0f}")
    st.subheader(f"🔝 Popular Brands in {category} Category")
    popular_brands = category_data["brand_name"].value_counts().reset_index()
    popular_brands.columns = ["Brand", "Count"]

    fig = px.bar(popular_brands, x="Brand", y="Count",
                 title=f"Popular Brands in {category} Category",
                 color="Brand")
    st.plotly_chart(fig)
    st.subheader(f"📊 Rating Distribution in {category} Category")
    fig = px.histogram(category_data, x="rating_x", nbins=10,
                       title=f"Rating Distribution for {category} Smartphones",
                       color="brand_name", marginal="box")
    st.plotly_chart(fig)
    st.subheader(f"🏅 Top 5 Smartphones by Performance in {category} Category")
    top_5_performance = category_data.sort_values("performance_index", ascending=False).head(5)
    st.dataframe(top_5_performance[["brand_name", "model_name", "price", "performance_index"]])
    st.subheader(f"⭐ Best Smartphone Recommendation in {category} Category")

    # Calculate a 'Value Score' (Performance/Price) for each smartphone
    category_data["value_score"] = category_data["performance_index"] / category_data["price"]

    # Get the smartphone with the highest value score
    best_phone = category_data.loc[category_data["value_score"].idxmax()]

    st.write(f"**{best_phone['brand_name']} - {best_phone['model_name']}**")
    st.write(f"**Price:** ₹{best_phone['price']} | **Performance Index:** {best_phone['performance_index']}")
    st.write(f"**Rating:** {best_phone['rating_x']} ⭐ | **Battery:** {best_phone['battery_capacity(mAh)']} mAh")
    st.subheader(f"📈 Price vs Performance in {category} Category")

    fig = px.scatter(
        category_data,
        x="price",
        y="performance_index",
        color="brand_name",
        hover_data=["model_name"],
        title=f"Price vs Performance in {category} Smartphones"
    )
    st.plotly_chart(fig)
else:
    st.header("📊 Global Smartphone Market Overview")

    total_smartphones = data.shape[0]
    avg_price = data["price"].mean()
    top_brands = data["brand_name"].value_counts().head(3).index.tolist()
    most_common_processor = data["processor_name"].mode()[0]

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Smartphones", total_smartphones)
    col2.metric("Average Price", f"₹{avg_price:,.0f}")
    col3.metric("Top 3 Brands", ", ".join(top_brands))
    col4.metric("Most Common Processor", most_common_processor)
    st.subheader("💰 Smartphone Count by Price Range")
    price_range_count = data["pricewise_cat"].value_counts().reset_index()
    price_range_count.columns = ["Price Range", "Count"]

    fig = px.bar(price_range_count, x="Price Range", y="Count", title="Smartphone Distribution by Price Range")
    st.plotly_chart(fig)
    st.subheader("📊 Brand-Wise Market Share")
    brand_count = data["brand_name"].value_counts().reset_index()
    brand_count.columns = ["brand_name", "count"]
    fig = px.pie(brand_count, values="count", names="brand_name", title="Market Share by Brand")
    st.plotly_chart(fig)
    st.subheader("⚙️ Processor Insights")
    top_processors = data["processor_name"].value_counts().head(10).reset_index()
    top_processors.columns = ["processor_name", "count"]
    fig = px.bar(top_processors, x="processor_name", y="count", title="Top 10 Processors by Count")
    st.plotly_chart(fig)
    st.subheader("🏆 Top Brand by Price Range")
    top_brand_price_range = data.groupby("pricewise_cat")["brand_name"].agg(lambda x: x.mode()[0]).reset_index()
    st.table(top_brand_price_range)
    st.subheader("💵 Average Price by Brand")
    avg_price_brand = data.groupby("brand_name")["price"].mean().reset_index()
    fig = px.bar(avg_price_brand, x="brand_name", y="price", title="Average Price by Brand", color="price")
    st.plotly_chart(fig)
    st.subheader("🌟 Top 5 Smartphones by Rating")
    top_rated_phones = data.sort_values(by="rating_x", ascending=False).head(5)
    st.table(top_rated_phones[["brand_name", "model_name", "price", "rating_x"]])
    st.subheader("📊 Market Share of Processor Brands")
    processor_share = data["processor_brand"].value_counts(normalize=True) * 100
    fig = px.pie(processor_share, values=processor_share.values, names=processor_share.index,
                 title="Market Share of Processor Brands")
    st.plotly_chart(fig)
    st.subheader("💵 Price vs Performance by Processor Brand")
    fig = px.scatter(data, x="price", y="performance_index", color="processor_brand",
                     hover_data=["model_name"], title="Price vs Performance by Processor Brand")
    st.plotly_chart(fig)
    import seaborn as sns
    import matplotlib.pyplot as plt

    st.subheader("🔥 Processor Usage Across Price Ranges")
    pivot = data.pivot_table(index="processor_brand", columns="pricewise_cat", aggfunc="size", fill_value=0)
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(pivot, cmap="YlGnBu", annot=True, ax=ax)
    st.pyplot(fig)
    st.subheader("📊 Camera Megapixel Distribution")
    fig = px.histogram(data, x="rear_primary_resol(MP)", nbins=20, title="Distribution of Camera Megapixels")
    st.plotly_chart(fig)
    st.subheader("🏆 Average Camera Resolution by Brand")
    avg_camera_brand = data.groupby("brand_name")["rear_primary_resol(MP)"].mean().reset_index()

    fig = px.bar(avg_camera_brand, x="brand_name", y="rear_primary_resol(MP)",
                 title="Average Camera Resolution by Brand", color="rear_primary_resol(MP)")
    st.plotly_chart(fig)

# Add more filters for RAM, Storage, and Refresh Rate


# CSS for centering headers and modifying font
st.markdown(
    """
    <style>
    .main .block-container {
        max-width: 1200px;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    </style>
    """, unsafe_allow_html=True
)
