# -*- coding: utf-8 -*-
"""yellow_taxi_data_june_2020 (1).ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1vhHiXUIMae9XdVYaKuOVoZNPoTjSM98T

We are considering Yellow Taxi data for June

# Data Importing and Data Summarisation
"""

# import important libraries - matplotlib, seaborn and pandas
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

from google.colab import drive
drive.mount('/content/drive')

# yellow taxi data
file_loc1 = '/content/drive/MyDrive/Onelearn/EDA and Visulisation/W8D3/Lessons/yellow_tripdata_2020-06.parquet'
trip_data = pd.read_parquet(file_loc1)

trip_data.to_csv('/content/drive/MyDrive/Onelearn/EDA and Visulisation/W8D3/Lessons/yellow_tripdata_2020-06.csv')

# read file
trip_data = pd.read_csv('/content/drive/MyDrive/Onelearn/EDA and Visulisation/W8D3/Lessons/yellow_tripdata_2020-06.csv')
trip_data.head()

trip_data.shape

trip_data.info()

"""# Data Cleaning and Manipulation Steps"""

trip_data.drop(['Unnamed: 0','VendorID','RatecodeID','store_and_fwd_flag','airport_fee','congestion_surcharge',],axis = 1, inplace =True)

trip_data['tpep_pickup_datetime'] = pd.to_datetime(trip_data['tpep_pickup_datetime'])
trip_data['tpep_dropoff_datetime'] = pd.to_datetime(trip_data['tpep_dropoff_datetime'])

trip_data.info()

trip_data.dropna(inplace = True)

trip_data['passenger_count'] = trip_data['passenger_count'].astype(int)

# create 'duration' column using pd.Timedelta(minutes=1)
trip_data['duration'] = (trip_data['tpep_dropoff_datetime'] - trip_data['tpep_pickup_datetime'])/ pd.Timedelta(minutes=1)
# create 'trip_pickup_hour' column using 'tpep_pickup_datetime' column
trip_data['trip_pickup_hour'] = trip_data['tpep_pickup_datetime'].dt.hour
# create 'trip_dropoff_hour' column using 'tpep_dropoff_datetime' column
trip_data['trip_dropoff_hour'] = trip_data['tpep_dropoff_datetime'].dt.hour
# create 'trip_day' column using 'tpep_pickup_datetime' column - use day_name()
trip_data['trip_day'] = trip_data['tpep_pickup_datetime'].dt.day_name()
# print data info
print(trip_data.info())
# print data head
trip_data.head()

"""Now our Total_amount is basically Total_amount = fare_amount + tolls_amount + tip_amount + (extra + mta_tax + improvement_surcharge)

of the above components of total_amount we will specifically focus on 'fare_amount','tip_amount', 'tolls_amount' and 'total taxes'
"""

# create 'total_taxes' column from summing 'extra','mta_tax', 'improvement_surcharge'
trip_data['total_taxes'] = trip_data['extra']+trip_data['mta_tax']+trip_data['improvement_surcharge']
# drop 'extra','mta_tax','improvement_surcharge' columns
trip_data.drop(['extra','mta_tax','improvement_surcharge'],axis=1,inplace=True)
# print data head
trip_data.head()

"""For payment_type we have the following mapping for categories: 1= Credit card 2= Cash 3= No charge 4= Dispute 5= Unknown 6= Voided trip

let's just check if we have only these categories available in payment_type or not
"""

# value_counts for 'payment_type' column
trip_data['payment_type'].value_counts()

# function for mapping numerical payment_type to actual payment
def map_payment_type(x):
    if x==1:
        return 'Credit_card'
    elif x==2:
        return 'Cash'
    elif x==3:
        return 'No_charge'
    elif x==4:
        return 'Dispute'
    elif x==5:
        return 'Unknown'
    else:
        return 'Voided_trip'

# use .apply and lambda on payment_type column to change 'payment_type' column
trip_data['payment_type'] = trip_data.payment_type.apply(lambda x:map_payment_type(x))
# print data head
trip_data.head()

trip_data.to_csv('/content/drive/MyDrive/Onelearn/EDA and Visulisation/W8D3/Lessons/yellow_taxi_data_2020-06_cleaned.csv',index=False)

"""# Data Analysis and Visualisation"""

trip_data

