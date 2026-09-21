# Boxwise: Box Recommendation System

A Django project that recommends the cheapest shipping box for an order, based on product dimensions and weight and on box dimensions, weight capacity and cost.

## What it does
- Stores products, boxes, orders and order items (managed through the Django admin).
- Given an order, recommends the cheapest box that satisfies the selection rules below.
- Exposes the recommendation as an HTML page and as a JSON endpoint.

## Setup
```bash
python -m venv venv
venv\Scripts\activate          # Windows (macOS/Linux: source venv/bin/activate)
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## How to try it
1. Open `http://127.0.0.1:8000/admin/` and log in.
2. Add a few **Boxes** and **Products**.
3. Add an **Order**, then add **Order items** linking that order to products with quantities.
4. Note the order's id (it is in the admin URL, e.g. `/admin/boxes/order/1/change/`).
5. Open one of:
   - HTML page: `http://127.0.0.1:8000/orders/<id>/recommend/`
   - JSON: `http://127.0.0.1:8000/api/orders/<id>/recommend-box/`

Example JSON response:
```json
{
  "order": 1,
  "recommended_box": {
    "name": "Medium",
    "length": "40.00",
    "width": "30.00",
    "height": "20.00",
    "max_weight": "5.000",
    "cost": "35.00"
  }
}
```
Decimal values are returned as strings on purpose, to avoid float rounding.
If nothing fits, `recommended_box` is `null`. If the order id does not exist, the response is a 404.

## Units
Dimensions are in centimetres, weights in kilograms, and cost in rupees (₹). Box dimensions are **internal** dimensions.

## Selection rules
1. An order must contain at least one item, otherwise no box is recommended.
2. The box's maximum weight must be greater than or equal to the order's total weight.
3. Every product must fit within the box's internal dimensions, with rotation allowed (dimensions are sorted and compared in order).
4. Among the boxes that pass, the cheapest is chosen (ties are broken by id, so results are deterministic).
5. If no box passes, the result is `None`.

## Design decisions
- **DecimalField** for dimensions, weight and cost, because floats can give wrong results at exact boundaries (for example 0.1 + 0.2) and money should never be a float.
- **Packing logic lives in `boxes/packing.py`** with no Django imports, so it can be tested on its own.
- **`Order.recommend_box()`** filters boxes by weight in the database, orders them by cost, and returns the first one that passes the fit checks.
- **Both an HTML page and a JSON endpoint**: the page is for people, the JSON is for other systems. No user login or checkout was built because the assignment did not require it.
- Products in existing orders are protected from deletion (`on_delete=PROTECT`) so order history stays intact.

## Known limitations
This is a simplified version, not a true 3D bin-packing solver.
- Only one box per order is recommended. Orders that would need to be split across several boxes get no recommendation.
- No padding, stacking limits or fragile-item rules are modelled.

## Running the tests
```bash
python manage.py test
```
See `TEST_OUTPUT.md` for a recorded run.

## Project structure
```
boxwise/            project settings and root urls
boxes/
  models.py         Product, Box, Order, OrderItem, Order.recommend_box()
  packing.py        fits_in_box()
  views.py          JSON endpoint and HTML page
  urls.py
  templates/boxes/result.html
  tests/            unit and view tests
```

## Possible future improvements
- Layer-based or other packing heuristic for multi-item orders.
- Splitting an order across several boxes.
- An API endpoint to create orders.

## AI usage
See `AI_USAGE.md`.
