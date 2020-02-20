from urllib.request import urlopen, Request
from bs4 import BeautifulSoup as soup
import time

# Avoid 403 error with headers
# https://stackoverflow.com/questions/47594331/python-3-urlopen-http-error-403-forbidden
r = Request('https://www.airlinequality.com/airline-reviews/american-airlines/page/1/?sortby=post_date%3ADesc&pagesize=100', headers={'User-Agent': 'Mozilla/5.0'})
page_html = urlopen(r).read()

page_soup = soup(page_html, "html.parser")
containers = page_soup.findAll("article", {"itemprop":"review"})

filename = "reviews_test1.csv"
f = open(filename, "w")

headers = ("reviewer_name, "
            "reviewer_nationality, "
            "review_date, "
            "review_title, "
            "type_of_traveler, "
            "seat_type, "
            "route, "
            "date_flown, "
            "overall_rating, "
            "seat_comfort, "
            "cabin_staff_service, "
            "food_and_beverages, "
            "inflight_entertainment, "
            "ground_service, "
            "wifi_and_connectivity, "
            "value_for_money, "
            "recommended")

f.write("")

def get_star_rating(row):
    return len(row.findAll("span", {"class": "star fill"}))

for container in containers:
    review_info = container.find("div", {"class": "body"}).find("h3").text.strip()
    reviewer_name = review_info[:review_info.find("(") - 1]
    reviewer_nationality = review_info[review_info.find("(") + 1:review_info.find(")")]
    review_date = review_info[review_info.find(")") + 2:]

    overall_rating = container.find(itemprop="reviewRating").find("span", itemprop="ratingValue").text

    body = container.find("div", {"class": "body"})
    review_title = body.find("h2").text.strip("\"")

    table_rows = body.find("div", {"class": "tc_mobile"}).find("div", {"class": "review-stats"}).find("table", {"class": "review-ratings"}).findAll("tr")
    type_of_traveler = table_rows[0].find("td", {"class", "review-value"}).text
    seat_type = table_rows[1].find("td", {"class", "review-value"}).text
    route = table_rows[2].find("td", {"class", "review-value"}).text
    date_flown = table_rows[3].find("td", {"class", "review-value"}).text


    seat_comfort = "None"
    cabin_staff_service = "None"
    food_and_beverages = "None"
    inflight_entertainment = "None"
    ground_service = "None"
    wifi_and_connectivity = "None"
    value_for_money = "None"

    for row in table_rows:
        row_title = row.find("td", {"class": "review-rating-header"}).text
        star_rating = str(get_star_rating(row))

        if row_title == "Seat Comfort":
            seat_comfort = star_rating
        
        elif row_title == "Cabin Staff Service":
            cabin_staff_service = star_rating

        elif row_title == "Food & Beverages":
            food_and_beverages = star_rating           

        elif row_title == "Inflight Entertainment":
            inflight_entertainment = star_rating           

        elif row_title == "Ground Service":
            ground_service = star_rating           
            
        elif row_title == "Wifi & Connectivity":
            wifi_and_connectivity = star_rating           

        elif row_title == "Value For Money":
            value_for_money = star_rating           

        elif row_title == "Recommended":
            recommended = row.find("td", {"class": "review-value"}).text

    f.write(reviewer_name + "," + reviewer_nationality + "," + review_date + "," + review_title + "," + type_of_traveler + "," + seat_type + "," + route + "," + date_flown + "," + overall_rating + "," + seat_comfort + "," + cabin_staff_service + "," + food_and_beverages + "," + inflight_entertainment + "," + ground_service + "," + wifi_and_connectivity + "," + value_for_money + "," + recommended + "\n")



    


f.close()
