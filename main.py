import geocoder
import requests
import datetime
import smtplib

CARRIERS = {
    "att": "@mms.att.net",
    "tmobile": "@tmomail.net",
    "verizon": "@vtex.com",
    "sprint": "@page.nextel.com"
}

EMAIL = "birthdayreminder101@gmail.com"
PASSWORD = "hxuzkzskuljfmrcn"


def get_random_quote():
    try:
        response = requests.get("https://quote-garden.herokuapp.com/api/v3/quotes/random")
        if response.status_code == 200:
            return response.json()
        else:
            return {'data': [{'quoteText': 'Get after it today.', 'quoteAuthor': 'Me'}]}

    except:
        print("Something went wrong! Try Again!")


def current_city():
    return geocoder.ip('me').city


def weather_query():
    api_key = "a17f26ca342b43e8244201781bf51643"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    city_name = current_city()
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name + "&units=imperial"
    return requests.get(complete_url).json()


def format_message(forecast):
    today = datetime.date.today().strftime("%A, %B %-d")
    id = forecast["weather"][0]["id"]
    weather = forecast["weather"][0]["main"]
    description = forecast["weather"][0]["description"]
    current_temp = forecast["main"]["temp"]
    feels_like = forecast["main"]["feels_like"]
    min_temp = forecast["main"]["temp_min"]
    max_temp = forecast["main"]["temp_max"]
    humidity = forecast["main"]["humidity"]
    wind_speed = forecast["wind"]["speed"]
    wind_direction = forecast["wind"]["deg"]
    clouds = forecast["clouds"]["all"]
    city = forecast["name"]
    sunrise = datetime.datetime.fromtimestamp(forecast["sys"]["sunrise"]).strftime("%-I:%M %p")
    sunset = datetime.datetime.fromtimestamp(forecast["sys"]["sunset"]).strftime("%-I:%M %p")
    qotd = get_random_quote()
    message = (
        f"Good morning Wyatt. Today is {today}.\n"
        f"Current temp in {city}: {round(current_temp)} Fn.\n"
        f"Feels like: {round(feels_like)} Fn.\n"
        f"High: {round(max_temp)} Fn | Low: {round(min_temp)} Fn\n"
        f"Today's forecast: {weather}.\n"
        f"Description: {description}.\n"
        f"Sunrise: {sunrise} | Sunset: {sunset}.\n"
        f"Quote of the day: \"{qotd['data'][0]['quoteText']}\" - {qotd['data'][0]['quoteAuthor']}\n"
    )
    return message


def send_message(phone_number, carrier, message):
    recipient = phone_number + CARRIERS[carrier]
    auth = (EMAIL, PASSWORD)

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(auth[0], auth[1])

    server.sendmail(auth[0], recipient, message)


def main():
    # forecast = weather_query()
    # message = format_message(forecast)
    send_message("8475029296", "att", "Test")


if __name__ == '__main__':
    main()
