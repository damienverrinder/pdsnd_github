import time
import pandas as pd
import numpy as np
import calendar as calendar
import datetime

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

timefilter = ""

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    city = ""
    filterselection = ""
    month = ""
    day = ""

    # Function to always take the users input and handle any case sensitivity - annoying in applications
    def fixinputcase(inputstring):
        outputstring = inputstring.lower().capitalize()
        return outputstring
    print('')
    print('-'*40)
    print('\nHello! Let\'s explore some US bikeshare data!')

    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("\nWould you like to see data for Chicago, New York City or Washington?\n")
        if city.lower() in CITY_DATA:
            break
        else:
            print("\nOops, we don't have any data for {}!".format(city))

    # Function to request the Month filter
    def askformonthfilter():
        while True:
            month = input("\nWhich month? January, February, March, April, May or June?\n")
            month = fixinputcase(month)
            if month in ['January', 'February', 'March', 'April', 'May', 'June']:
                return month
                break
            else:
                print("\nOops, we don't have data for {}".format(month))

    def askfordayfilter():
        while True:
            day = input("\nWhich day of the week? Monday, Tuesday, Wednesday etc.\n")
            day = fixinputcase(day)

            if day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']:
                return day
                break
            else:
                print("\nOops, we don't have data for {}".format(day))

    # Ask for Time Filters for the Data to be analysed
    while True:
        filterselection = input("\nWould you like to filter the data by month, day, both or none?\n")
        filterselection = fixinputcase(filterselection)

        if filterselection in ['Month', 'Day', 'Both', 'None']:
            global timefilter
            timefilter = filterselection
            if filterselection == "Month":
                month = askformonthfilter()
                day = "All"
                break
            if filterselection == 'Day':
                month = "All"
                day = askfordayfilter()
                break
            if filterselection == 'Both':
                month = askformonthfilter()
                day = askfordayfilter()
                break
            if filterselection == "None":
                month = "All"
                day = "All"
                break
        else:
            print("Oops, that doesn't look right - please enter month, day, both or none.")

    print('')
    print('-'*40)
    print("\nSelected City = {}, Month = {}, Day = {}".format(city,month,day))

    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # Notify the user that we are loading data
    print ("\nLoading Data - please wait...\n")

    # based on the city requested, load the appropriate CSV file based on the CITY_DATA file list
    citydf = pd.read_csv(CITY_DATA[city.lower()])

    # remove unusable data from data frame
    citydf = citydf[pd.notnull(citydf['Start Time'])]

    # modify the data frame to include required data types and columns
    expected_schema = ['Unnamed: 0', 'Start Time', 'End Time', 'Trip Duration',
       'Start Station', 'End Station', 'User Type', 'Gender', 'Birth Year',
       'Start Month', 'End Month', 'Start Day of Week', 'End Day of Week']

    # cycle through the expected columns and check they exist in the dataset loaded
    # if a column is missing all together, add it and fill the values with nans
    for column in expected_schema:
        if column not in citydf.columns:
            citydf[column] = np.nan

    citydf['Start Time'] = pd.to_datetime(citydf['Start Time'])
    citydf['End Time'] = pd.to_datetime(citydf['End Time'])
    citydf['Start Month'] = citydf['Start Time'].dt.strftime('%B')
    citydf['End Month'] = citydf['End Time'].dt.strftime('%B')
    citydf['Start Day of Week'] = citydf['Start Time'].dt.weekday_name
    citydf['End Day of Week'] = citydf['End Time'].dt.weekday_name
    citydf['Start Hour'] = citydf['Start Time'].dt.hour
    citydf['End Hour'] = citydf['End Time'].dt.hour

    # filter the data in the requested month if required
    if month.lower() != "all":
        #print(citydf[['Start Month', 'Start Day of Week', 'Start Time']].head(10))

        citydf = citydf[citydf['Start Month'].astype(str) == month]
        #print("Filtered by month {} has {} rows.".format(month, len(citydf.index)))

    # filter the data to the requested day of week if required
    if day.lower() != "all":

        citydf = citydf[citydf['Start Day of Week'].astype(str) == day]
        #print("Filtered by day {} has {} rows.".format(day, len(citydf.index)))

    print('-'*40)

    return citydf


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    global timefilter

    # TO DO: display the most common start hour
    df['Start Hour'] = df['Start Time'].dt.hour
    most_common_hour = df['Start Hour'].mode()[0]

    trips = df[df['Start Hour'] == most_common_hour]['Start Time'].count()

    print("Most popular hour:{}, Count:{}, Filter:{}".format(most_common_hour, trips, timefilter))

    # TO DO: display the most common day of week
    most_common_days = df.groupby('Start Day of Week')['Start Hour'].count().idxmax()
    trips_for_day = df.groupby('Start Day of Week')['Start Hour'].count().max()
    print("Most common Day:{}, Count:{}, Filter:{}".format(most_common_days,trips_for_day, timefilter))

    # TO DO: display the most common month
    most_common_month = df.groupby('Start Month')['Start Hour'].count().idxmax()
    trips_for_month = df.groupby('Start Month')['Start Hour'].count().max()
    print("Most common Month:{}, Count:{}, Filter:{}".format(most_common_month,trips_for_month, timefilter))

    print("\nThis took %s seconds.\n" % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    global timefilter
    # TO DO: display most commonly used start station

    most_common_start_station = df.groupby('Start Station')['Start Time'].count().idxmax()
    ss_count = df.groupby('Start Station')['Start Time'].count().max()

    print("Most popular Start Station:{}, Count:{}, Filter:{}".format(most_common_start_station, ss_count, timefilter))

    # TO DO: display most commonly used end station
    most_common_end_station = df.groupby('End Station')['End Time'].count().idxmax()
    es_count = df.groupby('End Station')['End Time'].count().max()

    print("Most popular End Station:{}, Count:{}, Filter:{}".format(most_common_end_station, es_count, timefilter))

    # TO DO: display most frequent combination of start station and end station trip
    cs_count = df.groupby(['Start Station', 'End Station'])['Start Time'].count().max(axis=0)
    most_common_combo_station = df.groupby(['Start Station', 'End Station'])['Start Time'].count().idxmax()

    print("Most popular trip station to station:{}, Count:{}, Filter:{}".format(most_common_combo_station, cs_count, timefilter))

    print("\nThis took %s seconds.\n" % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    global timefilter
    # TO DO: display total travel time
    # Total travel time is simply the sum of the Trip Durations of the filtered dataset
    # Divide by 60, then divide by 60, then divide by 24 to get total days travel time
    # Round days to two decimal places
    total_travel_time_days = round(df['Trip Duration'].sum() / 60 / 60 / 24, 2)
    total_trips = df['Start Time'].count()

    print("Total Travel Time for all Trips:{} days, Count:{}, Filter:{}".format(total_travel_time_days, total_trips, timefilter))

    # TO DO: display mean travel time
    # Mean travel time calcualted using built in mean function
    # Divide by 60 to show time in minutes
    # Round minutes to two decimal places
    average_travel_time_mins = round(df['Trip Duration'].mean() / 60, 2)

    print("Average Travel Time per Trip:{} mins, Count:{}, Filter:{}".format(average_travel_time_mins, total_trips, timefilter))

    print("\nThis took %s seconds.\n" % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    # Look for the unique list of User Types and display their count
    # For each unique user, display the count of trips per user type
    count_user_types = len(df['User Type'].unique())
    count_users_per_type = df[['User Type', 'Start Time']].fillna("Unknown").groupby('User Type')['Start Time'].agg('count').to_string()
    print("There are {} User Types for this filter. Trips recorded per User Type below: \n{}\n".format(count_user_types, count_users_per_type))

    # TO DO: Display counts of gender
    # Do a similar function for Unique Gender Types - also include where we do not know the gender
    # For each Gender (including Nan's) count the number of trips taken by that gender
    count_gender = len(df['Gender'].unique())
    count_trips_per_gender = df[['Gender', 'Start Time']].fillna("Unknown").groupby('Gender')['Start Time'].agg('count').to_string()
    print("There are {} genders for this filter. Trips taken per gender listed below: \n{}\n".format(count_gender, count_trips_per_gender))

    # TO DO: Display earliest, most recent, and most common year of birth
    # Because this is a mathematical operation, filter data to values we can use
    # Use simple data frame math functions to output this data
    this_year = datetime.date.today().year
    final_output = ""
    error_message = "We could not calculate age statistics for this data set because of {}."
    youngest_user = ""
    oldest_user = ""
    most_common_age_user = ""

    df_by_view = df[np.isfinite(df['Birth Year'])]

    # Check if any data exists for Birth Year
    if df_by_view.empty != True:
        # if it does, try and work with the data to calculate the statistics
        try:
            youngest_user = str(int(this_year - df_by_view['Birth Year'].max()))
            oldest_user = int(this_year - df_by_view['Birth Year'].min())
            most_common_age_user = int(this_year - df_by_view['Birth Year'].mode()[0])
            final_output = "Based on Birth Year, we can see the age range of our Users:\nYoungest:{} yrs Old\nOldest {} yrs Old\nMost Common {} yrs Old".format(youngest_user,                      oldest_user, most_common_age_user)
        # if it fails, record an error message that there was a data issue
        except:
            final_output = error_message.format("a Data Issue")
    # if no data exists, retuern an error message that there was no data to work with
    else:
        final_output = error_message.format("No Data being available")

    print(final_output)

    print("\nThis took %s seconds.\n" % (time.time() - start_time))
    print('-'*40)


def present_data(df):
    #function is designed to give the user the ability to run through their filtered dataset
    while True:
        review_data = input("\nWould you like to review the raw data? (Y or N)\n")
        row_from = 0
        row_to = 0

        if review_data.upper() == "Y":
            while True:
                row_input = input("\nHow many rows would you like to review? (enter number)\n")

                try:
                    rows = int(row_input)
                    row_from = row_to
                    row_to += rows

                    print(df[row_from:row_to])

                    more_data = input("\nWould you like to review more? (Y or N)\n")
                    if more_data.upper() == "Y":
                        continue
                    else:
                        break
                except:
                    print("\nOops, that doesn't look like a valid row count.")
                    continue

                break

        elif review_data.upper() == "N":
            break
        else:
            print("Oops, I don't understand ""{}"".".format(review_data))
            continue

def main():
    # Enable more display data
    pd.set_option('display.max_columns', 500)
    pd.set_option('display.width', 500)

    # Continuous loop while the user wishes to keep repeating the main process of this application
    # When they feedback "No" to restart, the loop will break/exit and the code will finish executing
    while True:
       city,month,day = get_filters()
       df = load_data(city, month, day)

       # once we have loaded up our data, make sure that we have data for the filters selected, before executing any statistics
       if df.empty != True:
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)
       else:
            print("Oops, it looks like there is no data available for your filters.\n")

        # let the user review the data
       present_data(df)

       restart = input("\nWould you like to restart and try a different filter? (Y or N)\n")
       if restart.upper() != 'Y':
            break

if __name__ == "__main__":
	main()