"""# CONTINUOUS VARIABLE DISTRIBUTION(Univariate Analysis)"""

# continuous_columns list
continuous_columns = ['fare_amount','tip_amount','total_taxes','total_amount','duration','trip_distance','tolls_amount']

trip_data[continuous_columns].head()

# use .describe() for showing the statistics for continuous columns
trip_data[continuous_columns].describe()

"""Since we are trying to understand the distribution of continuous numerical variables, we will be using

histograms box plots Below we have used a for loop to loop through all the continuous variables and then draw histograms and box plots for each of them at each iteration
"""

# for loop for continuous_columns variable
for feature in continuous_columns:
    fig,ax = plt.subplots(1,2,figsize=(12,6))
    ax[0].hist(trip_data[feature])
    ax[0].set_title('histogram of column values in '+feature)
    sns.boxplot(trip_data[feature],ax=ax[1])
    # using ax2.set_title for box plot
    ax[1].set_title('box plot of column values in '+feature)
    # seaborn style setting
    sns.set()
    # matplotlib command for displaying plots
    plt.show()

"""Negtive values for columns does not make sense fare_amount tip_amount total_taxes tolls_amount total_amount duration

Let's just observe how the negative values in each of these columns look like
"""

# using .loc to show negative values in fare_amount  # 8 mil rows
trip_data.loc[trip_data['fare_amount']<0]

# using .loc to show negative values in tip_amount
trip_data.loc[trip_data['tip_amount']<0]

# using .loc to show negative values in tolls_amount
trip_data.loc[trip_data['tolls_amount']<0]

# using .loc to show negative values in total_taxes
trip_data.loc[trip_data['total_taxes']<0]

# using .loc to show negative values in total_amount
trip_data.loc[trip_data['total_amount']<0]

# data shape before filtering negative fare_amount rows
print(trip_data.shape)
# using .loc to filter only those rows where fare_amount is positive 
trip_data = trip_data.loc[trip_data['fare_amount']>=0]
# print data shape
print(trip_data.shape)
# print data.head()
trip_data.head()

print(trip_data.loc[trip_data['tip_amount']<0].shape)
print(trip_data.loc[trip_data['total_taxes']<0].shape)
print(trip_data.loc[trip_data['tolls_amount']<0].shape)

# using .loc to show negative values in duration
trip_data.loc[trip_data['duration']<0]

# using .loc to filter only those rows where duration is positive 
trip_data = trip_data.loc[trip_data['duration']>=0]
print(trip_data.shape)

"""Now we will again look at the distribution plots for these variables"""

# for loop for continuous_columns variable
for feature in continuous_columns:
    fig,ax = plt.subplots(1,2,figsize=(12,6))
    ax[0].hist(trip_data[feature])
    ax[0].set_title('histogram of column values in '+feature)
    sns.boxplot(trip_data[feature],ax=ax[1])
    # using ax2.set_title for box plot
    ax[1].set_title('box plot of column values in '+feature)
    # seaborn style setting
    sns.set()
    # matplotlib command for displaying plots
    plt.show()

# use .describe() again to show the statistics for these continuous variables
trip_data[continuous_columns].describe()

# for loop for continuous_columns variable
for feature in continuous_columns:
    # removing the outliers
    feature_data_percentile = trip_data[feature].quantile(0.95)
    feature_data = trip_data.loc[trip_data[feature]<feature_data_percentile,feature]
    fig,ax = plt.subplots(1,2,figsize=(12,6))
    ax[0].hist(feature_data)
    ax[0].set_title('histogram of column values in '+feature)
    sns.boxplot(feature_data,ax=ax[1])
    # using ax2.set_title for box plot
    ax[1].set_title('box plot of column values in '+feature)
    # seaborn style setting
    sns.set()
    # matplotlib command for displaying plots
    plt.show()

