import pandas as pd
import numpy as np
import streamlit as st
from itertools import product
from PIL import Image #to add image




#Main config
st.set_page_config(page_title="4ce-phenotyping", layout="wide" , initial_sidebar_state="auto") #why here? set_page_config() can only be called once per app, and must be called as the first Streamlit command in your script.


df = pd.read_csv("data/Disengagement_Milage_Collision_2019_2021_ver2_modified1_temp.csv")

#Filter the columns based on this
filter = ['Disengagement', 'Mileage', 'Mileage_Driverless',  'Collision', 'Disengagement_per_Mile', 'Collision_per_Mile', 'Disengagement_if_initiated_by_AV_per_Mile','without_a_driver_=_Yes', 'Collision if injury per Mile']

#selectbox control
column = st.selectbox("select the parameter", filter)

df = df[['Manufacturer', 'Year', column]]
st.write(df)



def bump(df): #dataframe and the number of unique time intervals
  df = ro.conversion.py2rpy(df)
  r = robjects.r
  r['source']('Rank_pheno.R')
  bump_func = robjects.globalenv['bump_rank']
  return bump_func(df)





#
##define the scope of the files
#st.sidebar.markdown('''--------------------''')
#file = st.sidebar.selectbox("Select the recording date:", ['60 days', '90 days'])
#
## EXTRA CSS--------
#st.markdown(
#    """
#<style>
#.reportview-container .markdown-text-container {
#    font-family: monospace;
#}
#.sidebar .sidebar-content {
#    background-image: linear-gradient(#2e7bcf,#2e7bcf);
#    color: white;
#}
#.Widget>label {
#    color: black;
#    font-family: monospace;
#}
#[class^="st-b"]  {
#
#    font-family: monospace;
#}
#
#.st-at {
#    padding-right: 35px;
#}
#footer {
#    font-family: monospace;
#}
#
#header .decoration {
#    background-image: none;
#}
#
#</style>
#""",
#    unsafe_allow_html=True,
#)
#
#
#
#
#
#st.markdown(
#        f"""
#<style>
#    .reportview-container .main .block-container{{
#        max-width: 900px;
#        padding-top: 0rem;
#        padding-right: 0rem;
#        padding-left: 0rem;
#        padding-bottom: 0rem;
#    }}
#</style>
#""",
#        unsafe_allow_html=True,
#    )
#
##Horizontal radio buttons
#st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
#
##-----To remove streamlit's toolbar-----
#hide_streamlit_style = """
#            <style>
#            #MainMenu {visibility: hidden;}
#            footer {visibility: hidden;}
#            </style>
#            """
#st.markdown(hide_streamlit_style, unsafe_allow_html=True)
#
##to diffrenciate between 60 and 90 data
#df_lists_60 = []
#df_lists_90 = []
#
#uploaded_files = st.file_uploader("Select file(s)", accept_multiple_files=True)
#for uploaded_file in uploaded_files:
#     file_name = uploaded_file.name
#     site_name = file_name.split('_')[1]
#     record_day = file_name.split('_')[2]
##     st.write(file_name)
#     df_uploaded = upload(uploaded_file)
#     if record_day == '60':
#        df_lists_60.append(df_uploaded)
#     elif record_day == '90':
#        df_lists_90.append(df_uploaded)
#     else:
#        st.warning("At least one of the uploaded files does not match the project's naming standard.")
#
#
#
#st.markdown('''--------------------''')
#
##To import files one bye one
##cols = st.columns(2)
##Upitt = cols[0].file_uploader("Please select the UPitt file")
##MGB = cols[1].file_uploader("Please select the MGB file")
##NWU = cols[0].file_uploader("Please select the NWU file")
##
##df_lists = []
##if MGB is not None:
##    MGB = upload(MGB)
##    df_lists.append(MGB)
##
##if Upitt is not None:
##    Upitt = upload(Upitt)
##    df_lists.append(Upitt)
##
##if NWU is not None:
##    NWU = upload(NWU)
##    df_lists.append(NWU)
#
#if file == '60 days':
#    df_lists = df_lists_60
#else:
#    df_lists = df_lists_90
#
#if len(df_lists)>0:
#    if len(df_lists) ==1:
#        df = df_lists[0]
#    else:
#        for i in range (0, len(df_lists)-1):
#            df = df_lists[i].append(df_lists[i+1])
#    # Defining the controllers
#    cols = st.columns(2) #to list the filters in two columns
#    phenotypes = list(df['aoi'].unique())
#    features = list(df['feature'].unique())
#    types = list(df['type'].unique())
#    times = ['0-29', '30-59', '60-89', '90+']
#    aoi = st.multiselect("Drop Phenotypes from the Visualization", phenotypes, phenotypes)
#    type_select = cols[0].selectbox("Select the Feature Type", ["All"]+types)
#
##    #Slider Feature
##    values = st.slider(
##         'Select a range of OR',
##         0.0, max(df['OR']), (0.25, max(df['OR']-0.01)))
##
#    #OR filter
#    OR = st.radio("Filter by OR:", (">1", "<1", "All"))
#
#    #Apply the filters on the dataframe
##    df = df.query('OR>=@values[0] and OR<=@values[1] and aoi in @aoi')
#    if OR == ">1":
#        df = df.query('OR>1')
#        OR_b = False
#    elif OR == "<1":
#        df = df.query('OR<1')
#        OR_b = True
#        if df.empty:
#            st.warning("There is no feature to show!")
#
#
#    if not df.empty:
#        if type_select != 'All':
#            df = df.query('type == @type_select')
#
#    #    # Defining the controllers
#    #    st.write(df['time'].value_counts())
#    #    st.write(df['aoi'].value_counts())
#    #    st.write(df['feature'].value_counts())
#    #    st.write(df['type'].value_counts())
#
#        #Counting features throughout the (combined) df
#        df2 = df.groupby(['time', 'feature']).size().reset_index(name='counts')
##        df2.to_csv("df.csv", index=False)
#
#        # making sure for all lanes we have all of the features
#        df_test = df[['time','feature']]
#        df_test['counts'] = 0
#        uniques = [df_test[i].unique().tolist() for i in df_test.columns]
#        df_combo = pd.DataFrame(product(*uniques), columns = df_test.columns)
#    #    st.write(df_combo)
#
#        #Final df
#        result = pd.concat([df_combo, df2]).groupby(['time','feature'])['counts'].sum().reset_index()
#        result = result.fillna(0)
#        len = len(result['time'].unique()) #This will be used in R for the number of lanes
##        result.to_csv("df.csv", index=False)
#
##        bump(df2,len,type_select,OR_b)
##        image = Image.open('Images/rank.jpeg')
##        cols = st.columns([1,3,1])
##        cols[1].image(image)
##        st.markdown('''----------------''')
##        st.markdown("Fully Connected Plot")
#
#        bump(result,len,type_select,OR_b)
#        image = Image.open('Images/rank.jpeg')
#        cols = st.columns([1,3,1])
#        cols[1].image(image)
