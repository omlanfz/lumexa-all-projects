// Star Weather — Live Weather Dashboard
// Data source: Open-Meteo (https://open-meteo.com) — fully free, no API key required.
//   Geocoding:  https://geocoding-api.open-meteo.com/v1/search
//   Forecast:   https://api.open-meteo.com/v1/forecast

const GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search";
const FORECAST_URL = "https://api.open-meteo.com/v1/forecast";
const LAST_LOCATION_KEY = "lumexa-weather-last-location";

// --- WMO Weather interpretation codes -> emoji + label ---
// Reference: https://open-meteo.com/en/docs (WMO Weather interpretation codes table)
const WEATHER_CODE_MAP = {
  0: { icon: "☀️", label: "Clear sky" },
  1: { icon: "🌤️", label: "Mainly clear" },
  2: { icon: "⛅", label: "Partly cloudy" },
  3: { icon: "☁️", label: "Overcast" },
  45: { icon: "🌫️", label: "Fog" },
  48: { icon: "🌫️", label: "Depositing rime fog" },
  51: { icon: "🌦️", label: "Light drizzle" },
  53: { icon: "🌦️", label: "Moderate drizzle" },
  55: { icon: "🌧️", label: "Dense drizzle" },
  56: { icon: "🌧️", label: "Light freezing drizzle" },
  57: { icon: "🌧️", label: "Dense freezing drizzle" },
  61: { icon: "🌦️", label: "Slight rain" },
  63: { icon: "🌧️", label: "Moderate rain" },
  65: { icon: "🌧️", label: "Heavy rain" },
  66: { icon: "🌧️", label: "Light freezing rain" },
  67: { icon: "🌧️", label: "Heavy freezing rain" },
  71: { icon: "🌨️", label: "Slight snow fall" },
  73: { icon: "🌨️", label: "Moderate snow fall" },
  75: { icon: "❄️", label: "Heavy snow fall" },
  77: { icon: "❄️", label: "Snow grains" },
  80: { icon: "🌦️", label: "Slight rain showers" },
  81: { icon: "🌧️", label: "Moderate rain showers" },
  82: { icon: "⛈️", label: "Violent rain showers" },
  85: { icon: "🌨️", label: "Slight snow showers" },
  86: { icon: "❄️", label: "Heavy snow showers" },
  95: { icon: "⛈️", label: "Thunderstorm" },
  96: { icon: "⛈️", label: "Thunderstorm with slight hail" },
  99: { icon: "⛈️", label: "Thunderstorm with heavy hail" },
};

function describeWeatherCode(code) {
  return WEATHER_CODE_MAP[code] || { icon: "🌡️", label: "Unknown conditions" };
}

// --- ELEMENTS ---
const searchForm = document.querySelector("#search-form");
const cityInput = document.querySelector("#city-input");
const locationBtn = document.querySelector("#location-btn");
const suggestionsEl = document.querySelector("#suggestions");
const statusMsgEl = document.querySelector("#status-msg");
const dashboardEl = document.querySelector("#dashboard");
const unitToggleBtn = document.querySelector("#unit-toggle-btn");

const currentIconEl = document.querySelector("#current-icon");
const currentTempEl = document.querySelector("#current-temp");
const currentPlaceEl = document.querySelector("#current-place");
const currentConditionEl = document.querySelector("#current-condition");
const currentFeelsEl = document.querySelector("#current-feels");
const currentHumidityEl = document.querySelector("#current-humidity");
const currentWindEl = document.querySelector("#current-wind");
const updatedAtEl = document.querySelector("#updated-at");
const forecastListEl = document.querySelector("#forecast-list");

// --- STATE ---
let lastWeatherData = null; // most recently fetched forecast payload, kept for unit re-render
let unit = "celsius"; // "celsius" | "fahrenheit"
let debounceTimer = null;
let activeSuggestionIndex = -1;

// --- HELPERS ---
function celsiusToFahrenheit(celsius) {
  return celsius * (9 / 5) + 32;
}

function formatTemp(celsiusValue) {
  const value = unit === "fahrenheit" ? celsiusToFahrenheit(celsiusValue) : celsiusValue;
  return `${Math.round(value)}°`;
}

