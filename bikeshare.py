import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

CITIES = ['chicago', 'new york', 'washington']

MONTHS = ['january', 'february', 'march', 'april', 'may', 'june']

DAYS = ['sunday', 'monday', 'tuesday', 'wednesday', \
        'thursday', 'friday', 'saturday']


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    while True:
        city = input('Which city do you want to explore Chicago, New York or Washington? \n> ').lower()
        if city in CITIES:
            break
    while True:
        month = input('All right! now it\'s time to provide us a month name ' \
                      'or just say \'all\' to apply no month filter. \n(e.g. all, january, february, march, april, may, june) \n> ').lower()
        if month in MONTHS:
            break

    day = input('One last thing. Could you type one of the week day you want to analyze?' \
                ' You can type \'all\' again to apply no day filter. \n(e.g. all, monday, sunday) \n> ')

    print('-' * 40)
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

    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    if month != 'all':
        month = MONTHS.index(month) + 1
        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    most_common_month = df['month'].value_counts().idxmax()
    print("The most common month is :", most_common_month)

    most_common_day_of_week = df['day_of_week'].value_counts().idxmax()
    print("The most common day of week is :", most_common_day_of_week)

    most_common_start_hour = df['hour'].value_counts().idxmax()
    print("The most common start hour is :", most_common_start_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    most_common_start_station = df['Start Station'].mode()[0]
    print("The most commonly used start station :", most_common_start_station)

    most_common_end_station = df['End Station'].mode()[0]
    print("The most commonly used end station :", most_common_end_station)

    most_common_start_end_station = df.groupby(['Start Station','End Station'])
    popular_combination_station=most_common_start_end_station.size().sort_values(ascending=False).head(1)
    print("The most commonly used start station and end station :\n", popular_combination_station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    total_travel = df['Trip Duration'].sum()
    print("Total travel time :", total_travel)

    mean_travel = df['Trip Duration'].mean()
    print("Mean travel time :", mean_travel)

    max_travel = df['Trip Duration'].max()
    print("Max travel time :", max_travel)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    print("Counts of user types:\n")
    user_counts = df['User Type'].value_counts()

    for index, user_count in enumerate(user_counts):
        print("  {}: {}".format(user_counts.index[index], user_count))

    print()

    if 'Gender' in df.columns:
        user_stats_gender(df)

    if 'Birth Year' in df.columns:
        user_stats_birth(df)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats_gender(df):
    """Displays statistics of analysis based on the gender of bikeshare users."""

    print("Counts of gender:\n")
    gender_counts = df['Gender'].value_counts()

    for index, gender_count in enumerate(gender_counts):
        print("  {}: {}".format(gender_counts.index[index], gender_count))

    print()


def user_stats_birth(df):
    """Displays statistics of analysis based on the birth years of bikeshare users."""

    birth_year = df['Birth Year']

    most_common_year = birth_year.value_counts().idxmax()
    print("The most common birth year:", most_common_year)

    most_recent = birth_year.max()
    print("The most recent birth year:", most_recent)

    earliest_year = birth_year.min()
    print("The most earliest birth year:", earliest_year)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
