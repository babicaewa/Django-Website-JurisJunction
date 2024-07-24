from django.db.models import Avg
import os
import random
from django.conf import settings
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange,
    Dimension,
    Metric,
    Filter,
    FilterExpression,
    RunReportRequest,
)
import requests
from math import radians, sin, cos, sqrt, atan2
from os.path import isfile
from os.path import join as path_join
from random import choice
from os import listdir
from django.http import JsonResponse
import json


google_maps_api_key = "Enter here"

def clean_filters(filters):
    filters = {k: v for k, v in filters.items() if v}
    return filters

def nearby_professional_locations(address):
    base_url = 'https://maps.googleapis.com/maps/api/geocode/json?'
    params = {
        'key': google_maps_api_key,
        'address': address
    }
    try:
        response = requests.get(base_url, params=params).json()
        print(response)
        if 'results' in response and response['results']:
            location = response['results'][0]['geometry']['location']
            latitude = location['lat']
            longitude = location['lng']
            print(f"location:{location}")
            print(f"Long:{longitude}")
            print(f"Lat:{latitude}")
            return latitude, longitude
        else:
            return "No results found"
    except requests.exceptions.RequestException as e:
        return f'An error occurred: {e}'

#print(nearby_professional_locations('Waco, TX, USA'))

def distance_between_points(lat1, lon1, lat2, lon2):
    # Radius of the Earth in kilometers
    earth_radius_km = 6371.0

    # Convert latitude and longitude from degrees to radians
    lat1_rad = radians(lat1)
    lon1_rad = radians(lon1)
    lat2_rad = radians(lat2)
    lon2_rad = radians(lon2)

    # Calculate differences in latitude and longitude
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    # Calculate distance using Haversine formula
    a = sin(dlat / 2)**2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance_km = earth_radius_km * c

    return distance_km


def calculate_average_rating(professional):
    return round(professional.review_set.aggregate(avg_rating=Avg('rating'))['avg_rating'],1)


#file_path = os.path.join(settings.STATICFILES_DIRS[0], 'json', 'service_account.json')
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.join(settings.BASE_DIR, 'core/static/json/service_account.json')




"""Runs a simple report on a Google Analytics 4 property."""
"""
# TODO(developer): Uncomment this variable and replace with your
#  Google Analytics 4 property ID before running the sample.
property_id = "415599247"

# Using a default constructor instructs the client to use the credentials
# specified in GOOGLE_APPLICATION_CREDENTIALS environment variable.
client = BetaAnalyticsDataClient()

request = RunReportRequest(
    property=f"properties/{property_id}",
    dimensions=[Dimension(name="city")],
    metrics=[Metric(name="activeUsers")],
    date_ranges=[DateRange(start_date="2020-03-31", end_date="today")],
)
response = client.run_report(request)

print("Report result:")
for row in response.rows:
    print(row.dimension_values[0].value, row.metric_values[0].value)
"""


def users_visited(user_page_url, property_id="415599247"):
    users_data = []
    # Runs a simple report on a Google Analytics 4 property.
        # TODO(developer): Uncomment this variable and replace with your
        #  Google Analytics 4 property ID before running the sample.
    property_id = "415599247"
            # Using a default constructor instructs the client to use the credentials
            # specified in GOOGLE_APPLICATION_CREDENTIALS environment variable.
    client = BetaAnalyticsDataClient()

    date_ranges = [
        DateRange(start_date="365daysAgo", end_date="today"),
        DateRange(start_date="30daysAgo", end_date="today"),
        DateRange(start_date="7daysAgo", end_date="today"),
        DateRange(start_date="yesterday", end_date="today")
    ]

    print(f"this is the url: {user_page_url}")
    for date_range in date_ranges:
        request = RunReportRequest(
            property=f"properties/{property_id}",
            dimensions=[Dimension(name="pagePath")],
            metrics=[Metric(name="activeUsers")],
            date_ranges=[date_range],
            dimension_filter=FilterExpression(
                    filter=Filter(
                        field_name="pagePath",
                        string_filter=Filter.StringFilter(value=user_page_url),
                    )
            )
        )

        response = client.run_report(request)
        
        print(f"Report result for {date_range.start_date} to {date_range.end_date}:")
            
        total = 0
        for row in response.rows:
            print(row.dimension_values[0].value, row.metric_values[0].value)
            total += int(row.metric_values[0].value)
        users_data.append(total)
        
    return users_data

def users_visited_past(user_page_url, property_id="415599247"):
    users_data = []
    # Runs a simple report on a Google Analytics 4 property.
        # TODO(developer): Uncomment this variable and replace with your
        #  Google Analytics 4 property ID before running the sample.
    property_id = "415599247"
            # Using a default constructor instructs the client to use the credentials
            # specified in GOOGLE_APPLICATION_CREDENTIALS environment variable.
    client = BetaAnalyticsDataClient()

    date_ranges = [
        DateRange(start_date="730daysAgo", end_date="365daysAgo"),
        DateRange(start_date="60daysAgo", end_date="30daysAgo"),
        DateRange(start_date="14daysAgo", end_date="7daysAgo"),
        DateRange(start_date="2daysAgo", end_date="yesterday")
    ]

    print(f"this is the url: {user_page_url}")
    for date_range in date_ranges:
        request = RunReportRequest(
            property=f"properties/{property_id}",
            dimensions=[Dimension(name="pagePath")],
            metrics=[Metric(name="activeUsers")],
            date_ranges=[date_range],
            dimension_filter=FilterExpression(
                    filter=Filter(
                        field_name="pagePath",
                        string_filter=Filter.StringFilter(value=user_page_url),
                    )
            )
        )

        response = client.run_report(request)
        
        print(f"Report result for {date_range.start_date} to {date_range.end_date}:")
            
        total = 0
        for row in response.rows:
            print(row.dimension_values[0].value, row.metric_values[0].value)
            total += int(row.metric_values[0].value)
        users_data.append(total)
        
    return users_data