function setStatus(message, isError = false) {
  statusMsgEl.textContent = message;
  statusMsgEl.classList.toggle("error", isError);
}

function saveLastLocation(location) {
  localStorage.setItem(LAST_LOCATION_KEY, JSON.stringify(location));
}

function loadLastLocation() {
  const raw = localStorage.getItem(LAST_LOCATION_KEY);
  if (raw === null) return null;
  try {
    const parsed = JSON.parse(raw);
    if (parsed && typeof parsed.latitude === "number" && typeof parsed.longitude === "number") {
      return parsed;
    }
    return null;
  } catch (error) {
    console.error("Corrupted last-location data, ignoring.", error);
    return null;
  }
}

// --- GEOCODING (city name -> lat/lon) ---
async function searchCities(query) {
  const url = `${GEOCODING_URL}?name=${encodeURIComponent(query)}&count=6&language=en&format=json`;
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error(`Geocoding request failed with status ${response.status}`);
  }
  const data = await response.json();
  return data.results || [];
}

function renderSuggestions(results) {
  suggestionsEl.innerHTML = "";
  activeSuggestionIndex = -1;

  if (results.length === 0) {
    suggestionsEl.hidden = true;
    return;
  }

  results.forEach((place) => {
    const li = document.createElement("li");
    const regionParts = [place.admin1, place.country].filter(Boolean);
    li.innerHTML = `${place.name} <span class="suggestion-region">${regionParts.join(", ")}</span>`;
    li.addEventListener("click", () => selectPlace(place));
    suggestionsEl.appendChild(li);
  });

  suggestionsEl.hidden = false;
}

function hideSuggestions() {
  suggestionsEl.hidden = true;
  suggestionsEl.innerHTML = "";
  activeSuggestionIndex = -1;
}

async function selectPlace(place) {
  hideSuggestions();
  cityInput.value = `${place.name}, ${place.country}`;
  const location = {
    latitude: place.latitude,
    longitude: place.longitude,
    label: `${place.name}, ${place.country}`,
  };
  saveLastLocation(location);
  await loadWeather(location);
}

// --- FORECAST (lat/lon -> current + daily weather) ---
async function fetchForecast(latitude, longitude) {
  const params = new URLSearchParams({
    latitude: String(latitude),
    longitude: String(longitude),
    current: "temperature_2m,apparent_temperature,relative_humidity_2m,weather_code,wind_speed_10m",
    daily: "weather_code,temperature_2m_max,temperature_2m_min",
    timezone: "auto",
    forecast_days: "5",
  });
  const response = await fetch(`${FORECAST_URL}?${params.toString()}`);
  if (!response.ok) {
    throw new Error(`Forecast request failed with status ${response.status}`);
  }
  return response.json();
}

async function loadWeather(location) {
  setStatus(`Loading weather for ${location.label}...`);
  dashboardEl.hidden = true;

  try {
    const data = await fetchForecast(location.latitude, location.longitude);
    lastWeatherData = { ...data, placeLabel: location.label };
    renderWeather(lastWeatherData);
    setStatus("");
    dashboardEl.hidden = false;
  } catch (error) {
    console.error("Failed to load weather:", error);
    setStatus("Could not load weather data. Check your connection and try again.", true);
  }
}

// --- RENDER ---
function renderWeather(data) {
  const current = data.current;
  const weatherInfo = describeWeatherCode(current.weather_code);

  currentIconEl.textContent = weatherInfo.icon;
  currentTempEl.textContent = formatTemp(current.temperature_2m);
  currentPlaceEl.textContent = data.placeLabel;
  currentConditionEl.textContent = weatherInfo.label;
  currentFeelsEl.textContent = formatTemp(current.apparent_temperature);
  currentHumidityEl.textContent = `${Math.round(current.relative_humidity_2m)}%`;
  currentWindEl.textContent = `${Math.round(current.wind_speed_10m)} km/h`;

  const observedAt = new Date(current.time);
  updatedAtEl.textContent = `Updated ${observedAt.toLocaleString()} (local time for this location)`;

  renderForecast(data.daily);
}

