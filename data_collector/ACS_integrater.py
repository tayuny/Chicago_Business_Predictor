import pandas as pd
import numpy as np

####################################################################################################################
# preprocess ACS data between 2012 to 2017

table_dict = {"total_population": {"table": "B01003", "zip": "GEO.id2", "variable":"HD01_VD01"}, 
              "median_household_income": {"table": "B19013", "zip": "GEO.id2", "variable":"HD01_VD01"},
              "gini_index": {"table": "B19083", "zip": "GEO.id2", "variable":"HD01_VD01"},
              "health_coverage_population": {"table": "B992701", "zip": "GEO.id2", "variable":"HD01_VD02"},
              "same_house": {"table": "B07012", "zip": "GEO.id2", "variable":"HD01_VD06"},
              "poverty_rate": {"table": "S1701", "zip": "GEO.id2", "variable":"HC02_EST_VC01"}}
unemp_dict = {"unemployment_rate": {"table": "S2301", "zip": "GEO.id2", "variable":"HC04_EST_VC01"},
              "unemployment_rate2": {"table": "DP03", "zip": "GEO.id2", "variable":"HC03_VC07"}}

def read_ACS(year_list, table_dict, unemp_dict):
    '''
    '''
    data_dict = {}
    for year in year_list:
        for t_name, value in table_dict.items():
            if (year == 13) and (t_name == "same_house"):
                pass

            else:
                table_name = t_name + str(year)
                df = pd.read_csv(r"..\data\ACS_final\ACS_" + str(year) + "_" + \
                                 value["table"] + "_" + t_name + ".csv")
                data_dict[table_name] = [df.iloc[1:], value]

        if year <= 14:
            emp_table_name = "unemployment_rate" + str(year)
            df = pd.read_csv(r"..\data\ACS_final\ACS_" + str(year) + "_" + \
                                 unemp_dict["unemployment_rate"]["table"] + "_" + "unemployment_rate" + ".csv")
            data_dict[emp_table_name] = [df.iloc[1:], unemp_dict["unemployment_rate"]]

        else:
            emp_table_name = "unemployment_rate" + str(year)
            df = pd.read_csv(r"..\data\ACS_final\ACS_" + str(year) + "_" + \
                                 unemp_dict["unemployment_rate2"]["table"] + "_" + "unemployment_rate" + ".csv")
            data_dict[emp_table_name] = [df.iloc[1:], unemp_dict["unemployment_rate2"]]

    return data_dict

def ACS_select(df_dict):
    '''
    '''
    new_df_dict = {}
    yearly_data = {}
    for df_name, df_value in df_dict.items():
        variable, year = df_name[:-2], df_name[-2:]
        
        df_v = df_value[1]
        df = df_value[0][[df_v["zip"], df_v["variable"]]]
        new_df_dict[df_name] = {df_v["zip"]:"zipcode", df_v["variable"]:variable}
        df = df.rename(columns=new_df_dict[df_name])

        if year not in yearly_data:
            yearly_data[year] = df
        else:
            yearly_data[year] = pd.merge(df, yearly_data[year], left_on="zipcode", right_on="zipcode")
    
    same_home13 = pd.DataFrame({"zipcode": yearly_data["13"]["zipcode"],"same_house":([np.nan] * yearly_data["13"].shape[0])})
    yearly_data["13"] = pd.merge(yearly_data["13"], same_home13, left_on="zipcode", right_on="zipcode")
        
    return yearly_data

def ACS_integrater(yearly_data):
    '''
    '''
    ordered_column = ["zipcode", "total_population", "median_household_income", "gini_index", 
                                     "health_coverage_population", "same_house", "poverty_rate",
                                     "unemployment_rate", "year"]
    full_df = pd.DataFrame(columns=ordered_column)

    for year, df in yearly_data.items():
        df["year"] = year
        df = df[ordered_column]
        full_df = pd.concat([full_df, df], join="inner")
    
    return full_df

def ACS_do(year_list, table_dict, unemp_dict):
    '''
    '''
    data_dict = read_ACS(year_list, table_dict, unemp_dict)
    yearly_data = ACS_select(data_dict)
    full_df = ACS_integrater(yearly_data)
    return full_df

