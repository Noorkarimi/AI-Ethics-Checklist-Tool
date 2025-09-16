from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
import itertools

from flask import Flask, render_template, request

app = Flask(__name__)

_listing_id_counter = itertools.count(1)


@dataclass
class RentalListing:
    id: int
    title: str
    city: str
    district: str
    monthly_rent: int
    bedrooms: int
    bathrooms: int
    amenities: List[str]
    description: str
    contact_name: str
    contact_phone: str
    contact_email: str
    created_at: datetime = field(default_factory=datetime.utcnow)

    @property
    def rent_display(self) -> str:
        return f"{self.monthly_rent:,} AFN"


@dataclass
class RentalRequest:
    listing_id: int
    renter_name: str
    renter_phone: str
    renter_email: str
    message: str
    move_in_date: str
    created_at: datetime = field(default_factory=datetime.utcnow)


listings: List[RentalListing] = [
    RentalListing(
        id=next(_listing_id_counter),
        title="Sunny Apartment in Kabul",
        city="Kabul",
        district="Shahr-e Naw",
        monthly_rent=35000,
        bedrooms=2,
        bathrooms=1,
        amenities=["Electricity", "Running Water", "Internet"],
        description="Bright 2-bedroom apartment close to markets and public transport.",
        contact_name="Ahmad Khan",
        contact_phone="+93 700 123 456",
        contact_email="ahmad@example.com",
    ),
    RentalListing(
        id=next(_listing_id_counter),
        title="Family House near Herat Bazaar",
        city="Herat",
        district="Jibril",
        monthly_rent=28000,
        bedrooms=3,
        bathrooms=2,
        amenities=["Electricity", "Running Water", "Back-up Generator"],
        description="Spacious family home with a private courtyard and nearby schools.",
        contact_name="Fatima Rahimi",
        contact_phone="+93 799 987 654",
        contact_email="fatima@example.com",
    ),
]

rental_requests: List[RentalRequest] = []


def _parse_int(value: str, field_name: str, errors: List[str]) -> Optional[int]:
    try:
        parsed = int(value)
    except ValueError:
        errors.append(f"{field_name} must be a whole number.")
        return None
    if parsed <= 0:
        errors.append(f"{field_name} must be greater than zero.")
        return None
    return parsed


def _find_listing(listing_id: int) -> Optional[RentalListing]:
    for listing in listings:
        if listing.id == listing_id:
            return listing
    return None


def _handle_create_listing(form, errors: List[str]) -> Optional[str]:
    title = form.get("title", "").strip()
    if not title:
        errors.append("Please provide a title for your listing.")

    city = form.get("city", "").strip()
    if not city:
        errors.append("Please include the city where the property is located.")

    district = form.get("district", "").strip()
    if not district:
        errors.append("Please include the district or neighborhood name.")

    monthly_rent_raw = form.get("monthly_rent", "").strip()
    if not monthly_rent_raw:
        errors.append("Monthly rent is required.")
        monthly_rent = None
    else:
        monthly_rent = _parse_int(monthly_rent_raw, "Monthly rent", errors)

    bedrooms_raw = form.get("bedrooms", "").strip()
    if not bedrooms_raw:
        errors.append("Please specify the number of bedrooms.")
        bedrooms = None
    else:
        bedrooms = _parse_int(bedrooms_raw, "Bedrooms", errors)

    bathrooms_raw = form.get("bathrooms", "").strip()
    if not bathrooms_raw:
        errors.append("Please specify the number of bathrooms.")
        bathrooms = None
    else:
        bathrooms = _parse_int(bathrooms_raw, "Bathrooms", errors)

    amenities = [amenity for amenity in form.getlist("amenities") if amenity]

    description = form.get("description", "").strip()
    if not description:
        errors.append("Please add a short description of the property.")

    contact_name = form.get("contact_name", "").strip()
    if not contact_name:
        errors.append("Please include the contact person's name.")

    contact_phone = form.get("contact_phone", "").strip()
    if not contact_phone:
        errors.append("Please include a phone number for renters to reach you.")

    contact_email = form.get("contact_email", "").strip()

    if errors:
        return None

    listing = RentalListing(
        id=next(_listing_id_counter),
        title=title,
        city=city,
        district=district,
        monthly_rent=monthly_rent if monthly_rent is not None else 0,
        bedrooms=bedrooms if bedrooms is not None else 0,
        bathrooms=bathrooms if bathrooms is not None else 0,
        amenities=amenities,
        description=description,
        contact_name=contact_name,
        contact_phone=contact_phone,
        contact_email=contact_email,
    )
    listings.insert(0, listing)
    return "Your property has been listed successfully! Renters can now view it below."


def _handle_rental_request(form, errors: List[str]) -> Optional[str]:
    listing: Optional[RentalListing] = None

    listing_id_raw = form.get("listing_id", "").strip()
    if not listing_id_raw:
        errors.append("Please select a property you want to rent.")
    else:
        try:
            listing_id = int(listing_id_raw)
        except ValueError:
            errors.append("Invalid property selected. Please choose again.")
        else:
            listing = _find_listing(listing_id)
            if listing is None:
                errors.append("The selected property could not be found.")

    renter_name = form.get("renter_name", "").strip()
    if not renter_name:
        errors.append("Please provide your full name.")

    renter_phone = form.get("renter_phone", "").strip()
    if not renter_phone:
        errors.append("Please include a phone number so the landlord can reach you.")

    renter_email = form.get("renter_email", "").strip()

    message = form.get("message", "").strip()
    if not message:
        errors.append("Add a short note to let the landlord know why you're interested.")

    move_in_date = form.get("move_in_date", "").strip()

    if errors or listing is None:
        return None

    rental_requests.append(
        RentalRequest(
            listing_id=listing.id,
            renter_name=renter_name,
            renter_phone=renter_phone,
            renter_email=renter_email,
            message=message,
            move_in_date=move_in_date,
        )
    )

    return f"Your request for {listing.title} has been sent to {listing.contact_name}."


@app.route('/', methods=['GET', 'POST'])
def index():
    success_message: Optional[str] = None
    errors: List[str] = []

    if request.method == 'POST':
        form_type = request.form.get('form_type')
        if form_type == 'create_listing':
            message = _handle_create_listing(request.form, errors)
            if message:
                success_message = message
        elif form_type == 'rental_request':
            message = _handle_rental_request(request.form, errors)
            if message:
                success_message = message

    inquiry_counts = {
        listing.id: sum(1 for request_obj in rental_requests if request_obj.listing_id == listing.id)
        for listing in listings
    }

    return render_template(
        'index.html',
        listings=listings,
        success_message=success_message,
        errors=errors,
        inquiry_counts=inquiry_counts,
    )


if __name__ == '__main__':
    app.run(debug=True)