function renderForecast(daily) {
  forecastListEl.innerHTML = "";

  daily.time.forEach((dateString, index) => {
    const code = daily.weather_code[index];
    const weatherInfo = describeWeatherCode(code);
    const date = new Date(`${dateString}T00:00:00`);
    const dayName = index === 0 ? "Today" : date.toLocaleDateString(undefined, { weekday: "short" });

    const card = document.createElement("div");
    card.className = "forecast-day";
    card.innerHTML = `
      <div class="day-name">${dayName}</div>
      <div class="day-icon">${weatherInfo.icon}</div>
      <div class="day-temps">
        <span class="day-high">${formatTemp(daily.temperature_2m_max[index])}</span>
        <span class="day-low"> / ${formatTemp(daily.temperature_2m_min[index])}</span>
      </div>
    `;
    forecastListEl.appendChild(card);
  });
}

// --- EVENTS ---
searchForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const query = cityInput.value.trim();
  if (query === "") return;

  hideSuggestions();
  setStatus(`Searching for "${query}"...`);

  try {
    const results = await searchCities(query);
    if (results.length === 0) {
      setStatus(`No city found matching "${query}". Try a different spelling.`, true);
      return;
    }
    // Use the first (best) match directly when the user hits Enter/Search
    await selectPlace(results[0]);
  } catch (error) {
    console.error("City search failed:", error);
    setStatus("Could not search for that city. Check your connection and try again.", true);
  }
});

cityInput.addEventListener("input", () => {
  const query = cityInput.value.trim();
  clearTimeout(debounceTimer);

  if (query.length < 2) {
    hideSuggestions();
    return;
  }

  // Debounce: wait for the user to pause typing before hitting the API,
  // avoiding one network request per keystroke.
  debounceTimer = setTimeout(async () => {
    try {
      const results = await searchCities(query);
      renderSuggestions(results);
    } catch (error) {
      console.error("Autocomplete search failed:", error);
      hideSuggestions();
    }
  }, 350);
});

cityInput.addEventListener("keydown", (event) => {
  const items = suggestionsEl.querySelectorAll("li");
  if (suggestionsEl.hidden || items.length === 0) return;

  if (event.key === "ArrowDown") {
    event.preventDefault();
    activeSuggestionIndex = Math.min(activeSuggestionIndex + 1, items.length - 1);
  } else if (event.key === "ArrowUp") {
    event.preventDefault();
    activeSuggestionIndex = Math.max(activeSuggestionIndex - 1, 0);
  } else if (event.key === "Escape") {
    hideSuggestions();
    return;
  } else {
    return;
  }

  items.forEach((item, index) => item.classList.toggle("highlighted", index === activeSuggestionIndex));
});

document.addEventListener("click", (event) => {
  if (!event.target.closest(".search-form")) hideSuggestions();
});

locationBtn.addEventListener("click", () => {
  if (!("geolocation" in navigator)) {
    setStatus("Geolocation is not supported in this browser.", true);
    return;
  }

  setStatus("Getting your current location...");
  navigator.geolocation.getCurrentPosition(
    async (position) => {
      const location = {
        latitude: position.coords.latitude,
        longitude: position.coords.longitude,
        label: "Your Location",
      };
      cityInput.value = "";
      saveLastLocation(location);
      await loadWeather(location);
    },
    (error) => {
      console.error("Geolocation error:", error);
      setStatus("Could not get your location. Please allow location access or search by city name instead.", true);
    }
  );
});

unitToggleBtn.addEventListener("click", () => {
  unit = unit === "celsius" ? "fahrenheit" : "celsius";
  unitToggleBtn.textContent = unit === "celsius" ? "Show in °F" : "Show in °C";
  if (lastWeatherData) renderWeather(lastWeatherData);
});

// --- STARTUP ---
// If the user has looked up a location before, load it automatically;
// otherwise show a neutral starting message.
const savedLocation = loadLastLocation();
if (savedLocation) {
  cityInput.value = savedLocation.label === "Your Location" ? "" : savedLocation.label;
  loadWeather(savedLocation);
} else {
  setStatus("Search for a city above, or use your current location, to see live weather.");
}
