import tkinter as tk
from tkinter import ttk
from urllib import response
import requests
from PIL import Image, ImageTk
from io import BytesIO

API_KEY = "69da0ecd973e7780a719eefa2f0a4750"

CURRENT_URL = "https://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"

class WeatherApp:

    def __init__(self, root):

        self.root = root
        self.root.title("Weather App")
        self.root.geometry("600x800")

        self.unit = "metric"

        title = tk.Label(root,
                         text="Weather App",
                         font=("Arial", 22, "bold"))
        title.pack(pady=10)

        frame = tk.Frame(root)
        frame.pack()

        self.city_entry = tk.Entry(frame, width=25, font=("Arial", 14))
        self.city_entry.pack(side=tk.LEFT, padx=5)

        search_btn = tk.Button(frame,
                               text="Get Weather",
                               command=self.get_weather)
        search_btn.pack(side=tk.LEFT)

        location_btn = tk.Button(frame,
                                 text="Use My Location",
                                 command=self.detect_location)
        location_btn.pack(side=tk.LEFT, padx=5)

        self.toggle_btn = tk.Button(root,
                                    text="Switch to °F",
                                    command=self.toggle_units)

        self.toggle_btn.pack(pady=5)

        self.icon_label = tk.Label(root)
        self.icon_label.pack()

        self.result = tk.Label(root,
                               font=("Arial", 13),
                               justify="left")
        self.result.pack()

        tk.Label(root,
                 text="Next 6 Hours",
                 font=("Arial", 15, "bold")).pack()

        self.hourly = tk.Text(root,
                              height=8,
                              width=70)
        self.hourly.pack()

        tk.Label(root,
                 text="Next 5 Days",
                 font=("Arial", 15, "bold")).pack()

        self.daily = tk.Text(root,
                             height=10,
                             width=70)
        self.daily.pack()

    def toggle_units(self):

        if self.unit == "metric":
            self.unit = "imperial"
            self.toggle_btn.config(text="Switch to °C")
        else:
            self.unit = "metric"
            self.toggle_btn.config(text="Switch to °F")

        if self.city_entry.get():
            self.get_weather()

    def detect_location(self):

        try:
            data = requests.get("https://ipinfo.io/json").json()

            city = data["city"]

            self.city_entry.delete(0, tk.END)
            self.city_entry.insert(0, city)

            self.get_weather()

        except:
            self.result.config(text="Unable to detect location.")

    def get_icon(self, icon_code):

        url = f"https://openweathermap.org/img/wn/{icon_code}@2x.png"

        image = requests.get(url).content

        img = Image.open(BytesIO(image))

        photo = ImageTk.PhotoImage(img)

        self.icon_label.config(image=photo)

        self.icon_label.image = photo

    def get_weather(self):

        city = self.city_entry.get().strip()

        if city == "":
            self.result.config(text="Please enter a city.")
            return

        params = {
            "q": city,
            "appid": API_KEY,
            "units": self.unit
        }

        try:

            response = requests.get(CURRENT_URL,
                                    params=params,
                                    timeout=10)

            if response.status_code == 404:
                self.result.config(text="City not found.")
                return

            if response.status_code == 401:
                self.result.config(text="Invalid API Key.")
                return

            data = response.json()

            temp = data["main"]["temp"]

            humidity = data["main"]["humidity"]

            weather = data["weather"][0]["description"]

            wind = data["wind"]["speed"]

            icon = data["weather"][0]["icon"]

            self.get_icon(icon)

            if self.unit == "metric":
                c = temp
                f = c * 9 / 5 + 32
            else:
                f = temp
                c = (f - 32) * 5 / 9

            self.result.config(

                text=f"""
Temperature: {c:.1f} °C
Temperature: {f:.1f} °F

Humidity: {humidity} %

Weather: {weather.title()}

Wind Speed: {wind}
"""
            )

            self.get_forecast(city)

        except requests.exceptions.Timeout:

            self.result.config(text="Request Timeout")

        except requests.exceptions.ConnectionError:

            self.result.config(text="No Internet Connection")

        except Exception as e:

            self.result.config(text=str(e))

    def get_forecast(self, city):

        params = {
            "q": city,
            "appid": API_KEY,
            "units": self.unit
        }

        response = requests.get(FORECAST_URL,params=params)
        response = requests.get(FORECAST_URL, params=params, timeout=10)

        if response.status_code != 200:
         self.result.config(text="Unable to fetch forecast.")
         return

        data = response.json()

        self.hourly.delete("1.0", tk.END)
        self.daily.delete("1.0", tk.END)

        forecasts = data["list"]

        self.hourly.insert(tk.END,
                           "Time\tTemp\tWeather\n\n")

        for item in forecasts[:6]:

            time = item["dt_txt"]

            temp = item["main"]["temp"]

            weather = item["weather"][0]["main"]

            self.hourly.insert(tk.END,
                               f"{time}\t{temp}°\t{weather}\n")

        self.daily.insert(tk.END,
                          "Date\tTemp\tWeather\n\n")

        shown = []

        for item in forecasts:

            date = item["dt_txt"].split()[0]

            if date not in shown:

                shown.append(date)

                temp = item["main"]["temp"]

                weather = item["weather"][0]["main"]

                self.daily.insert(tk.END,
                                  f"{date}\t{temp}°\t{weather}\n")

            if len(shown) == 5:
                break

root = tk.Tk()

WeatherApp(root)

root.mainloop()