"""Looking from the above histograms and box plots we can decipher following information for each column

fare_amount - most of the fare amount is within 8.5 dollar value as is shown by the median value. Though there are some significant outliers, the maximum of which is beyond 940 dollars.

tip_amount - most of the tip amount is within 1.5 dollar as is shown by the median value. Though again here too we have outliers, the maximum of which is around 400 dollars.

tolls_amount - most of the tolls_amount value is 0 so it seems most of the trips do not have to pay for tolls.

total_taxes - most of the total_taxes values is within 1.3 dollars as is shown by the median value. There is very less outliers.

total_amount - most of the total_amount values is within 14 dollars as is shown by the median value. Again the outliers in this case seems mostly because of outliers in fare_amount.some Heavy outlier exist of 1100 dollar

duration - most of the values in duration is within 8.86 minutes range as is shown by the median value. We do have some outliers which are beyond the range of 4000 minutes.

trip_distance - most of the trip_distance is within 1.7 miles value as is shown by the median. only a heavy outliers exit of around 22k miles.

**categorical_variables**
"""

# list of categorical_variables
categorical_variables = ['payment_type','trip_pickup_hour','trip_dropoff_hour','trip_day','PULocationID','DOLocationID']

# start exploration with payment_type using .value_counts()
trip_data['payment_type'].value_counts()

# but this is a series for ease of plotting we need to use dataframe using .reset_index() on value_counts()
payment_type_category_count = trip_data['payment_type'].value_counts().reset_index()
# print the above dataframe
payment_type_category_count

# we are shown the count under each category but it is better to have count% for comparison - create count_percent col
payment_type_category_count['count_percent'] = (payment_type_category_count['payment_type']/trip_data.shape[0])*100
# print the data frame
payment_type_category_count

# now let's plot it as bar chart
# first step - create fig, ax object using plt.subplots
fig,ax = plt.subplots(figsize=(7,7))
# second step - use sns.barplot(x, y , data, ax) for plotting bar plot
sns.barplot(x = 'index', y = 'count_percent', data=payment_type_category_count,ax=ax)
# third step - use ax object to change plot properties - here we set a title with ax.set_title()
ax.set_title('box plot for payment_type column')
# third step - seaborn style setting
sns.set()
# fourth step - use plt.show() for showing the plots
plt.show()

"""From above we can understand that most of the payments are done through cash and credit cards. The proportion of credit card payments is around 70%.

Now we look into time based categorical variables.

'trip_pickup_hour' 'trip_dropoff_hour' 'trip_day'
"""

# now let's plot all the time based categorical variables in this way using a for loop
for feature in ['trip_pickup_hour','trip_dropoff_hour','trip_day']:
    # Create a dataframe for the feature using value_counts().reset_index()
    feature_value_counts = trip_data[feature].value_counts().reset_index()
    # create count_percent column 
    feature_value_counts['count_percent'] = (feature_value_counts[feature]/trip_data.shape[0])*100
    # print the number of categories in the feature
    print('Number of categories in feature '+ feature + ' is ' + str(feature_value_counts.shape[0]))
    # Create fig,ax object using plt.subplots 
    if feature_value_counts.shape[0]<10:
        fig,ax = plt.subplots(figsize=(7,7))
    else:
        fig,ax = plt.subplots(figsize=(20,7))
    # plot barplot x='index' and y='count_percent' using sns.barplot
    sns.barplot(x='index',y='count_percent',data=feature_value_counts,ax=ax)
    # set_title
    ax.set_title('Bar plot for '+ feature)
    # set_xlabel
    ax.set_xlabel(feature)
    sns.set()
    plt.show()

"""Based on above plots we can observe following things

Trip Hour 1) The dropoff and pick up hour distribution looks almost same, it is because the trip duration in most of the cases is less than an hour with the median duration value within 9 min.

2) Peak hour for the pick up and drop off is around evening from 13 to 16. The busiest time is 15 PM.

3) There is less traffic during night times and only after 8AM in morning does the pickup and drop off starts picking up pace.

Trip day

1)Sunday has the lowest taxi uses while Tuesday is the busiest.

2)Weekdays have heavy taxi uses compared to the weekands

Moving on we will explore the distribution of location based features:

'PULocationID'

'DOLocationID'
"""

# let's see the number of categories available in both pickup and dropoff location - PULocationID and DOLocationID
print(trip_data['PULocationID'].value_counts().shape)
print(trip_data['DOLocationID'].value_counts().shape)

