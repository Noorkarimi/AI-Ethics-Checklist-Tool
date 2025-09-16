# Afghanistan Home Rental Hub

A simple Flask web application that helps landlords across Afghanistan publish their properties and allows renters to browse listings and submit rental requests.

## Features

- Showcase available homes with key information such as city, district, rent, amenities, and contact details.
- Landlords can add new listings directly from the web interface.
- Renters can select a property and send a rental inquiry to the landlord.
- Includes a couple of sample listings to demonstrate how the platform works.

## Getting Started

### Requirements

- Python 3.10+
- [Flask](https://flask.palletsprojects.com/) web framework

### Installation

1. (Optional) Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows use `.venv\\Scripts\\activate`
   ```
2. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the application

```bash
python app.py
```

Open your browser and visit `http://127.0.0.1:5000/` to view the home rental hub.

> **Note:** Listings and renter requests are kept in memory for simplicity. They will reset when the application restarts. For a production-ready solution you should connect the forms to a real database and add authentication.

## Project Structure

- `app.py` – Flask application and in-memory data storage.
- `templates/index.html` – HTML template for the user interface.
- `static/styles.css` – Styling for the application.
- `requirements.txt` – Python dependencies.

## Future Improvements

- Persist listings and requests in a database.
- Allow landlords to manage their existing listings.
- Add localization for Dari and Pashto speakers.
- Send email or SMS notifications when new rental requests are submitted.
