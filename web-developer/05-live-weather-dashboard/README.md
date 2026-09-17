# Star Weather — Live Weather Dashboard

A real, live weather dashboard built with plain HTML5, CSS3, and vanilla
JavaScript (ES6+). Search any city on Earth (or use your device's current
location), and see real current conditions plus a real 5-day forecast —
powered entirely by the free [Open-Meteo](https://open-meteo.com) API,
which requires **no API key, no sign-up, and no secrets** of any kind.

This project is the direct capstone of Course 08, Lessons 4 and 5
(the Fetch API and `async`/`await`).

## Live Data Sources

This app calls two real, public Open-Meteo endpoints directly from the browser:

- **Geocoding** (city name → coordinates):
  `https://geocoding-api.open-meteo.com/v1/search?name=<city>&count=6&language=en&format=json`
- **Forecast** (coordinates → current + 5-day weather):
  `https://api.open-meteo.com/v1/forecast?latitude=<lat>&longitude=<lon>&current=temperature_2m,apparent_temperature,relative_humidity_2m,weather_code,wind_speed_10m&daily=weather_code,temperature_2m_max,temperature_2m_min&timezone=auto&forecast_days=5`

Both endpoints are free and open — no key, token, or account is required to
run this app. Weather condition codes are translated to icons/labels using
the official WMO Weather interpretation codes table from Open-Meteo's docs.

## Features

- Type-ahead city search with debounced autocomplete suggestions (region shown alongside each match)
- Keyboard navigation of suggestions with Arrow Up/Down and Escape
- "My Location" button using the browser's Geolocation API
- Real current conditions: temperature, "feels like", humidity, wind speed, and a weather icon/label
- Real 5-day forecast with daily high/low temperatures
- °C / °F unit toggle, recalculated instantly from the same fetched data (no extra API call)
- The last-viewed location is remembered in Local Storage and reloaded automatically next visit
- Clear loading and error states if a search fails or the network is unavailable

## How It Works

1. As you type a city name, the app debounces your input (waits ~350ms after you stop typing) and calls the **geocoding** endpoint to find matching places.
2. Selecting a city (or pressing Enter/Search) grabs its latitude/longitude and calls the **forecast** endpoint for that exact location.
3. The response is rendered into the current-conditions card and the 5-day forecast grid using plain DOM manipulation — no frameworks.
4. The chosen location is saved to Local Storage, so reopening the page automatically re-fetches fresh live weather for wherever you looked up last.
5. `async`/`await` with `try`/`catch` wraps every network call, so a failed request (offline, typo'd city, etc.) shows a clear error message instead of breaking the page.

## Folder Structure
```
05-live-weather-dashboard/
├── index.html     # App structure and markup
├── styles.css     # All styling, layout, and responsive rules
├── script.js      # Geocoding + forecast fetch logic, rendering, events
└── README.md      # This file
```

## Run It Locally
No build tools, install steps, or API keys required.

- **Option A:** Double-click `index.html`, or drag it into any browser window.
- **Option B (recommended, avoids any local file quirks):**
  ```
  npx serve .
  ```
  then open the printed `http://localhost:...` address in your browser.

Note: because this app makes real `fetch()` calls to `api.open-meteo.com` and
`geocoding-api.open-meteo.com`, it needs an active internet connection to
show live data — it will show a friendly error message if you're offline.

## Try It Yourself

1. Search for your own city and confirm the current temperature and forecast look plausible for today's actual weather.
2. Click "My Location" and allow location access — confirm it loads weather for wherever you actually are.
3. Toggle °F/°C and confirm every temperature on the page updates instantly.
4. Reload the page and confirm your last-searched city loads automatically without you typing anything.
5. Turn off your Wi-Fi and try searching — confirm you see a clear error message instead of a blank or broken page.

## Deploy to Vercel

**Option A — Import via the Vercel website**
1. Push this folder to a new GitHub repository:
   ```
   git init
   git add .
   git commit -m "Initial commit: live weather dashboard"
   git remote add origin https://github.com/<your-username>/live-weather-dashboard.git
   git branch -M main
   git push -u origin main
   ```
2. Go to [vercel.com](https://vercel.com), sign in, click **Add New Project**, and select this repository.
3. No build command is needed for a static HTML/CSS/JS site — click **Deploy**.
4. Vercel gives you a live URL such as `https://live-weather-dashboard.vercel.app`.

**Option B — Vercel CLI**
```
npm install -g vercel
vercel
```
Follow the CLI prompts; it deploys the current folder directly and prints a live URL.

Once connected to GitHub, every future `git push` to `main` automatically redeploys the live site.
