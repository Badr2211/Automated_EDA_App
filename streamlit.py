import plotly.express as px

from distutils.sysconfig import BASE_EXEC_PREFIX
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns 
import warnings
from pandas.plotting import scatter_matrix

# Ignore all warnings
warnings.filterwarnings("ignore")

# Now you can execute your code without being bothered by warnings

#load the data 
def load_data (path):
    
    if path ==None :
        path ='WA_Fn-UseC_-Telco-Customer-Churn.csv'
        extention =path.split('.')[-1]
    else :
        extention =path.name.split('.')[-1]
    if extention == 'csv':
       data = pd. read_csv(path)
    elif extention in ("xls", "xlsx"):
        data = pd. read_excel(path)
    elif extention == 'json' :
       data = json.load(path)
    elif extention == 'txt' :
       with open(file_path, 'r') as file:
            data = file.read()
    elif extention == 'db':
        conn = sqlite3.connect(file_path)
        query = "SELECT * FROM ;"
        data = pd.read_sql(query, conn)
        conn.close()
    else:
        raise ValueError("Unsupported file extension")
    return data

#Explore each feature 
def feature_insight(df,target):
    df_unique = pd .DataFrame([[
                    i,df[i].unique(),
                    df[i].dtypes,
                    df[i].corr(df[target]) if ( df[i].dtypes != 'object' and  df[target].dtypes != 'object') else None,
                    df[i].isna().sum(),
                    len(df[i].unique())] 
                    for i in df.columns],columns=['Feature','Unique Values','dtype','Corr with target','N.null','N.of unique values']).set_index('Feature')
    return df_unique.T

#Clean data
def clean(df,df_ID):
    data =df
    print(data.isnull().sum())
    if data.isnull().sum() .sum() == 0:
        print ('\nNO Null Value')
    else :
        print('\nWarning :Null value ,deal with it')
        for c in data.columns :
            print(c)
            if data[c].dtype !='object' :
                print(c)
                if data[c].isna().sum()> data.shape[0]/4:
                    #print(c,'n')
                    data[c].dropna()
                elif data[c].isna().sum()==0:
                    continue
                else :
                    #print(c,'else')
                    data[c].fillna(data[c].mean(),inplace=True)
            else :
                if data[c] .isna().sum()>0:
                    mode_category = data[c].mode()[0] 
                    data[c].fillna(value=mode_category, inplace=True)
                    
        print(data.isnull().sum())
    if df_ID.is_unique:
        print('\nSample is unique no duplicated')
        
    else :
        print('\ndupplicated , deal with it ...')
        data_unique = data.drop_duplicates(keep='first')
    
    return data

#corr heatmap

def corrplot(data):
    numeric_columns = data.select_dtypes(exclude=['object']).columns
    corr_matrix = data[numeric_columns].corr()

    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0, ax=ax)
    plt.title('Correlation Heatmap')
    st.pyplot(fig)

def num(data):
    num_feature=[i for  i in data.columns  if data[i].dtype !='object']
    return num_feature

def cat(data):
    cat_feature=[i for  i in data.columns  if data[i].dtype =='object']
    return cat_feature

def eda_target(df,target):
    if df[target].dtypes=='object':
        col1 ,col2 = st.columns([3,2])
        with col1:
            st.subheader("Target Variable Distribution")
            st.bar_chart(df[target].value_counts())
        with col2:
            # Create the pie chart with hole using st.pyplot and matplotlib
            fig, ax = plt.subplots()
            target_counts=df[target].value_counts()
            ax.pie(target_counts, labels=target_counts.index, autopct="%1.1f%%", startangle=140 , **{'wedgeprops': dict(width=0.7)})
            st.subheader(" Target Variable Distribution")

            st.pyplot(fig)

        #df[target].value_counts().plot.bar()
    else :
        #fig, ax = plt.subplots()
        #df[target].hist(bins=20, color='lightgreen', edgecolor='black', alpha=0.7, ax=ax)
        col1,col2 = st.columns([.3,.3])
        with col1:
            fig, ax = plt.subplots()
            sns.kdeplot(df[target], ax=ax)

            #   Display the plot in Streamlit
            st.pyplot(fig)
        with col2:
            fig, ax = plt.subplots()
            sns.boxplot(df[target], ax=ax)
            #   Display the plot in Streamlit
            st.pyplot(fig)