for feature in ['PULocationID','DOLocationID']:
    # Create a dataframe for the feature using value_counts().reset_index()
    feature_value_counts = trip_data[feature].value_counts().reset_index()
    # create count_percent column 
    feature_value_counts['count_percent'] = (feature_value_counts[feature]/trip_data.shape[0])*100
    # print the number of categories in the feature
    print('Number of categories in feature '+ feature + ' is ' + str(feature_value_counts.shape[0]))
    # Create fig,ax object using plt.subplots 
    fig,ax = plt.subplots(figsize=(25,7))
    # plot barplot x='index' and y='count_percent' using sns.barplot
    sns.barplot(x='index',y='count_percent',data=feature_value_counts,ax=ax)
    # set_title
    ax.set_title('Bar plot for '+ feature)
    # set_xlabel
    ax.set_xlabel(feature)
    sns.set()
    plt.show()

"""The above plots looks quite messy but one insight that we can indetify from above plot that most of pickup and dropoff points do not have more 0.5% traffic (0.5 percent of 8755612 total trips is 43778).

So in our next plot we will filter out these pickup and dropoff points to look into the graph more clearly.
"""

for feature in ['PULocationID','DOLocationID']:
    feature_value_counts = trip_data[feature].value_counts().reset_index()
    feature_value_counts['count_percent'] = (feature_value_counts[feature]/trip_data.shape[0])*100
    # filter only those location which has more than 0.5 % of traffic
    feature_value_counts = feature_value_counts.loc[feature_value_counts['count_percent']>=0.5]
    print('Number of categories in feature '+ feature + ' above 0.5 % count is ' + str(feature_value_counts.shape[0]))
    fig,ax = plt.subplots(figsize=(25,7))
    sns.barplot(x='index',y='count_percent',data=feature_value_counts,ax=ax)
    ax.set_title('Bar plot for '+ feature)
    ax.set_xlabel(feature)
    sns.set()
    plt.show()

"""From the above plots we can glance following insights

The busiest location in terms of pickup are 236 and 237

The busiest location for dropoff too are 236 , 237 and 79 busiest locations but 236 is far more busiest than the other two in drop_off hour. 

For exploring busy routes we need to create a new route column which is a combination of pickup and dropoff point.

So route = 'PULocationID'-'DULocationID'
"""

# create routes column using PULocationID and DOLocationID with lambda function
trip_data['routes'] = trip_data.apply(lambda x: str(x['PULocationID'])+'-'+str(x['DOLocationID']),axis=1)

trip_data['routes'].head()

# plot bar plot for routes which have trip count above 0.25%
feature = 'routes'
feature_value_counts = trip_data[feature].value_counts().reset_index()
feature_value_counts['count_percent'] = (feature_value_counts[feature]/trip_data.shape[0])*100
# choosing routes where the trip percent is above 0.25% of total trips
feature_value_counts = feature_value_counts.loc[feature_value_counts['count_percent']>=0.25]
print('Number of categories in feature '+ feature + ' above 0.25 % count is ' + str(feature_value_counts.shape[0]))
fig,ax = plt.subplots(figsize=(25,7))
sns.barplot(x='index',y='count_percent',data=feature_value_counts,ax=ax)
ax.set_title('Bar plot for '+ feature)
ax.set_xlabel(feature)
sns.set()
plt.show()

"""From the above plot we can observe that 5 busiest route are following:

264-264

237-236

236-237

236-236
"""

# look into value_counts of 'passenger_count'
trip_data['passenger_count'].value_counts()

"""Here we see that the mostly 1 or 2 passengers avail the cab. The instance of large group of people travelling together is rare

# Bivariate Analysis

PRICING VARIABLE EXPLORATION WITH HOUR/DAY OF TRIP *

All of our pricing variables are continuous and Hour/Day is categorical.

The way to explore relationship between a continuous variable and categorical variable is through a box plot. We create box plot for each category of categorical variable.

so as to see how the distribution changes for the continuous variables as the category values changes for categorical variable.

We will start with fare_amount exploration.
"""

# fig,ax object using plt.subplots()
fig,ax = plt.subplots(figsize=(25,7))
# box plot using - sns.boxplot(x, y , data, ax)
sns.boxplot(x = 'trip_pickup_hour',y='fare_amount',data=trip_data,ax=ax)
# ax.set_title
ax.set_title('box plot of fare_amount wrt hour of the day')
# seaborn style setting
sns.set()
# matplotlib plt.show()
plt.show()

