# Get the covariates and construct the dataset

def get_dataset():
    
# Covariate 1: Functioning of Government (FOG) index by Freedom House

    FOG = pd.read_excel('FOG index 2003-2018.xlsx',sheet_name="FIW2010") 
    FOG = FOG.iloc[:, : 10].drop(columns=["Country/Territory",'Status','PR Rating','CL Rating','A Aggr', 'B Aggr'], axis=1)
    FOG =FOG.rename(columns={"C Aggr":"FOG"}) 

# Covariate 2: Corruption
    corruption=pd.read_excel("World Governance Indicators, control of corruption 2018.xlsx", sheet_name="COC")
    df1 =FOG.merge(corruption, on="Country", how="left")

# Covariate 3: Regularoty Quality
    regqual=pd.read_excel("World Governance Indicators, control of corruption 2018.xlsx", sheet_name="REG")

    df2=df1.merge(regqual,on="Country", how="left")

# Covariate 4: Government Effectiveness
    gov_eff=pd.read_excel("World Governance Indicators, control of corruption 2018.xlsx", sheet_name="GOV")

    df3=df2.merge(gov_eff,on="Country", how="left")

# Covariate 5: Polity IV from Teytelbom
    polityIV = pd.read_excel("polityIV.xls", sheet_name="2010")
    df4 = df3.merge(polityIV, on="Country", how='left')

# Covariate 6: EU dummy 
    EU = pd.read_excel("EU.xlsx")
    df5 = df4.merge(EU,left_on="Country", right_on="country", how="left")
    df5.EU = df5.EU.fillna(0)
    df5.EU = df5.EU.astype(int)
    df5 = df5.drop("country",axis=1)


# Covarite 7: Gallup on Environmental Awareness  
    
    gallup = pd.read_excel('Gallup on Environmental Awareness 2010.xlsx') 
    gallup = gallup.rename(columns={2010:"Gallup"})

# This data comes from https://news.gallup.com/poll/147203/Fewer-Americans-Europeans-View-Global-Warming-Threat.aspx

    gallup = gallup.drop(2008,axis=1)
    gallup['country'] = gallup['country'].replace("Slovakia",'Slovak Republic')
    gallup['country'] = gallup['country'].replace("Kyrgyzstan",'Kyrgyz Republic')
    df6 = df5.merge(gallup, left_on= "Country", right_on= "country", how="left" )
    df6[df6.Gallup.isna()] 

# France, Switzerland and Norway etc. is missing in Gallup 2010 dataset! Gallup question asks the knowledge on climate change.
# Imputing  manually from 2007 / 2008
    df6.loc[2, "Gallup"] = 93  # france
    df6.loc[5, "Gallup"] = 97  #norway
    df6.loc[21, "Gallup"] = 95 # iceland
    df6.loc[87, "Gallup"] = 49 # madagascar
    df6.loc[89, "Gallup"] = 54 # mozambiq
    df6.loc[65, "Gallup"] = 30 # rwanda
    df6.loc[39, "Gallup"] = 88 # estonia
    df6.loc[34, "Gallup"] = 91 # latvia
    df6.loc[86, "Gallup"] = 22 # burundi
    df6 = df6.drop("country", axis=1)

# Covarite 8: Trust % in others from minx and lamb # World values survey
    trust = pd.read_excel("self trust.xls") 
    df7 = df6.merge(trust, on="Country", how='left')

# Covarite 9: vulnerability
    vul = pd.read_excel("vulnerability.xls", sheet_name="Sheet1")
    df8= df7.merge(vul, on="Country", how="left")

# Covarite 10: GDP in billion dollars  from fossil % GDP spread sheet 
    GDP = pd.read_excel("GDP.xlsx")
    df9= df8.merge(GDP,left_on="Country", right_on= "country" , how='left')

# Covarite 11: GDP per capita
    GDP_pc = pd.read_excel("GDPpercap.xls", sheet_name="2010")
    df10= df9.merge(GDP_pc, on="Country", how="left")


# Covarite 12/ 13: Renewables as total cons. and electricity output # 2000 or 2015 Worldbank 

    renewable = pd.read_excel('Renewables.xlsx', sheet_name="Sheet2")
    df11=df10.merge(renewable,on="Country", how="left")

# Covarite 14: gas and oil rents % GDP # Minx and Lamb # kendim gas ve oil icin topladim Worldbank
    gas_oil_rent = pd.read_excel("gas and oil rents.xls", sheet_name="2010")
    df12 = df11.merge(gas_oil_rent, on="Country", how='left')
    df12 = df12.drop(["gas","oil"],axis=1)

#  Covarite 15: coal rents % GDP 
    coal_rent = pd.read_excel("coal.xls", sheet_name="2010")
    df13 = df12.merge(coal_rent, on="Country", how='left')

# Covarite 16: coal in % electricity production
    coal_elec = pd.read_excel("elect from coal.xls", sheet_name="2010")
    df14 = df13.merge(coal_elec, on="Country", how='left')

# Covarite 17: Fossil % GDP
    fossil = pd.read_excel('fossilGDP.xlsx')
    fossil =fossil.rename(columns={2010:'fossil_GDP'})
    df = df14.merge(fossil, on="Country", how='left')

    df = df.drop("country", axis=1)
    df.drop(["Add A", "Year"], axis=1, inplace=True)
    return df