def time_spent(user_page_url, property_id="415599247"):
    users_data = []
    # Runs a simple report on a Google Analytics 4 property.
        # TODO(developer): Uncomment this variable and replace with your
        #  Google Analytics 4 property ID before running the sample.
    property_id = "415599247"
            # Using a default constructor instructs the client to use the credentials
            # specified in GOOGLE_APPLICATION_CREDENTIALS environment variable.
    client = BetaAnalyticsDataClient()

    date_ranges = [
        DateRange(start_date='2015-08-14', end_date="today"),
    ]

    print(f"this is the url: {user_page_url}")
    for date_range in date_ranges:
        request = RunReportRequest(
            property=f"properties/{property_id}",
            dimensions=[Dimension(name="pagePath")],
            metrics=[Metric(name="averageSessionDuration")],
            date_ranges=[date_range],
            dimension_filter=FilterExpression(
                    filter=Filter(
                        field_name="pagePath",
                        string_filter=Filter.StringFilter(value=user_page_url),
                    )
            )
        )

        response = client.run_report(request)
        
        print(f"Report result for {date_range.start_date} to {date_range.end_date}:")
            
        total = 0
        print(f"what sigma {response.rows}")
        if response.rows:

            for row in response.rows:
                print(row.dimension_values[0].value, row.metric_values[0].value)
                print(f"this the number idk why: {row.metric_values[0].value}")
                #total += int(row.metric_values[0].value)
                total = int(float(row.metric_values[0].value))
        
    return total




def top5_cities(user_page_url, property_id="415599247"):
    top5_cities_arr = []
    # Runs a simple report on a Google Analytics 4 property.
        # TODO(developer): Uncomment this variable and replace with your
        #  Google Analytics 4 property ID before running the sample.
    property_id = "415599247"
            # Using a default constructor instructs the client to use the credentials
            # specified in GOOGLE_APPLICATION_CREDENTIALS environment variable.
    client = BetaAnalyticsDataClient()

    date_ranges = [
        DateRange(start_date="365daysAgo", end_date="today"),
        DateRange(start_date="30daysAgo", end_date="today"),
        DateRange(start_date="7daysAgo", end_date="today"),
        DateRange(start_date="yesterday", end_date="today")
    ]

    print(f"this is the url: {user_page_url}")
    for date_range in date_ranges:
        request = RunReportRequest(
            property=f"properties/{property_id}",
            dimensions=[Dimension(name="city")],
            metrics=[Metric(name="activeUsers")],
            date_ranges=[date_range],
            dimension_filter=FilterExpression(
                    filter=Filter(
                        field_name="pagePath",
                        string_filter=Filter.StringFilter(value=user_page_url),
                    )
            )
        )

        response = client.run_report(request)
        
        print(f"Report result for {date_range.start_date} to {date_range.end_date}:")
            
        total_per_period = []
        for row in response.rows:
            print(row.dimension_values[0].value, row.metric_values[0].value)
            total_per_period.append((row.dimension_values[0].value, row.metric_values[0].value))
        top5_cities_arr.append(total_per_period)


        print("\n")
    print(top5_cities_arr)
    return top5_cities_arr

def get_random_blog_photo():
    media_root = settings.MEDIA_ROOT
    folder_path = os.path.join(media_root, 'blog_photos')
    files = [
        content for content in listdir(media_root)
        if isfile(path_join(folder_path, content))
    ]
    print(f"folder_path: {folder_path}")
    return choice(files)

def users_visited_overview(user_page_url, property_id="415599247"):
    users_data = []
    # Runs a simple report on a Google Analytics 4 property.
        # TODO(developer): Uncomment this variable and replace with your
        #  Google Analytics 4 property ID before running the sample.
    property_id = "415599247"
            # Using a default constructor instructs the client to use the credentials
            # specified in GOOGLE_APPLICATION_CREDENTIALS environment variable.
    client = BetaAnalyticsDataClient()

    date_ranges = [
        DateRange(start_date="28daysAgo", end_date="21daysAgo"),
        DateRange(start_date="21daysAgo", end_date="14daysAgo"),
        DateRange(start_date="14daysAgo", end_date="7daysAgo"),
        DateRange(start_date="7daysAgo", end_date="today"),
    ]

    print(f"this is the url: {user_page_url}")
    for date_range in date_ranges:
        request = RunReportRequest(
            property=f"properties/{property_id}",
            dimensions=[Dimension(name="pagePath")],
            metrics=[Metric(name="activeUsers")],
            date_ranges=[date_range],
            dimension_filter=FilterExpression(
                    filter=Filter(
                        field_name="pagePath",
                        string_filter=Filter.StringFilter(value=user_page_url),
                    )
            )
        )

        response = client.run_report(request)
        
        print(f"Report result for {date_range.start_date} to {date_range.end_date}:")
            
        total = 0
        data_per_week = []
        for row in response.rows:
            print(row.dimension_values[0].value, row.metric_values[0].value)
            total += int(row.metric_values[0].value)
        users_data.append((f"{date_range.start_date} to {date_range.end_date}", total))
    print(f"user_data -- {users_data}")

    return users_data