# fig,ax object using plt.subplots()
fig,ax = plt.subplots(figsize=(25,7))
# box plot using - sns.boxplot(x, y , data, ax)
sns.boxplot(x = 'trip_dropoff_hour',y='fare_amount',data=trip_data,ax=ax)
# ax.set_title
ax.set_title('box plot of fare_amount wrt hour of the day')
# seaborn style setting
sns.set()
# matplotlib plt.show()
plt.show()

"""From the above plot we can observe that most of the outliers in fare_amount happens during 10AM to 7PM based on pickup time.

From the above plot trip_dropoff_hour outliers happens during 14 or 2PM to 20 or 8PM based on pickup time.

Outliers is less in the late nights and early morning.

For observing the distribution in a better way we would restrict the fare_amount to below 50 dollars.
"""

# restricted_fare_amount_data dataframe formation by filtering fare_amount less than 50 dollars
restricted_fare_amount_data = trip_data.loc[(trip_data['fare_amount']<=50) & (trip_data['fare_amount']>=0)]
restricted_fare_amount_data.shape

fig,ax = plt.subplots(figsize=(25,7))
sns.boxplot(x = 'trip_pickup_hour',y='fare_amount',data=restricted_fare_amount_data,ax=ax)
ax.set_title('box plot of fare_amount wrt hour of the day')
sns.set()
plt.show()

fig,ax = plt.subplots(figsize=(25,7))
sns.boxplot(x = 'trip_dropoff_hour',y='fare_amount',data=restricted_fare_amount_data,ax=ax)
ax.set_title('box plot of fare_amount wrt hour of the day')
sns.set()
plt.show()

"""We can obseve from the above graph the fare_amount in late nigth is comparitively higher than the rest of the hours(same pattern seen in both the cases).

Also the median fare_amount between 5 - 6 is less than all others hours of the day(seen in bothe cases)

let's us see if hour of day has any effect on other pricing related variables or not.

Starting with total_amount
"""

fig,ax = plt.subplots(figsize=(25,7))
# sns.boxplot changes
sns.boxplot(x = 'trip_pickup_hour',y='total_amount',data=trip_data,ax=ax)
ax.set_title('box plot of total_amount wrt hour of the day')
sns.set()
plt.show()

fig,ax = plt.subplots(figsize=(25,7))
# sns.boxplot changes
sns.boxplot(x = 'trip_dropoff_hour',y='total_amount',data=trip_data,ax=ax)
ax.set_title('box plot of total_amount wrt hour of the day')
sns.set()
plt.show()

# restricted_total_amount_data for filtering total_amount data to less than 50 dollars
restricted_total_amount_data = trip_data.loc[trip_data['total_amount']<=50]
restricted_total_amount_data.shape

fig,ax = plt.subplots(figsize=(25,7))
sns.boxplot(x = 'trip_pickup_hour',y='total_amount',data=restricted_total_amount_data,ax=ax)
ax.set_title('box plot of total_amount wrt hour of the day')
sns.set()
plt.show()

fig,ax = plt.subplots(figsize=(25,7))
sns.boxplot(x = 'trip_dropoff_hour',y='total_amount',data=restricted_total_amount_data,ax=ax)
ax.set_title('box plot of total_amount wrt hour of the day')
sns.set()
plt.show()

"""the pattern of total_amount is same as the pattern we seen in the fare_amount"""

restricted_tip_amount_data = trip_data.loc[trip_data['tip_amount']<10]
restricted_total_taxes_data = trip_data.loc[trip_data['total_taxes']<10]

fig,ax = plt.subplots(figsize=(25,7))
sns.boxplot(x = 'trip_pickup_hour',y='tip_amount',data=restricted_tip_amount_data,ax=ax)
ax.set_title('box plot of tip_amount wrt hour of the day')
sns.set()
plt.show()

fig,ax = plt.subplots(figsize=(25,7))
sns.boxplot(x = 'trip_dropoff_hour',y='tip_amount',data=restricted_tip_amount_data,ax=ax)
ax.set_title('box plot of tip_amount wrt hour of the day')
sns.set()
plt.show()

"""The median of tip_amount in early morning is mostly zero but IQR is high that means the some of the tip amounts are higher end).

And in between 11 -14 the tip_amount is minimum and almost constant, whereas tip amount is on higher side in evenings.

(Same pattern seen in both the trip_pickup and trip_drop_off)


"""

# total_taxes = extra + improvement_surcharges + Mta

