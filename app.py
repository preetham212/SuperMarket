import pandas as pd 
import plotly.express as px  
import streamlit as st 
from PIL import Image
import matplotlib.pyplot as plt

st.set_page_config(page_title="Supermarket Dashboard",  layout="wide")

# @st.cache
def get_data_from_excel():
    
    df=pd.read_csv('supermarkt_sales.csv')
    df["hour"] = pd.to_datetime(df["Time"], format="%H:%M").dt.hour
    df['Date']=pd.to_datetime(df['Date'])
    df['month_name']=df['Date'].dt.month_name()
    return df

df = get_data_from_excel()



st.title("Supermarket Dashboard")
st.markdown("##")

supermImg = Image.open('supermarket.jpg')
st.image(supermImg)



# TOP KPI's
total_sales = int(df["Total"].sum())
avg_rating = round(df["Rating"].mean(), 1)
rating_symbol = ":star:" * int(round(avg_rating, 0))

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Total Sales:")
    st.subheader(f"US $ {total_sales:,}")
with middle_column:
    st.subheader("Average Rating:")
    st.subheader(f"{avg_rating} {rating_symbol}")


st.markdown("""---""")

#Checkboxes
b1=st.sidebar.checkbox('Sales by month & hour')
b2=st.sidebar.checkbox('Product Line')
b3=st.sidebar.checkbox('Payment Method')
    
    # st.write(playersdf[playersdf.FIDE == playersdf.FIDE.max()])
    # st.write("The players witht the higest FIDE average is the top ranked player")
# ---- SIDEBAR ----
if b1:
    st.sidebar.header("Please Filter Here:")
    city = st.sidebar.multiselect(
    "Select the City:",
    options=df["City"].unique(),
    default=df["City"].unique(),
    key="city1"
    )

    gender = st.sidebar.multiselect(
    "Select the Gender:",
    options=df["Gender"].unique(),
    default=df["Gender"].unique(),
    key="gender1"
    )
    
    df_selection = df.query(
        "City == @city & Gender == @gender"
    )
    
    # SALES BY HOUR [BAR CHART]
    hourly_sales = df_selection.groupby(by=["hour"]).sum()[["Total"]]
    fig_hourly_sales = px.bar(
        hourly_sales,
        x=hourly_sales.index,
        y="Total",
        title="<b>Sales by hour</b>",
        color_discrete_sequence=["#0083B8"] * len(hourly_sales),
        template="plotly_white",
    )
    fig_hourly_sales.update_layout(
        xaxis=dict(tickmode="linear"),
        plot_bgcolor="rgba(0,0,0,0)",
        yaxis=(dict(showgrid=False)),
    )
    # left_column, right_column = st.columns(2)
    # left_column.plotly_chart(fig_hourly_sales, use_container_width=True)
    # right_column.plotly_chart(fig_product_sales, use_container_width=True)
    st.write(fig_hourly_sales)


    sales_month = df_selection.groupby(by=["month_name"]).sum()[["Total"]]
    fig_month_sales = px.bar(
        sales_month,
        x=sales_month.index,
        y="Total",
        title="<b>Sales by month</b>",
        color_discrete_sequence=["#0083B8"] * len(sales_month),
        template="plotly_white",
    )
    fig_month_sales.update_layout(
        xaxis=dict(tickmode="linear"),
        plot_bgcolor="rgba(0,0,0,0)",
        yaxis=(dict(showgrid=False)),
    )
    st.write(fig_month_sales)
if b2:
    st.sidebar.header("Please Filter Here:")
    city = st.sidebar.multiselect(
    "Select the City:",
    options=df["City"].unique(),
    default=df["City"].unique(),
    key="city2"
    )
    gender = st.sidebar.multiselect(
    "Select the Gender:",
    options=df["Gender"].unique(),
    default=df["Gender"].unique(),
    key="gender2"
    )
    
    df_selection = df.query(
        "City == @city & Gender == @gender"
    )

    sales_by_product_line = (
        df_selection.groupby(by=["Product line"]).sum()[["Total"]].sort_values(by="Total")
    )
    fig_product_sales = px.bar(
        sales_by_product_line,
        x="Total",
        y=sales_by_product_line.index,
        orientation="h",
        title="<b>Sales by Product Line</b>",
        color_discrete_sequence=["#0083B8"] * len(sales_by_product_line),
        template="plotly_white",
    )
    fig_product_sales.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=(dict(showgrid=False))
    )
    st.write(fig_product_sales)
    
    #products per product_line
    products_product_line = (
        df_selection.groupby(by=["Product line"]).sum()[["Quantity"]].sort_values(by="Quantity")
    )
    fig_products = px.bar(
        products_product_line,
        x="Quantity",
        y=products_product_line.index,
        orientation="h",
        title="<b>Products sold per product line</b>",
        color_discrete_sequence=["#0083B8"] * len(products_product_line),
        template="plotly_white",
    )
    fig_products.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=(dict(showgrid=False))
    )
    st.write(fig_products)
if b3:
    st.sidebar.header("Please Filter Here:")
    city = st.sidebar.multiselect(
    "Select the City:",
    options=df["City"].unique(),
    default=df["City"].unique(),
    key="city3"
    )

    gender = st.sidebar.multiselect(
    "Select the Gender:",
    options=df["Gender"].unique(),
    default=df["Gender"].unique(),
    key="gender3"
    )
    
    df_selection = df.query(
        "City == @city & Gender == @gender"
    )
    payment_method_customers = (
        df_selection.groupby(by=["Payment"]).sum()[["Total"]].sort_values(by="Total")
    )
    fig_payment = px.bar(
        payment_method_customers,
        x="Total",
        y=payment_method_customers.index,
        orientation="h",
        title="<b>Payment methods</b>",
        color_discrete_sequence=["#0083B8"] * len(payment_method_customers),
        template="plotly_white",
    )
    fig_payment.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=(dict(showgrid=False))
    )
    st.write(fig_payment)
