import os
import ssl
import math
import requests
import subprocess
import numpy as np
import pandas as pd
import streamlit as st
from urllib import request
from bs4 import BeautifulSoup

st.set_page_config(
    page_title="Smart Cart | All at One Place",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

dfPrimary = pd.DataFrame()
specsList = []

def writeToExcel(df):
    global dfPrimary  
    dfPrimary = pd.concat([dfPrimary, df], ignore_index=True, axis=0)
    dfPrimary.to_csv("ProductDetails.csv", index=False)
       
def CrawlAmazon(amazon, tries):

    
    header = ({'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})
    
    web = requests.get(amazon, headers= header)
    print(amazon)
    print(web)
    soup =  BeautifulSoup(web.content, 'lxml')

    names = []
    prices = []
    ratings = []
    estTime = []
    links = []

    blockcontent = soup.find_all("div", class_="a-section a-spacing-base")
    if blockcontent:
        for block in blockcontent:
                namecontent = block.find("span", class_="a-size-base-plus a-color-base a-text-normal")
                if namecontent:
                    names.append(namecontent.text)

                    ratingContent = block.find("span", class_="a-icon-alt")
                    if ratingContent:
                        ratings.append(ratingContent.string[:3])
                    else:
                        ratings.append('NA')

                    linkcontent = block.find("a", class_="a-link-normal s-no-hover s-underline-text s-underline-link-text s-link-style a-text-normal")
                    if linkcontent:
                        links.append("https://www.amazon.in" + linkcontent.get("href"))
                    else:
                        links.append('NA')

                    pricecontent = block.find("span", class_="a-offscreen")
                    if pricecontent:
                        price_str = pricecontent.text.replace('₹', '').replace(',', '')  
                        try:
                            price = int(price_str)
                            prices.append(price)
                        except ValueError:
                            prices.append('NA')
                    else:
                        prices.append('NA')

                    timecontent = block.find("span", class_="a-color-base a-text-bold")
                    if timecontent:
                        estTime.append(timecontent.string)
                    else:
                        estTime.append('NA')
    else:
        blockcontent = soup.find_all("div", class_="a-section")
        if blockcontent:
            for block in blockcontent:
                namecontent = block.find("span", class_="a-size-base-plus a-color-base a-text-normal")
                if namecontent:
                    names.append(namecontent.text)
                    ratingContent = block.find("span", class_="a-icon-alt")
                    if ratingContent:
                        ratings.append(ratingContent.string[:3])
                    else:
                        ratings.append('NA')

                    linkcontent = block.find("a", class_="a-link-normal s-no-hover s-underline-text s-underline-link-text s-link-style a-text-normal")
                    if linkcontent:
                        links.append("https://www.amazon.in" + linkcontent.get("href"))
                    else:
                        links.append('NA')

                    pricecontent = block.find("span", class_="a-offscreen")
                    if pricecontent:
                        price_str = pricecontent.text.replace('₹', '').replace(',', '')  
                        try:
                            price = int(price_str)
                            prices.append(price)
                        except ValueError:
                            prices.append('NA')
                    else:
                        prices.append('NA')

                    timecontent = block.find("span", class_="a-color-base a-text-bold")
                    if timecontent:
                        estTime.append(timecontent.string)
                    else:
                        estTime.append('NA')

    min_length = min(len(names), len(prices), len(ratings), len(estTime), len(links))
    names = names[:min_length]
    prices = prices[:min_length]
    ratings = ratings[:min_length]
    estTime = estTime[:min_length]
    links = links[:min_length]

    df = pd.DataFrame({
                        'Website' : 'Amazon',
                        'Name': names,
                        'Price' : prices,
                        'Ratings' : ratings,
                        'Time' : estTime,
                        'Link' : links})
    
    # print(df)
    if df.empty:
        if tries == 20:
            return
        else:
            CrawlAmazon(amazon, tries + 1 )
    writeToExcel(df)
    print("Data found from Amazon")
    
def crawlFlipkart(flipkart):   
   
    web = requests.get(flipkart)
    print(flipkart)
    print(web)
    soup =  BeautifulSoup(web.content,"html.parser")

    names = []
    prices = []
    ratings = []
    estTime = []
    links = []

    blockContent = soup.find_all("div", class_="_2kHMtA")
    if(blockContent):
        for block in blockContent:
            if (block):
                namecontent = block.find("div", class_="_4rR01T")
                if namecontent:
                    names.append(namecontent.text)

                    ratingContent = block.find("div", class_="_3LWZlK")
                    if ratingContent:
                        ratings.append(ratingContent.text)
                    
                    else:
                        ratings.append('NA')

                    linkcontent = block.find("a", class_="_1fQZEK")
                    if linkcontent:
                        links.append("https://www.flipkart.com" + linkcontent.get("href"))
                    else:
                        links.append('NA')

                    pricecontent = block.find("div", class_="_30jeq3 _1_WHN1")
                    if pricecontent:
                        price_str = pricecontent.text.replace('₹', '').replace(',', '')  
                        try:
                            price = int(price_str)
                            prices.append(price)
                        except ValueError:
                            prices.append('NA')
                    else:
                        prices.append('NA')

                    tempvar = links[len(links) - 1]
                    if(tempvar != "NA"):
                        tempweb = requests.get(tempvar)
                        tempsoup = BeautifulSoup(tempweb.content, "lxml")
                        timecontent = tempsoup.find("span", class_="_1TPvTK")
                        if timecontent:
                            estTime.append(timecontent.text)
                        else:
                            estTime.append('NA')
    else:
        blockContent = soup.find_all("div", class_="_4ddWXP") 
        if(blockContent):
            for block in blockContent:
                if (block):
                    namecontent = block.find("a", class_="s1Q9rs")
                    if namecontent:
                        names.append(namecontent.text)

                        ratingContent = block.find("div", class_="_3LWZlK")
                        if ratingContent:
                            ratings.append(ratingContent.text)
                        
                        else:
                            ratings.append('NA')

                        linkcontent = block.find("a", class_="s1Q9rs")
                        if linkcontent:
                            links.append("https://www.flipkart.com" + linkcontent.get("href"))
                        else:
                            links.append('NA')

                        pricecontent = block.find("div", class_="_30jeq3")
                        if pricecontent:
                            price_str = pricecontent.text.replace('₹', '').replace(',', '')  
                            try:
                                price = int(price_str)
                                prices.append(price)
                            except ValueError:
                                prices.append('NA')
                        else:
                            prices.append('NA')

                        tempvar = links[len(links) - 1]
                        if(tempvar != "NA"):
                            tempweb = requests.get(tempvar)
                            tempsoup = BeautifulSoup(tempweb.content, "lxml")
                            timecontent = tempsoup.find("span", class_="_1TPvTK")
                            if timecontent:
                                estTime.append(timecontent.text)
                            else:
                                estTime.append('NA')

    min_length = min(len(names), len(prices), len(ratings), len(estTime), len(links))
    names = names[:min_length]
    prices = prices[:min_length]
    ratings = ratings[:min_length]
    estTime = estTime[:min_length]
    links = links[:min_length]

    df = pd.DataFrame({
                        'Website' : 'Flipkart',
                        'Name': names,
                        'Price' : prices,
                        'Ratings' : ratings,
                        'Time' : estTime,
                        'Link' : links})
    
    # print(df)
    writeToExcel(df)
    print("Data found from Flipkart")

def crawlSnapdeal(snapdeal): 

    header = ({'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})
    
    web = requests.get(snapdeal, headers= header)
    print(snapdeal)
    print(web)
    soup =  BeautifulSoup(web.content, 'lxml')

    names = []
    prices = []
    ratings = []
    estTime = []
    links = []

    linkcontent = soup.findAll("a", class_="dp-widget-link noUdLine")
    for i in range(0, len(linkcontent), 2):
        href = linkcontent[i].get('href')
        if href:
            tempweb = requests.get(href)
            tempsoup = BeautifulSoup(tempweb.content,"lxml")
            namecontent = tempsoup.find("div", class_="col-xs-22")
            if namecontent:
                # print(namecontent)
                names.append(namecontent.text.strip())
            else:
                names.append("NA")
   
            pricecontent = tempsoup.find("span", class_="payBlkBig")
            if pricecontent:
                prices.append(pricecontent.text)
            else:
                prices.append("NA")
    
            ratingContent = tempsoup.find("span", class_="avrg-rating")
            if (ratingContent):
                ratings.append(ratingContent.string[1:-1])
            else:
                ratings.append("NA")

            timecontent = tempsoup.find('p', class_="expect-delvry")
            if timecontent:
                estTime.append(' '.join(timecontent.stripped_strings))
            else:
                estTime.append("NA")

            links.append(href)
    
    min_length = min(len(names), len(prices), len(ratings), len(estTime),len(links))
    names = names[:min_length]
    prices = prices[:min_length]
    ratings = ratings[:min_length]
    estTime = estTime[:min_length]
    links = links[:min_length]
    df = pd.DataFrame({
                        'Website' : 'Snapdeal',                
                        'Name': names,
                        'Price' : prices,
                        'Ratings' : ratings,
                        'Time' : estTime,
                        'Link' : links,
                        })
    
    # print(df)
    writeToExcel(df)
    print("Data found from Snapdeal")

def crawlAlibaba(Alibaba):   

    header = ({'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})
   
    web = requests.get(Alibaba, headers= header)
    print(Alibaba)
    print(web)
    soup =  BeautifulSoup(web.content,"html.parser")

    names = []
    prices = []
    ratings = []
    estTime = []
    links = []

    blockcontent = soup.find_all("div", class_="product-card-gallery product-card")
    if blockcontent:
        for block in blockcontent:
            linkcontent = block.find("a", class_="product-image")
            specificLink = ""
            if linkcontent:
                href = linkcontent.get('href')  
                if href:
                    specificLink = href + "+india.html"
            else:
                links.append('NA')

            ratingContent = block.find("div", class_="product-review-score")

            if(specificLink):
                tempweb = requests.get(specificLink)
                tempsoup = BeautifulSoup(tempweb.content, "lxml")
        
                namecontent = tempsoup.find("div", class_="product-title-container")
                if namecontent:
                    names.append(namecontent.text)
                   
                    if ratingContent:
                        ratings.append(ratingContent.text)
                    else:
                        ratings.append('NA')

                    pricecontent = tempsoup.find("div", class_="price")
                    if pricecontent:
                            prices.append(pricecontent.text)
                    else:
                        prices.append('NA')
                    
                    estTime.append("NA")
                    links.append(specificLink)

    min_length = min(len(names), len(prices), len(ratings), len(estTime), len(links))
    names = names[:min_length]
    prices = prices[:min_length]
    ratings = ratings[:min_length]
    estTime = estTime[:min_length]
    links = links[:min_length]
    df = pd.DataFrame({
                        'Website' : 'Alibaba',
                        'Name': names,
                        'Price' : prices,
                        'Ratings' : ratings,
                        'Time' : estTime,
                        'Link' : links})
    
    # print(df)
    writeToExcel(df)
    print("Data found from Alibaba")
    
def urlFormation(product, specsList):
    
    amazon = ""
    amazon = amazon + "https://www.amazon.in/s?k=" + product
    
    flipkart = ""
    flipkart = flipkart + "https://www.flipkart.com/search?q=" + product

    snapdeal = ""
    snapdeal = snapdeal + "https://www.snapdeal.com/search?keyword="  + product
    
    alibaba = ""
    alibaba = alibaba +  "https://www.alibaba.com/showroom/" + product

    for i in specsList:
        amazon += '+' + i
        snapdeal += '+' + i
        alibaba += '+' + i
        flipkart += '+' + i

    CrawlAmazon(amazon,0)
    crawlFlipkart(flipkart)
    crawlSnapdeal(snapdeal)
    alibaba = alibaba + "+india.html"
    crawlAlibaba(alibaba)

    col1,col2,col3 = st.columns([1,10,1])
    with col2:
        print_analysis_to_screen()

def crawling():
    st.markdown("<h1 style='font-size: 7em; text-align: center; color:lightblue'>SMART CART</h1>", unsafe_allow_html=True)
    container_style = """
    border-radius: 3px;
    padding: 1px;
    background-color: beige;
    box-shadow: 2px 2px 5px grey;
    height : 8px
    """
    st.markdown(
        f"""
        <div style="{container_style}">
            <h1 style=' font-size : 1em; text-align: center;color: black;'></h1>
        </div>
        """,
        unsafe_allow_html=True
    )
    for _ in range(7):
        st.write("")
    
    col1, col2, col3 = st.columns([1,4,1])
    with col2:
        st.markdown("<h5 style='font-size:1.5em; text-align: center; color:lightblue'>ENTER PRODUCT DETAILS:</h5>", unsafe_allow_html=True)
        # st.write("ENTER PRODUCT DETAILS:")
        product = st.text_input("Enter Product")
        product = product.replace(" ","+")

        specs = st.text_input("Enter specifications : ( colon separated ) ")

        global specsList
        specs = specs.replace(": ", "" ).replace(" ", "+").replace("\t", "+").replace("\n", "+")
        specsList = specs.split(":")
        
        if st.button("Search", type = "primary"):
            urlFormation(product, specsList)

def dollar_to_ruppee(dollar):
    url = 'https://open.er-api.com/v6/latest/USD'

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        
        # Get the current value of 1 USD in terms of Indian Rupees (INR)
        usd_to_inr = data['rates']['INR']
        ruppee = round(dollar * usd_to_inr, 1)
        return ruppee
    else:
        print("Failed to retrieve data from the API.")
        return

def clean_price(price):
    price = str(price).replace(',', '')
    if price.startswith('US$') and price.endswith('/piece'):
        dollar_price = float(price[3:-6])
        return dollar_to_ruppee(dollar_price)
    else:
        return price

def analysis():
    global dfPrimary
    df = dfPrimary
    global specsList
    specsList = [spec.replace('+', ' ') for spec in specsList]

    # Data Cleaning and Preprocessing
    # print(df)
    df = df.dropna(subset=['Price'])
    df.loc[:, 'Price'] = df['Price'].apply(clean_price)
    df.loc[:, 'Ratings'] = pd.to_numeric(df['Ratings'], errors = 'coerce')
    df = df.dropna(subset=['Ratings'])
    df.loc[:, 'Price'] = pd.to_numeric(df['Price'] , errors = 'coerce')
    df = df.dropna(subset=['Price'])

    df['Price'] = df['Price'].astype(np.float64)

    # Convert search terms to lowercase for case-insensitive matching
    specs_lower = [spec.lower() for spec in specsList]
    df['_lowercase_name'] = df['Name'].str.lower()

    # Filter rows based on specsList (case-insensitive)
    mask = df['_lowercase_name'].apply(lambda x: any(word in x for spec in specs_lower for word in spec.split()))
    df = df[mask]  # Keep only the rows that match the specsList

    df.drop('_lowercase_name', axis=1, inplace=True)

    total_records = df.Name.count()
    
    quartile = round((75/100)* total_records)

    df_sorted = df.sort_values(by=['Price', 'Ratings', 'Time'], ascending=[True, False, True])

    return df_sorted[:quartile]


def print_analysis_to_screen():
    if specsList:  # Check if specsList is not empty
        df = analysis()
        st.markdown("<h5 style='font-size:1.5em; text-align: center; color:lightblue'>BEST PRODUCTS:</h5>", unsafe_allow_html=True)

        df['Ratings'] = df['Ratings'].apply(lambda x: '⭐' * math.ceil(x))
        df['Price'] = '₹ ' + df['Price'].astype(str)

        st.markdown("""
            <style>
                table {
                    font-family: Arial, sans-serif;
                    border-collapse: collapse;
                    text-align : center;                    
                }
                
                th, td {
                    border: 1.5px solid #f50707;  
                    margin-bottom: 3px;
                    text-align: left;
                    padding: 40px;            
                }
                
                th {
                    background-color: #4db3f7;  
                    opacity: 0.8;
                }
                                
                .link-text {
                    color: #0000EE;
                    text-decoration: underline;
                    cursor: pointer;
                }

            </style>
        """, unsafe_allow_html=True)
        df['Link'] = df['Link'].apply(lambda x: f'<a href="{x}">Open link</a>')

        # Display DataFrame as HTML
        st.write(df.to_html(escape=False), unsafe_allow_html=True)

crawling()
