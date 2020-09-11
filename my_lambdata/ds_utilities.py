# Import libraries needed
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_wine
from pdb import set_trace as breakpoint
from IPython.display import display
import requests
from bs4 import BeautifulSoup


def get_business_info(business, city, state):
    '''
    This function  will scrape the yellowpages website and
    will return a list of the information, such as name, phone number,
    street address, city, state, and zip code for those businesses.
    Parameters:
    -----------
      business : type or name of business
      city : name of the city where the business is located
      state : the 2 character abbrivation for the state in which the
        business is located.
    Returns:
    --------
      DataFrame with information scraped from the yellowpages website,
        based on the parameters entered into the function.
    '''
    
    # Set the url to pull the data from:
    url = f'https://www.yellowpages.com/search?search_terms={business}&geo_location_terms={city}%2C+{state}&s=distance'
    # Create a get request:
    response = requests.get(url)
    # Check the status code to verify it is 200. This lets you know if there is
    #  an error reaching the website based on the code:
    if response.status_code == 200:
        # Use beautiful soup to parse everything:
        soup = BeautifulSoup(response.content, 'html.parser')
        # Get the data from the location within the webpage:
        information = soup.find_all('div', class_="info")
        data = {'Name': [], 'Phone_No': [], 'Street': [], 'City_State_Zip': []}
        for info in information:
            # Get all the attribrutes we need:
            name = info.find('a', class_="business-name").span
            name = name.text if name else None
            phone = info.find('div', class_='phones phone primary')
            phone = phone.text if phone else None
            street = info.find('div', class_='street-address')
            street = street.text if street else None
            area = info.find('div', class_='locality')
            area = area.text if area else None
            # Store the values in a data object:
            data['Name'].append(name)
            data['Phone_No'].append(phone)
            data['Street'].append(street)
            data['City_State_Zip'].append(area)
    else:
        print('There is an error, the website can not be reached.')
        
    # Turn data collected into a pandas dataframe:
    business_info = pd.DataFrame(data, columns=['Name', 'Phone_No', 'Street',
                                                'City_State_Zip'])
    return business_info


def enlarge(n):
    ''' 
    This function will multiple the input by 100 
    '''
    return n * 100


class MyDataSplitter():
    ''' 
    This class implements a 3-way data split and outputs summary metrics. 
    '''

    def __init__(self, df):
        self.df = df

    def train_validation_test_split(self, features, target,
                                    train_size=0.7, val_size=0.1,
                                    test_size=0.2, random_state=None,
                                    shuffle=True):
        '''
        This function is a utility wrapper around the Scikit-Learn train_test_split 
        that splits arrays or matrices into train, validation, and test subsets.
        Args:
            X (Numpy array or DataFrame): This is a dataframe with features.
            y (Numpy array or DataFrame): This is a pandas Series with target.
            train_size (float or int): Train split percentage (0 to 1).
            val_size (float or int): Validation split percetage (0 to 1).
            test_size (float or int): Test split percentage (0 to 1).
            random_state (int): Controls the shuffling applied to the data for reproducibility.
            shuffle (bool): Whether or not to shuffle the data before splitting
        Returns:
            Train, test, and validation dataframes for features (X) and target (y). 
        '''

        X = self.df[features]
        y = self.df[target]

        X_train_val, X_test, y_train_val, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state, shuffle=shuffle)

        X_train, X_val, y_train, y_val = train_test_split(
            X_train_val, y_train_val, test_size=val_size / (train_size + val_size),
            random_state=random_state, shuffle=shuffle)

        return X_train, X_val, X_test, y_train, y_val, y_test

    def date_divider(self, date_col):
        '''
        Param df: dataframe object from the Pandas library, entire dataframe where the date_column is located is required
        Param date_col: String value of the name of the date_column to be looked up in the passed dataframe
        Return: modified dataframe with the new Year, Month, and Day columns attached to the end.
        '''
        converted_df = self.df.copy()
        converted_df["Year"] = pd.DatetimeIndex(converted_df[date_col]).year
        converted_df["Month"] = pd.DatetimeIndex(converted_df[date_col]).month
        converted_df["Day"] = pd.DatetimeIndex(converted_df[date_col]).day
        return converted_df

    def print_split_summary(self, X_train, X_val, X_test):
        '''
        This function prints summary statistics for X_train, X_val, and X_test.
        '''
        print('######################## TRAINING DATA ########################')
        print(f'X_train Shape: {X_train.shape}')
        display(X_train.describe(include='all').transpose())
        print('')

        print('######################## VALIDATION DATA ######################')
        print(f'X_val Shape: {X_val.shape}')
        display(X_val.describe(include='all').transpose())
        print('')

        print('######################## TEST DATA ############################')
        print(f'X_test Shape: {X_test.shape}')
        display(X_test.describe(include='all').transpose())
        print('')


if __name__ == '__main__':
    # Test the enlarge function
    # y = int(input("Choose a number: "))
    # print(y, enlarge(y))

    raw_data = load_wine()
    df = pd.DataFrame(data=raw_data['data'], columns=raw_data['feature_names'])
    df['target'] = raw_data['target']

    # Test the My_Data_Splitter Class
    splitter = MyDataSplitter(df=df, features=['ash', 'hue'], target='target')
    X_train, X_val, X_test, y_train, y_val, y_test = splitter.train_validation_test_split()
    splitter.print_split_summary(X_train, X_val, X_test)