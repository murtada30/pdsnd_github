import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    while True:
        city= input("please enter a city (chicago, new york city, washington) : ").lower();
        if (city not in ("chicago", "new york city", "washington")):
            print("invalid city  !!")
            continue
        else:
            break

    # get user input for month (all, january, february, ... , june)

    while True:
        month= input("please type a month : (january, february, march, april, may, june) or all for no filter ").lower()
        if (month not in ("all", "january", "february","march","april","may","june")):
            print("invalid month  !!")
            continue
        else:
            break


    # get user input for day of week (all, monday, tuesday, ... sunday)

    while True:
        day= input("please type a day :(sunday, monday, tuesday, wednesday, thursday, friday) or all for no filter ").lower()
        if (day not in ("all", "sunday", "monday","tuesday","wednesday","thursday","friday")):
            print("invalid day  !!")
            continue
        else:
            break


    print('-'*40)
    return city, month, day

# a function to load data to data frame
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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour

    return df

# a function to calculate time statistics
def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    # find most common travelling month
    top_month=months[find_top_occurance(df,'month')-1]
    print("the top travled month is: " + top_month)


    # display the most common day of week

    print("the top travled day is: " + str(find_top_occurance(df,'day_of_week')))

    # display the most common start hour

    print("the top travled hour is : " + str(find_top_occurance(df,'hour')))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

# a function to compute stations statistics
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print("the top used start station  is: " + str(find_top_occurance(df,'Start Station')))

    # display most commonly used end station
    print("the top used end station  is: " + str(find_top_occurance(df,'End Station')))

    # display most frequent combination of start station and end station trip
    print("the top used route  is :" + str(df['Start Station'].groupby(df['End Station']).value_counts().nlargest(1)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

# a function to compute trips statistics
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time in hours
    print("the total travel time  in hours is :" + str((df['Trip Duration'].sum()/360)))

    # display mean travel time in minutes
    print("the mean travel time is minutes :" + str((df['Trip Duration'].mean()/60)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

# a function to compute users statistics
def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print(df['User Type'].value_counts())

    #find gender and birth year statistics for new york city and chicago only
    if(city=="new york city" or city == "chicago"):
        # Display counts of gender
        print(df['Gender'].value_counts())

        # Display earliest, most recent, and most common year of birth
        print("the earlist birth year is :" + str(int(df['Birth Year'].min())))
        print("the most recient birth year is :" + str(int(df['Birth Year'].max())))
        print("the most comon birth year is :" + str(int (find_top_occurance(df,'Birth Year'))))
    else:
        print("no Gendor or birth year info availble for Washington")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

# a function to display raw data, 5 lines at a time
def display_data(df):
    n=0 # line number intialization

    # iterate until getting a vlid user input
    while True:
        dispaly_answer= input("do you want to display raw data? (yes/no)? ")
        if (dispaly_answer.lower() not in ("yes","no")):# handling wrong user input
            print("invalid answer  !!")
            continue
        else:
            if(dispaly_answer.lower() == "yes"):# if user wants to display raw data
                while True:
                    print(df.iloc[n:n+5])# displaying 5 data rows at a time
                    dispaly_more= input("do you want to display more raw data (yes/no)? ")# asking if user wants to display more data
                    if (dispaly_more.lower() not in ("yes","no")):# chicking user input
                        print("invalid answer  !!")
                        continue
                    elif (dispaly_more.lower() == "yes"): # loop again to display more data
                        n+=5
                        continue
                    else:# user wants to stop displaying more data
                        return

            else:# user does not want to display any data
                break

    print('-'*40)

# a function to find top occurence of any column
def find_top_occurance(df,column_name):

    # calculate data count and find indexes
    top_occurance = df[column_name].value_counts().index
    # return top value in index 0
    return top_occurance[0]

# main function
def main():
    while True:
        # filter and load data
        city, month, day = get_filters()
        df = load_data(city, month, day)

        # find and print statistics
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)

        # display raw data
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
