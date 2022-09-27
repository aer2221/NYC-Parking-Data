

import pandas as pd
df=pd.read_csv('Parking.csv', dtype={'Plate':str,'Issue Date':str,'Amount Due':float})
tickets=df[['Plate','Issue Date','Amount Due']]
tickets.head()


def amount_owed(tickets, plate):
    #initialize both number of violations and amount due to 0 
    violations=0
    amount_due = 0
    
    #for loop that runs through dataframe given in function call
    #if the dataframe at "Plate" column matches plate given in function call, increase violations by 1, grab the
    #current amount, and add it to amount due across the entire loop 
    for row in range(len(df)):
        if (df.at[row,'Plate'] == plate):
            violations = violations+1
            curr_amount = float(df.at[row,"Amount Due"])
            amount_due=amount_due+curr_amount
            
    
    return violations,amount_due


amount_owed(tickets,"015THD")




#creates new dataframe from original dataframe
#removes "Issue Date" column and all "BLANKPLATE" license plate entries 
new_df=tickets[['Plate','Amount Due']]
new_df.drop(new_df.index[new_df['Plate']== 'BLANKPLATE'], inplace=True)
new_df.head()


#function uses built-in functions to group plates, sum the amount due of each plate, then return the max and its index
def most_owed(tickets):
    plate_amount=tickets.groupby(by=["Plate"]).sum()
    max_amount=plate_amount.max()
    max_plate=plate_amount.idxmax()
    return (max_plate,max_amount)


most_owed(new_df)



def list_egypt_plates(df):
    list=[]
    for index in range(len(tickets)):
        if (str(tickets.at[index,'Plate'])[0:3])=="DTH" or (str(tickets.at[index,'Plate'])[-3:])=="THD":
            list.append(True)
        else:
            list.append(False)

    return list

#assigns the list of booleans created by the function to variable value_list
value_list=list_egypt_plates(tickets)

#uses value_list to filter original dataframe of all license plates into dataframe with only Egyptian license plates 
egypt_plates=tickets[value_list]

#checking that the dataframe is correct (only Egyptian plates)
egypt_plates.head()


# ### How much money diplomatic cars from Egypt owe in total 

#takes only the "Amount Due" column from egypt_plates and assigns it to variable total_egypt_owes
total_egypt_owes=egypt_plates["Amount Due"]

#sums up all values in the "Amount Due" column 
total_egypt_owes.sum()      


# ### Which particular car from Egypt owes the most and how much it owes 

#groups egypt_plates by "Plate," sums the values of each plate, then prints the worst offender's amount and plate
worst_offender=egypt_plates.groupby(by=["Plate"]).sum()
print(worst_offender.max(),worst_offender.idxmax())


# ### In which year between 1995-2019 Egypt owed the most money and how much was it

#changes the data in the "Issue Date" column of egypt_plates to datetime format 
datetime_df=egypt_plates["Issue Date"]
datetime_df = pd.to_datetime(egypt_plates["Issue Date"], format='%m/%d/%Y')

#changes egypt_plates "Issue Date" column to include only datetime objects
egypt_plates['Issue Date']=datetime_df.dt.year


#creates variable "correct_years" consisting of boolean values and uses this variable to filter egypt_plates
correct_years= (egypt_plates["Issue Date"] > 1994) & (egypt_plates["Issue Date"] < 2020)
correct_years.head()
egypt_correct_years=egypt_plates[correct_years]


#utilizes dataframe with only the desired years
#groups by year, prints the year with the max amount due and the amount due in that year
worst_year=egypt_correct_years.groupby(by=(["Issue Date"])).sum()
print(worst_year.max(),worst_year.idxmax())


# * Total amount Egypt owes: 44828.77
# * License plate number of worst offender: 118THD
# * Amount owed by worst offender: 17850.0
# * Worst year for parking tickets from Egyption diplomats: 2000, $9925.0 dollars due that year 
