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
        city = input("Which city would you like to explore - Chicago, New York City, or Washington?\n").lower()
        if city in CITY_DATA.keys():
            print("{}, it is!\n".format(city.title()))
            break
        else:
            print("Sorry, that's not a valid city. Please try again.")
    

    # get user input for month (all, january, february, ... , june)
    while(True):
        month = input("Which month? January, February, March, April, May, June, or all?\n").lower()
        if month in ['january', 'february', 'march', 'april', 'may', 'june', 'all']:
            if month == 'all':
                print("Great! Let\'s look into ALL the months!\n")
            else:
                print("Great! Let\'s examine {} a bit closer!\n".format(month.title()))
            break
        else:
            print("Sorry, that's not a valid choice. Please try again.")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while(True):
        day = input("Which day of the week would you like to examine? Type \'all\' for every day of the week.\n").lower()
        if day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']:
            if day == 'all':
                print("Great! Let\'s look at every day of the week!\n")
            else:
                print("Great! Let\'s focus our attention towards {}!\n".format(day.title()))
            break
        else:
            print("Sorry, that's not a proper selection. Please try again.")

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

    # pulling specified city data and adding columns that will assist in our stats calculations
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    df['month'] = df['Start Time'].dt.month_name()
    df['day'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour
    df['Start and End'] = df['Start Station'] + " - " + df['End Station']

    # filtering data by desired user output
    if(month != 'all'):
        df = df[df['month'] == month.title()]
    if(day != 'all'):
        df = df[df['day'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    try:
        print('Most common month: ', df['month'].mode()[0])
    except KeyError:
        print("There is no common month for this specified timeframe.")

    # display the most common day of week
    try:
        print('Most common day of the week: ', df['day'].mode()[0])
    except KeyError:
        print("There is no common day for this specified timeframe.")

    # display the most common start hour
    try:
        print('Most common starting hour: ', df['hour'].mode()[0])
    except KeyError:
        print("There is no common hour for this specified timeframe.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print("Most common start station: ", df['Start Station'].mode()[0])

    # display most commonly used end station
    print("Most common end station: ", df['End Station'].mode()[0])

    # display most frequent combination of start station and end station trip
    print("Most common trip combination: ", df['Start and End'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # we will use numpy here to aggregate data faster
    trip_duration = df['Trip Duration'].to_numpy()

    # display total travel time
    print("Total travel time: ", np.sum(trip_duration), "hrs")

    # display mean travel time
    print("Mean travel time: ", np.round(np.mean(trip_duration), 2), "hrs")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("Counts of user types:\n", df['User Type'].value_counts(), "\n")

    # Display counts of gender
    try:
        print("Counts of genders:\n", df['Gender'].value_counts(), "\n")
    except KeyError:
        print("There are no available gender statistics for this dataset.")

    # Display earliest, most recent, and most common year of birth
    try:
        print("Earliest birth year: ", int(df['Birth Year'].min()))
        print("Most recent birth year: ", int(df['Birth Year'].max()))
        print("Most common birth year: ", int(df['Birth Year'].mode()[0]))
    except KeyError:
        print("There are no birth year statistics for this dataset.")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def show_data(df):
    display_data = input("Would you like to see 5 rows of data for this particular dataset? Please reply with yes or no.\n").lower()
    data_ind = 0

    # Checking for additional columns to be included in output, if they exist
    if set(['Gender', 'Birth Year']).issubset(df.columns):
        relevant_cols = ['Start Time', 'End Time', 'Trip Duration', 'Start Station', 'End Station', 'User Type', 'Gender', 'Birth Year']
    else:
        relevant_cols = ['Start Time', 'End Time', 'Trip Duration', 'Start Station', 'End Station', 'User Type']

    # Output 5 rows of data and continue doing so if user desires
    while((display_data == "yes") and (data_ind <= df.size)):
        if(data_ind + 5 >= df.size):
            print(df[relevant_cols].iloc[data_ind:df.size-1])
        else:
            print(df[relevant_cols].iloc[data_ind:data_ind+5])
        data_ind += 5
        if(data_ind >= df.size):
            break
        display_data = input("Would you like to see 5 more rows of data? Reply with yes or no.\n").lower()


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        show_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()