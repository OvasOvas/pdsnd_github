import time
import pandas as pd
import numpy as np
from tabulate import tabulate

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
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        try:
            city = input('Enter City name e.g. (chicago, new york city, washington): ').lower()
            if city in ['chicago', 'new york city', 'washington']: 
                break
            else:
                print('wrong input, choose city name from (chicago, new york city, washington)')
        except:
            print('An Error Occured')

    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
        try:
            month = input('Enter month e.g.(all, january, february, ... , june): ').lower()
            if month in ['all', 'january', 'february', 'march', 'april', 'may', 'june']:
                break
            else:
                print('Wrong input, Enter months within January to June')
        except:
            print('wrong input, choose month name from list (january, february, march, april, may, june')
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)

    while True:
        try:
            day = input('Enter day of the week e.g. (all, monday, tuesday, ... sunday): ').title() # i changed it to lower so that 'input(all) can work'
            if day in ['All', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']:
                break
            else:
                print('Wrong input Enter day of the week between (Monday and Sunday)')
        except:
            print('wrong input, choose month name from list (january, february, march, april, may, june')
    print('-'*40)
    return city, month, day

# get_filters()


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
    # load the city data
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time']) # parse column as time
    df['Month'] = df['Start Time'].dt.month #create a month column with months 1-12
    df['Day of Week'] = df['Start Time'].dt.day_name() #create a day of week column with Days

    # filter by month
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month.lower()) + 1

        df = df[df['Month'] == month] # filters by month

    # filter by day of week
    if day != 'All': #using a capital 'All' so as to pass through the input check.
        df = df[df['Day of Week'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_month = df['Month'].mode()[0]
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    most_common_month = months[most_month - 1]
    print(f'most common month is:                {most_common_month.title()}')

    # display the most common day of week
    most_day = df['Day of Week'].mode()[0]
    print(f'most common day of week is:          {most_day}')

    # display the most common start hour
    start_hour = df['Start Time'].dt.hour
    most_start_hour = start_hour.mode()[0]
    print(f'most common start hour is:           {most_start_hour}')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_start_station = df['Start Station'].mode()[0]
    print(f'most commonly used start station is:           {most_start_station}')

    # display most commonly used end station
    most_end_station = df['End Station'].mode()[0]
    print(f'most commonly used end station is:          {most_end_station}')


    # display most frequent combination of start station and end station trip
    start_station = df['Start Station']
    end_station = df['End Station']
    # start_end_station = start_station.str.cat(end_station, sep = ' to ')
    df['start_end_station'] = df['Start Station'].str.cat(df['End Station'], sep = ' to ')
    most_start_end = df['start_end_station'].mode()[0]
    count = df['start_end_station'].value_counts().max()

    print(f'most frequent combination of start station and end station is: {most_start_end}, count: {count}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print(f'Total Travel Time is:             {total_travel_time}')

    # display mean travel time
    average_travel_time = df['Trip Duration'].mean()
    print(f'Average travel time is:           {average_travel_time}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(f'the user types count is:\n             {user_types}\n')

    try:

        # Display counts of gender
        gender = df['Gender'].value_counts()
        print(f'the Gender Count is:\n                 {gender}\n')

        # Display earliest, most recent, and most common year of birth
        earliest = df['Birth Year'].min()
        print(f'the earliest year of birth is:             {int(earliest)}')

        most_recent = df['Birth Year'].max()
        print(f'the most recent year of birth is:          {int(most_recent)}')

        most_common = df['Birth Year'].mode()[0]
        print(f'the most common year of birth is:          {int(most_common)}')

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)
    except:
        print(f'Sorry! No info for User Gender and Birth Month in this location!')
        print('-'*40)
        pass

def display_scroll(df):
    row_index = 0
    scroll = 5
    while True:
        displayer = input('Would you like to see raw data scroll? enter yes or no ').lower()
        if displayer == 'yes':
            print(tabulate(df.iloc[row_index:row_index + scroll], headers = 'keys'))
            row_index += scroll
        else: 
            break



def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_scroll(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