full_df = ACS_do([12,13,14,15,16,17], table_dict, unemp_dict)
full_df.to_csv(r"..\data\ACS_final\ACS_full.csv")


##################################################################################################################################
# preprocess data before 2011

total_population11 = pd.read_csv(r"..\data\ACS_final\ACS_11_B01003_total_population.csv")
median_household_income11 = pd.read_csv(r"..\data\ACS_final\ACS_11_B19013_median_household_income.csv")
gini_index11 = pd.read_csv(r"..\data\ACS_final\ACS_11_B19083_gini_index.csv")
same_house11 = pd.read_csv(r"..\data\ACS_final\ACS_11_B07012_same_house.csv")
unemployment_rate11 = pd.read_csv(r"..\data\ACS_final\ACS_11_S2301_unemployment_rate.csv")
poverty_rate12 = pd.read_csv(r"..\data\ACS_final\ACS_12_S1701_poverty_rate.csv")
health_coverage_population12 = pd.read_csv(r"..\data\ACS_final\ACS_12_B992701_health_coverage_population.csv")

total_population11 = total_population11[["GEO.id2", "HD01_VD01"]].rename(columns={"GEO.id2":"zip code", "HD01_VD01":"total_population"})
median_household_income11 = median_household_income11[["GEO.id2", "HD01_VD01"]].rename(columns={"GEO.id2":"zip code", "HD01_VD01":"median_household_income"})
gini_index11 = gini_index11[["GEO.id2", "HD01_VD01"]].rename(columns={"GEO.id2":"zip code", "HD01_VD01":"gini_index"})
same_house11 = same_house11[["GEO.id2", "HD01_VD06"]].rename(columns={"GEO.id2":"zip code", "HD01_VD06":"same_house"})
unemployment_rate11 = unemployment_rate11[["GEO.id2", "HC04_EST_VC01"]].rename(columns={"GEO.id2":"zip code", "HC04_EST_VC01":"unemployment_rate"})
poverty_rate12 = poverty_rate12[["GEO.id2", "HC02_EST_VC01"]].rename(columns={"GEO.id2":"zip code","HC02_EST_VC01":"poverty_rate"})
health_coverage_population12 = health_coverage_population12[["GEO.id2","HD01_VD02"]].rename(columns={"GEO.id2":"zip code","HD01_VD02":"health_coverage_population"})

final11 = pd.merge(total_population11, median_household_income11, left_on="zip code", right_on="zip code")
final11 = pd.merge(final11, gini_index11, left_on="zip code", right_on="zip code")
final11 = pd.merge(final11, same_house11, left_on="zip code", right_on="zip code")
final11 = pd.merge(final11, unemployment_rate11, left_on="zip code", right_on="zip code")
final11 = pd.merge(final11, poverty_rate12, left_on="zip code", right_on="zip code")
final11 = pd.merge(final11, health_coverage_population12, left_on="zip code", right_on="zip code")

final_data11 = pd.DataFrame(columns=list(final11.columns) + ["year"])
for year in [2008,2009,2010,2011]:
    final11["year"] = year
    final_data11 = pd.concat([final_data11, final11], join="inner")

final_data11.to_csv(r"..\data\ACS_final\ACS_08-11.csv")


######################################################################################################################################
# Integrate all data

full_data12 = pd.read_csv(r"..\data\ACS_final\ACS_full.csv")
full_data08 = pd.read_csv(r"..\data\ACS_final\ACS_08-11.csv")
sub_dat12 = full_data12[full_data12.year==12][["zipcode", "same_house"]]
sub_dat13 = full_data12[full_data12.year==13].drop(["same_house"], axis=1)
new_13 = pd.merge(sub_dat12, sub_dat13, left_on="zipcode", right_on="zipcode")
full_data12 = full_data12[full_data12.year != 13]
full_data12 = pd.concat([new_13, full_data12], join="inner")
full_data12["year"] = full_data12["year"] + 2000
full_data08 = full_data08.rename(columns={"zip code": "zipcode"})
full_data08 = full_data08.iloc[1:]
full_data = pd.concat([full_data08, full_data12], join="inner")
full_data = full_data.drop(["Unnamed: 0"], axis=1)

full_data.to_csv(r"..\data\ACS_final\ACS_full08-17.csv")