fig,ax = plt.subplots(figsize=(25,7))
sns.boxplot(x = 'trip_pickup_hour',y='total_taxes',data=restricted_total_taxes_data,ax=ax)
ax.set_title('box plot of total_taxes wrt hour of the day')
sns.set()
plt.show()

fig,ax = plt.subplots(figsize=(25,7))
sns.boxplot(x = 'trip_dropoff_hour',y='total_taxes',data=restricted_total_taxes_data,ax=ax)
ax.set_title('box plot of total_taxes wrt hour of the day')
sns.set()
plt.show()

"""The taxs imposed from 16 to 19 is much higher as compared to the other hours beacue traffic surcharge.

The taxes in the period between 6 to 15 is much lower than the other pick_up hours
"""

# plot of trip_day with fare_amount
fig,ax = plt.subplots(figsize=(7,7))
# changes in sns.boxplot x and y
sns.boxplot(x = 'trip_day',y='fare_amount',data=restricted_fare_amount_data,ax=ax)
ax.set_title('box plot of fare_amount wrt the day of the week')
sns.set()
plt.show()

fig,ax = plt.subplots(figsize=(7,7))
sns.boxplot(x = 'trip_day',y='total_amount',data=restricted_total_amount_data,ax=ax)
ax.set_title('box plot of total_amount wrt the day of the week')
sns.set()
plt.show()

fig,ax = plt.subplots(figsize=(7,7))
sns.boxplot(x = 'trip_day',y='tip_amount',data=restricted_tip_amount_data,ax=ax)
ax.set_title('box plot of tip_amount wrt the day of the week')
sns.set()
plt.show()

fig,ax = plt.subplots(figsize=(7,7))
sns.boxplot(x = 'trip_day',y='total_taxes',data=restricted_total_taxes_data,ax=ax)
ax.set_title('box plot of total_taxes wrt the day of the week')
sns.set()
plt.show()

"""We can see that pricing overall does not change much with respect to day of week.but total taxes are higher in weekdays compared to weekands"""

# create a new series using value_counts() on 'PULocationID'
pickup_location_value_counts = trip_data['PULocationID'].value_counts()
# show the series
pickup_location_value_counts.head()

# top 10 frequent pickup locations using .nlargest(10).index
top_10_frequent_pickup_locations = pickup_location_value_counts.nlargest(10).index
top_10_frequent_pickup_locations

# for loop for plotting box plot of each of the top 10 frequent pickup locations
for top_pickup_locID in top_10_frequent_pickup_locations:
    # create the new dataframe for each location using .loc on 'PULocationID' - pickup_locID_dataframe
    pickup_locID_dataframe = trip_data.loc[trip_data['PULocationID'] == top_pickup_locID]
    # print the median fare_amount for the top_pickup_locID
    print('The median fare_amount of trips taken from '+str(top_pickup_locID)+' is '+str(pickup_locID_dataframe['fare_amount'].median()))
    # fig,ax object
    fig,ax = plt.subplots(figsize=(6,6))
    # sns.boxplot of fare_amount from the dataframe pickup_locID_dataframe
    sns.boxplot(pickup_locID_dataframe['fare_amount'],ax=ax)
    # set_title
    ax.set_title('box plot of fare_amount for pickup location '+ str(top_pickup_locID))
    sns.set()
    plt.show()

"""So from above plot we can observe that for one of the most busiest pickup location i.e 236 has median fare_amount is low in comparison to other busiset location.

It is also observe that the median fare_amount is highest for the location ID 140 which is about 9.5 dollars

This could be helpful in adjusting our revenue expectation based on putting our cabs in a given location because just choosing busy pickup locations for higher revenue won't work, we may have to choose locations taking into consideration both busy traffic and higher median fare_amount.

# DURATION EXPLORATION
"""

# plot box plot for duration for different hours of day
fig,ax = plt.subplots(figsize=(20,7))
# box plot using sns.boxplot x is 'trip_pickup_hour' and y is 'duration'
sns.boxplot(x = 'trip_pickup_hour', y='duration',data = trip_data,ax=ax)
ax.set_title('Box plot of trip_pickup hour with respect to trip duration')
sns.set()
plt.show()

# create restricted_duration dataframe with .loc on 'duration' column
restricted_duration= trip_data.loc[trip_data['duration']<50]
restricted_duration.shape

