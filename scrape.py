###################################################################
# Python web scraper
# 
# By Izhar Hamer
# 
###################################################################




from urllib.request import urlopen, Request
from bs4 import BeautifulSoup as soup
import time

# Create csv
filename = "reviews_American.csv"
f = open(filename, "w")

headers = ("reviewer_name, "
            "reviewer_nationality, "
            "review_date, "
            "review_title, "
            "review_text, "
            "aircraft, "
            "type_of_traveller, "
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

f.write(headers + "\n")

# Loop over all pages
for i in range(37):

    # Make sure page starts at 1
    if i == 0:
        continue

    # Avoid 403 error with headers
    # https://stackoverflow.com/questions/47594331/python-3-urlopen-http-error-403-forbidden
    r = Request('https://www.airlinequality.com/airline-reviews/american-airlines/page/'+ str(i) +'/?sortby=post_date%3ADesc&pagesize=100', headers={'User-Agent': 'Mozilla/5.0'})
    
    # Delta airlines
    # r = Request('https://www.airlinequality.com/airline-reviews/delta-air-lines/page/' + str(i) + '/?sortby=post_date%3ADesc&pagesize=100', headers={'User-Agent': 'Mozilla/5.0'})
    
    
    
    page_html = urlopen(r).read()

    page_soup = soup(page_html, "html.parser")
    containers = page_soup.findAll("article", {"itemprop":"review"})



    def get_star_rating(row):
        rating = len(row.findAll("span", {"class": "star fill"}))
        if rating != 0:
            return str(rating)
        else:
            return "999"

    def get_review_value(row):
        return row.find("td", {"class", "review-value"}).text

    for container in containers:
        review_info = container.find("div", {"class": "body"}).find("h3").text.strip()

        # Check if user has left previous reviews
        if not review_info[0].isalpha():
            reviewer_name = review_info[13:review_info.find("(") - 1].strip()
        else:
            reviewer_name = review_info[:review_info.find("(") - 1]

        reviewer_nationality = review_info[review_info.find("(") + 1:review_info.find(")")]
        review_date = review_info[review_info.find(")") + 2:]

        try:
            overall_rating = container.find(itemprop="reviewRating").find("span", itemprop="ratingValue").text
        except:
            overall_rating = "999"

        body = container.find("div", {"class": "body"})

        review_title = body.find("h2").text.replace("\"", "").strip()
        

        review_text_full = body.find("div", {"class": "tc_mobile"}).find("div", {"class": "text_content"}).text
        review_text = review_text_full[review_text_full.find("|") + 2:]
        

        table_rows = body.find("div", {"class": "tc_mobile"}).find("div", {"class": "review-stats"}).find("table", {"class": "review-ratings"}).findAll("tr")

        # Decalre all table row variables
        aircraft = "."
        seat_comfort = "."
        cabin_staff_service = "."
        food_and_beverages = "."
        inflight_entertainment = "."
        ground_service = "."
        wifi_and_connectivity = "."
        value_for_money = "."

        for row in table_rows:
            row_title = row.find("td", {"class": "review-rating-header"}).text
            star_rating = get_star_rating(row)

            if row_title == "Aircraft":
                aircraft = get_review_value(row)
            
            elif row_title == "Type Of Traveller":
                type_of_traveller = get_review_value(row)
            
            elif row_title == "Seat Type":
                seat_type = get_review_value(row)
            
            elif row_title == "Route":
                route = get_review_value(row)
            
            elif row_title == "Date Flown":
                date_flown = get_review_value(row)

            elif row_title == "Seat Comfort":
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

        f.write(reviewer_name.replace(",", "|").strip() + "," + reviewer_nationality.replace(",", "|").strip() + "," + review_date.replace(",", "|").strip() + "," + review_title.replace(",", "|").strip() + "," + review_text.replace(",", "|").strip() + "," + aircraft.replace(",", "|").strip() + "," + type_of_traveller.replace(",", "|").strip() + "," + seat_type.replace(",", "|").strip() + "," + route.replace(",", "|").strip() + "," + date_flown.replace(",", "|").strip() + "," + overall_rating + "," + seat_comfort + "," + cabin_staff_service + "," + food_and_beverages + "," + inflight_entertainment + "," + ground_service + "," + wifi_and_connectivity + "," + value_for_money + "," + recommended + "\n")
    
    # Adjust crawl speed
    time.sleep(5)

f.close()