def pairplot(df):
    #sns.pairplot(df)
    fig, ax = plt.subplots()

    scatter_matrix(df, alpha=0.8, figsize=(10, 10), diagonal='hist',ax=ax)

    #   Display the plot in Streamlit
    st.pyplot(fig)
        
st.set_page_config(page_title="Explore Your D0ataset", page_icon= ':bar_chart:',                   layout="wide",  
                    initial_sidebar_state="expanded")


with st.sidebar:
    st.image("https://th.bing.com/th/id/OIP.n6a3CTjh1hTTDlLPnSAEKAHaBA?rs=1&pid=ImgDetMain")
    st.title("Automated EDA project")
    st.info ("This project is used to Explore your data set  by easy and interactive dashboard   with preprocessing just upload your data or Explore the project by defult data set (Churn Dataset) :heart_eyes: by:[Mohamed Badr](https://www.linkedin.com/in/mohamed-badr-301378248/?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app) :heart_eyes:")
    file = st.file_uploader("Upload Your Dataset To exlore it and make easy interactive dashboard ,By Defult Churn Data-Set is uploaded ")

    df = load_data(file)
    cat_f= cat(df)
    num_f=num(df)
    target=st.selectbox("Target Column:",df.columns[::-1])

    choice = st.radio("Navigation", ["📋Basic Information And Statistics","📊EDA",'🎮Play With Feature Visulaizations'])


if choice== "📋Basic Information And Statistics":
    st.image('https://www.datasciencedegreeprograms.net/wp-content/uploads/2021/08/shutterstock_1642441465-2048x1225.jpg')
    st.header("1-Sample Of Data")
   
    st.dataframe(df.sample())
    
    st.header("2-Exploratory each feature")
    st.dataframe(feature_insight(df,target))
    
    st.header('3-Statistics')
    st.dataframe(df.describe())
        

if choice == "📊EDA":
    st.title('Exploratory Data analysis')
    st.image('https://th.bing.com/th/id/OIP.I9CAlMorFphXUKDzzIVqRgHaD4?rs=1&pid=ImgDetMain')
    st.header("1-Target analysis")
    eda_target(df,target)


    st.header("2-Correlation Map")
    #corrplot(df)
   
    st.header("2-Pair Plot")
    #pairplot(df)
if choice =="🎮Play With Feature Visulaizations":
    #with st.sidebar:
    #st.image("https://th.bing.com/th/id/OIP.n6a3CTjh1hTTDlLPnSAEKAHaBA?rs=1&pid=ImgDetMain")
    st.title("Play With Feature Visulaizations")
    tap1 ,tap2,tap3 = st.tabs( ["Scatter","Histogram",'boxplot'])
    with tap1:
        fig, ax = plt.subplots()
        col1 ,col2,col3,col4 =st.columns([.5,.5,.5,.5])
        with col1:
            x = st.selectbox("1Chose Feature To Put in X-axis ",num_f )
        with col2:
            y = st.selectbox("2Chose Feature To Put in Y-axis ",num_f )
        with col3:
            color = st.selectbox("Color ",[None]+num_f )
        with col4:
            size = st.selectbox("Size",[None]+num_f )
                                             
        fig=px.scatter(df,x,y,color=color,size=size)
        #=sns.regplot(x=x ,y=y ,data=df,ax=ax)
        st.plotly_chart(fig)

        #   Display the plot in Streamlit
        #st.pyplot(fig)
        
    with tap2:    
        fig, ax = plt.subplots()
        x = st.selectbox("Chose Feature To Put in X-axis  ",num_f )
        sns.histplot(x=x  ,data=df,ax=ax)
        #   Display the plot in Streamlit
        st.pyplot(fig)
        
    with tap3:
        fig, ax = plt.subplots()
        col1 ,col2 =st.columns([.5,.5])
        with col2:
            x = st.selectbox("Chose Feature To Put in X-axis   ",cat_f )
        with col1:
            y = st.selectbox("Chose Feature To Put in Y-axis ",num_f )
       
        sns.boxplot(x=x,y=y  ,data=df,ax=ax)
        #   Display the plot in Streamlit
        st.pyplot(fig)
        