fig,ax = plt.subplots(figsize=(20,7))
sns.boxplot(x = 'trip_pickup_hour', y='duration',data = restricted_duration,ax=ax)
ax.set_title('Box plot of trip_pickup hour with respect to trip duration')
sns.set()
plt.show()

"""The duration of trip is higher in the early morning and late nights whereas in pickup_hour 5-7 AM the duration of trip is lowest."""

# plot box plots of duration for top 10 frequent pickup locations
for top_pickup_locID in top_10_frequent_pickup_locations:
    # create the new dataframe for each location using .loc on 'PULocationID' - pickup_locID_dataframe
    pickup_locID_dataframe = trip_data.loc[trip_data['PULocationID'] == top_pickup_locID]
    # print the median duration for the top_pickup_locID
    print('The median trip duration of trips taken from '+str(top_pickup_locID)+' is '+str(pickup_locID_dataframe['duration'].median()))
    fig,ax = plt.subplots(figsize=(6,6))
    # sns.boxplot of duration from the dataframe pickup_locID_dataframe
    sns.boxplot(pickup_locID_dataframe['duration'],ax=ax)
    # set_title
    ax.set_title('box plot of duration for pickup location '+ str(top_pickup_locID))
    sns.set()
    plt.show()

"""As seen from the above plot the busiset location not has the longest duration of trip, but the other busiset location that is 140 has higher duration (thats why that location has higher fare_amount too)

# Analyse routes

We could analyse routes with fare_amount or total_taxes and duration for different time of the day.
"""

# counting the routes of the trip_data
trip_route_value_counts = trip_data['routes'].value_counts()

trip_route_value_counts.head(10)

# 10 busiest routes in trip_data
trip_route_top_10 = trip_route_value_counts.nlargest(10).index

trip_route_top_10

for trip_route in trip_route_top_10:
    # creating new data frame with trip_route.
    trip_route_df = trip_data.loc[trip_data['routes'] == trip_route]
    #print median fare_amount for the respective route
    print("the fare amount for the route " + trip_route +' '+ 'is ' + str(trip_route_df['fare_amount'].median()))
    #plotting boxplot 
    fig,ax = plt.subplots(figsize=(6,6))
    # sns.boxplot of duration from the dataframe pickup_locID_dataframe
    sns.boxplot(trip_route_df['fare_amount'],ax=ax)
    # set_title
    ax.set_title('box plot of fare_amount for trip_route '+ str(trip_route ))
    sns.set()
    plt.show()

"""From above plot it is clear that the busiset route does not assure you about the highest revenue. as seen from the graph fare amount for the buisest trip_rout 237-236 is lower than the other Busiset trip_routes.



the trip_route 264-264 has the highest fare_amount of 8.5 median.Its worthnoting that these route should be kept in mind for business prospect.
"""



for trip_route in trip_route_top_10:
    # creating new data frame with trip_route.
    trip_route_df = trip_data.loc[trip_data['routes'] == trip_route]
    #print median total_taxes for the respective route
    print("the fare amount for the route " + trip_route +' '+ 'is ' + str(trip_route_df['total_taxes'].median()))
    #plotting boxplot 
    fig,ax = plt.subplots(figsize=(6,6))
    # sns.boxplot of duration from the dataframe pickup_locID_dataframe
    sns.boxplot(trip_route_df['total_taxes'],ax=ax)
    # set_title
    ax.set_title('box plot of total_taxes for trip_route '+ str(trip_route ))
    sns.set()
    plt.show()

"""From the above plot it is clearly vissible almost all routes has same total_tax of 1.3 and 1.8 dollars, but the trip_route 264-264 and 75-74 lowest total_tax i.e 0.8 dollars as well.

As we seen from fare_amount plot of routes, the 264-264 route has higher fare amount as compared to other routes but it could be higher because of lower taxes applied on the these route as shown in above plot. as it has lowest total_tax value of 0.8 dollars
"""



for trip_route in trip_route_top_10:
    # creating new data frame with trip_route.
    trip_route_df = trip_data.loc[trip_data['routes'] == trip_route]
    #print median total_taxes for the respective route
    print("the duration for the route " + trip_route +' '+ 'is ' + str(trip_route_df['duration'].median()))
    #plotting boxplot 
    fig,ax = plt.subplots(figsize=(6,6))
    # sns.boxplot of duration from the dataframe  trip_route_df 
    sns.boxplot(trip_route_df['duration'],ax=ax)
    # set_title
    ax.set_title('box plot of duration for trip_route '+ trip_route)
    sns.set()
    plt.show()

