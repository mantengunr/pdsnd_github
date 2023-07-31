import time
import pandas as pd
import numpy as np
import calendar as cal

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
        city_input = input("Enter the city name: ").lower()
        if city_input != "chicago" and city_input != "new york city" and city_input != "washington":
          print("Incorrect city. Please enter either chicago, new york city, and washington")
        else:
          break
    city = city_input
    print("You chose "+city)

    # get user input for month (all, january, february, ... , june)
    while True:
        month_input = input("Enter the month: ").lower()
        if month_input != "all" and month_input != "january" and month_input != "february" and month_input != "march" and month_input != "april" and month_input != "may" and month_input != "june":
          print("Incorrect month. Please enter either all, january, february, ... , june")
        else:
          break

    month = month_input
    print("You chose "+month)

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day_input = input("Enter the day: ").lower()
        if day_input != "all" and day_input != "monday" and day_input != "tuesday" and day_input != "wednesday" and day_input != "thursday" and day_input != "friday" and day_input != "saturday" and day_input != "sunday":
          print("Incorrect day. Please enter either all, Monday, tuesday, ... sunday")
        else:
          break

    day = day_input
    print("You chose "+day)

    print('-'*40)
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

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]
    print('Most Popular Month:', cal.month_name[popular_month])

    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print('Most Popular Day:', popular_day)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_StartTime = df['hour'].mode()[0]
    print('Most Popular Starting Hour:', popular_StartTime)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_StartStation = df['Start Station'].mode()[0]
    print('Most Popular Start Station:',popular_StartStation)

    # display most commonly used end station
    popular_EndStation = df['End Station'].mode()[0]
    print('Most Popular End Station:', popular_EndStation)

    # display most frequent combination of start station and end station trip
    combined_StartEnd = df['Start Station'] + df['End Station']
    print('Most Frequent Combination of Start and End Station Trip: ',combined_StartEnd.mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_TravelTime = sum(df['Trip Duration'])
    print('Total Travel Time:', total_TravelTime)

    # display mean travel time
    average_TravelTime = np.mean(df['Trip Duration'])
    print('Average Travel Time:', average_TravelTime)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types  = df['User Type'].value_counts()
    print(user_types)
    print(" ")

    # Display counts of gender
    if 'Gender' in df:
      gender_counts  = df['Gender'].value_counts()
      print(gender_counts)
      print(" ")

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
      print('The earliest year of birth: ', min(df['Birth Year']))
      print('The most recent year of birth: ', max(df['Birth Year']))
      print('The most common year of birth: ', df['Birth Year'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    summary = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n').lower()
    if summary.lower() != 'yes':
       print('Ok!')
    else:
       start_loc = 0
       while True:
           print(df.iloc[start_loc:start_loc + 5])
           start_loc += 5
           summary = input("Do you wish to continue?: ").lower()
           if summary.lower() != 'yes':
              break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
