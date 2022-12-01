import streamlit as st
import pandas as pd
import altair as alt
import datetime
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
from PIL import Image

@st.cache(allow_output_mutation=True)
def load_data():
    df = pd.read_csv('supermarket_sales - Sheet1.csv')
    df["hour"] = pd.to_datetime(df["Time"], format="%H:%M").dt.hour
    df['Date']=pd.to_datetime(df['Date'])
    df['month_name']=df['Date'].dt.month_name()
    return df

st.set_page_config(page_title="SuperMarket",layout='wide')
st.title("Supermarket Dashboard")
st.markdown("##")

supermImg = Image.open('supermarket.jpg')
st.image(supermImg)

# load the data
df = load_data()

selectionBoard = st.sidebar.selectbox('Dashboard',['Total Revenue', 'Product Data', 'Miscellaneous'])

if selectionBoard == 'Product Data':
    st.write("Sales Data")
    city = st.sidebar.multiselect("Select the City:",
        options=df["City"].unique(),
        default=df["City"].unique())

    customertype = st.sidebar.multiselect(
    "Select the Customer Type:",
    options=df["Customer_type"].unique(),
    default=df["Customer_type"].unique())

    gender = st.sidebar.multiselect(
    "Select the Gender:",
    options=df["Gender"].unique(),
    default=df["Gender"].unique())

    df_selection = df.query("City == @city & Gender == @gender & Customer_type == @customertype" )

    total_sales = int(df_selection["Total"].sum())
    average_sale_by_transaction = round(df_selection["Total"].mean(), 2)
    
    left_column, right_column = st.columns(2)
    with left_column:
        st.subheader("Total Sales:")
        st.subheader(f"US $ {total_sales:,}")
    with right_column:
        st.subheader("Average Sales Per Transaction:")
        st.subheader(f"US $ {average_sale_by_transaction}")

    product_line_sales = (
    df_selection.groupby(by=["Product line"]).sum()[["Total"]].sort_values(by="Total"))

    product_sales_chart = px.bar(
        product_line_sales,
        x="Total",
        y=product_line_sales.index,
        orientation="h",
        title="<b>Sales by Product Line</b>",
        color_discrete_sequence=["#0083B8"] * len(product_line_sales),
        template="plotly_white")
    product_sales_chart.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=(dict(showgrid=False)))

   
    st.plotly_chart(product_sales_chart, use_container_width=True)

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

elif selectionBoard == 'Miscellaneous':
    df_group = df.groupby(['City','Payment'])['Total'].sum().reset_index()
    df_group_product = df.groupby(['City','Gender', 'Product line'])['Unit price'].sum().reset_index()
    option = st.sidebar.multiselect('Choose a City',df['City'].unique(), default=df['City'].unique())
    source = df_group_product[df_group_product['City'].isin(option)]
    
    if st.sidebar.checkbox('Total Unit Price'):
        product_chart = alt.Chart(source).mark_bar().encode(
            x=alt.X('Product line', title = 'Product'),
            y=alt.Y('Unit price', title = 'Unit Price'),
            color='Product line',
            column='City'
        ).properties(
            title = 'Total Unit Price for Product',
            height = 300,
            width = 300
        )
        st.write(product_chart)

    df['month'] = pd.DatetimeIndex(df['Date']).month
    df_group_month = df.groupby(['City','month'])['Total'].sum().reset_index()
    source_df = df[df['City'].isin(option)]
    clickon=alt.selection(type='single', empty='all', fields=['Payment'])

    if st.sidebar.checkbox('Payment Type'):
        product_chart1 = alt.Chart(source_df).mark_bar().encode(
            x=alt.X('count(Payment):Q', title = 'Count'),
            y=alt.Y('Payment', title = 'Payment'),
            color='Payment',
            column = 'City'
        ).properties(
            title = 'Total Payment Type',
            height = 300,
            width = 300
        )
        st.write(product_chart1)

    if st.sidebar.checkbox('Membership'):
        product_count = alt.Chart(source_df).mark_bar().encode(
            x=alt.X('Customer_type', title = 'Customer Type'),
            y=alt.Y('count(Customer_type):Q', title = 'Count'),
            color='City',
            column = 'City'
        ).properties(
            title = 'Membership vs Regular',
            height = 300,
            width = 300
        )
        st.write(product_count)

    if st.sidebar.checkbox('Product Line'):
        product_count = alt.Chart(source_df).mark_bar().encode(
            x=alt.X('count(Product line):Q', title = 'Count'),
            y=alt.Y('Product line', title = 'Product'),
            color='City',
        ).properties(
            title = 'Product Line Count',
            height = 300,
            width = 1000
        )
        st.write(product_count)
    
    if st.sidebar.checkbox('Date of Purchase'):
        product_chart2 = alt.Chart(source_df).mark_point().encode(
            x=alt.X('Date', title = 'Date'),
            y=alt.Y('Total', title = 'Total Cost'),
            color='City',
            tooltip =['Total','Date','City','Gender','Product line']
        ).properties(
            title = 'Total Cost per Transaction',
            height = 300,
            width = 1500
        ).interactive()
        st.write(product_chart2)

else:

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

    # TOP KPI's
    total_sales = int(df_selection["Total"].sum())
    avg_rating = round(df_selection["Rating"].mean(), 1)
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
    b3=st.sidebar.checkbox('Payment Method')
        
        # st.write(playersdf[playersdf.FIDE == playersdf.FIDE.max()])
        # st.write("The players witht the higest FIDE average is the top ranked player")
    # ---- SIDEBAR ----

    if b1:
        # SALES BY HOUR [BAR CHART]
        gross_income= df_selection.groupby(["City"])["gross income"].sum()

        fig_gross_income = px.bar(
            gross_income,
            x=gross_income.index,
            y="gross income",
            title="<b>Gross income per City</b>",
            color_discrete_sequence=["#0083B8"] * len(gross_income),
            template="plotly_white",
        )

        st.write(fig_gross_income)

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
    if b3:
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