"""As seen from the above plot that the busisest location 264-264 has 6.96,  highest duration as compared other busisest location.

# FINAL RESULTS FROM EDA

fare_amount - most of the fare amount is within 8.5 dollar 
value as is shown by the median value. Though there are some significant outliers, the maximum of which is beyond 940 dollars.

tip_amount - most of the tip amount is within 1.5 dollar as is shown by the median value. Though again here too we have outliers, the maximum of which is around 400 dollars.

tolls_amount - most of the tolls_amount value is 0 so it seems most of the trips do not have to pay for tolls.

total_taxes - most of the total_taxes values is within 1.3 dollars as is shown by the median value. There is very less outliers.

total_amount - most of the total_amount values is within 14 dollars as is shown by the median value. Again the outliers in this case seems mostly because of outliers in fare_amount.some Heavy outlier exist of 1100 dollar

duration - most of the values in duration is within 8.86 minutes range as is shown by the median value. We do have some outliers which are beyond the range of 4000 minutes.

trip_distance - most of the trip_distance is within 1.7 miles value as is shown by the median. only a heavy outliers exit of around 22k miles.

most of the payments are done through cash and credit cards. The proportion of credit card payments is around 70%.

Trip Hour 

1) The dropoff and pick up hour distribution looks almost same, it is because the trip duration in most of the cases is less than an hour with the median duration value within 9 min.

2) Peak hour for the pick up and drop off is around evening from 13 to 16. The busiest time is 15 PM.

3) There is less traffic during night times and only after 8AM in morning does the pickup and drop off starts picking up pace.

Trip day

1)Sunday has the lowest taxi uses while Tuesday is the busiest.

2)Weekdays have heavy taxi uses compared to the weekands

location_ID-The busiest location in terms of pickup are 236 and 237

The busiest location for dropoff too are 236 , 237 and 79 busiest locations but 236 is far more busiest than the other two in drop_off hour.

The mostly 1 or 2 passengers avail the cab. The instance of large group of people travelling together is rare.


The fare_amount in late nigth is comparitively higher than the rest of the hours(same pattern seen in both the cases).

Also the median fare_amount between 5 - 6 is less than all others hours of the day(seen in bothe cases)

The median of tip_amount in early morning is mostly zero.And in between 11 -14 the tip_amount is minimum and almost constant, whereas tip amount is on higher side in evenings.

The taxs imposed from 16 to 19 is much higher as compared to the other hours beacue traffic surcharge.

The taxes in the period between 6 to 15 is much lower than the other pick_up hours

Pricing overall does not change much with respect to day of week.But total taxes are higher in weekdays compared to weekands

For one of the most busiest pickup location i.e 236 has median fare_amount is low in comparison to other busiset location.

It is also observe that the median fare_amount is highest for the location ID 140 which is about 9.5 dollars

This could be helpful in adjusting our revenue expectation based on putting our cabs in a given location because just choosing busy pickup locations for higher revenue won't work, we may have to choose locations taking into consideration both busy traffic and higher median fare_amount.

The duration of trip is higher in the early morning and late nights whereas in pickup_hour 5-7 AM the duration of trip is lowest.

The busiset location not has the longest duration of trip, but the other busiset location that is 140 has higher duration (thats why that location has higher fare_amount too)

The busiset route does not assure you about the highest revenue. as seen from the graph fare amount for the buisest trip_rout 237-236 is lower than the other Busiset trip_routes.

The trip_route 264-264 has the highest fare_amount of 8.5 median.Its worthnoting that these route should be kept in mind for business prospect.

Almost all routes has same total_tax of 1.3 and 1.8 dollars, but the trip_route 264-264 and 75-74 lowest total_tax i.e 0.8 dollars as well.

As we seen from fare_amount plot of routes, the 264-264 route has higher fare amount as compared to other routes but it could be higher because of lower taxes applied on the these route as shown in above plot. as it has lowest total_tax value of 0.8 dollars

The busisest location 264-264 has 6.96, highest duration as compared other busisest location.
"""



