# Install the cdsapi library
# pip install cdsapi
# Import the cdsapi library
import cdsapi

# Create a Client object
c = cdsapi.Client()


# Retrieve the dataset using the cdsapi Client and 
# download the dataset to the current directory
c.retrieve(
    'reanalysis-era5-land',
    {
        'variable': 'surface_pressure',
        'year': [
            '2013', '2014',
            '2015', '2016', '2017',
            '2018', '2019', '2020',
        ],
        'month': [
            '01', '02', '03',
            '04', '05', '06',
            '07', '08', '09',
            '10', '11', '12',
        ],
        'day': [
            '01', '02', '03',
            '04', '05', '06',
            '07', '08', '09',
            '10', '11', '12',
            '13', '14', '15',
            '16', '17', '18',
            '19', '20', '21',
            '22', '23', '24',
            '25', '26', '27',
            '28', '29', '30',
            '31',
        ],
        'time': '00:00',
        'format': 'netcdf',
    },
    'download.nc')

# Download the dataset to the current directory
c.download("my_dataset.netcdf")
# Check the status of the request
print(status = c.status())
