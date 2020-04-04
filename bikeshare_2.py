import time
import pandas as pd

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
        city = input('Which city you want to analyze?\n Chicago, New York City or Washington\n').lower()
        if city.lower() not in ('chicago', 'new york city','washington'):
            print('Choose a avaliable city')
            continue
        else:
            break

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input('Which month?\n all, january, february, march, april, may or june\n').lower()
        if month.lower() not in ('all','january', 'february', 'march', 'april', 'may','june'):
            print('Choose a existing option')
            continue
        else:
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input('Which day of the week? \n all, sunday, monday, tuesday, wednesday, thursday, friday or saturday\n').lower()
        if day.lower() not in ('all','sunday', 'monday', 'tuesday',
                                 'wednesday', 'thursday', 'friday','saturday'):
            print('Choose a existing option')
            continue
        else:
            break

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
    df = pd.read_csv("{}.csv".format(city.replace(" ","_")))

    # Convert the Start and End Time columns to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].apply(lambda x: x.month)
    df['day_of_week'] = df['Start Time'].apply(lambda x: x.strftime('%A').lower())


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df.loc[df['month'] == month,:]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df.loc[df['day_of_week'] == day,:]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['month'].value_counts().keys()[0]
    print(f'Common month: {common_month}')

    # display the most common day of week
    common_day = df['day_of_week'].value_counts().keys()[0]
    print(f'Common day of week: {common_day}')

    # display the most common start hour
    hour = df['Start Time'].value_counts().keys()[0]
    hour_only = str(hour)[11:13]
    print(f'Common hour: {hour_only}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    pop_start = df['Start Station'].value_counts().keys()[0]
    count_start = df['Start Station'].value_counts().tolist()[0]

    print(f'The most common Start Station is {pop_start} with count: {count_start}')

    # display most commonly used end station
    pop_end = df['End Station'].value_counts().keys()[0]
    count_end = df['End Station'].value_counts().tolist()[0]

    print(f'The most common End Station is {pop_end} with count: {count_end}')

    # display most frequent combination of start station and end station trip
    df['Combination Station'] = df['Start Station'] + ' ' + df['End Station']
    pop_combination = df['Combination Station'].value_counts().keys()[0]
    count_combination = df['Combination Station'].value_counts().tolist()[0]

    print(f'The most frequent combination is {pop_combination} with count: {count_combination}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

   total_trip_duration = df['Trip Duration'].sum()
    avg_trip_duration = df['Trip Duration'].mean()
    m, s = divmod(total_trip_duration, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)
    y, d = divmod(d, 365)
    total_trip_duration = "\nTotal trip duration: %d years %02d days %02d hrs %02d min %02d sec" % (y, d, h, m, s)
    print(total_trip_duration)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    # display mean travel time
    m, s = divmod(avg_trip_duration, 60)
    h, m = divmod(m, 60)
    avg_trip_duration = "Average trip duration: %d hrs %02d min %02d sec" % (h, m, s)
    print(avg_trip_duration)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    users = df['User Type'].value_counts().keys()
    count_users = df['User Type'].value_counts().tolist()
    users_count = dict(zip(users,count_users))
    print(users_count)

    # Display counts of gender
    if 'Gender' in df.columns:

        genders = df['Gender'].value_counts().keys()
        count_genders = df['Gender'].value_counts().tolist()
        genders_count = dict(zip(genders,count_genders))
        print(genders_count)
    else:
        print('\nColumn Gender does not exist in dataset')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earlist,recent,common = df['Birth Year'].min(), df['Birth Year'].max(), df['Birth Year'].value_counts().keys()[0]
        print(f'Earlist: {earlist}, Recent: {recent} and Common: {common}')

        #print("\nThis took %s seconds." % (time.time() - start_time))
        #print('-'*40)
    else:
        print('\nColumn Birth Year does not exist in dataset')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


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
