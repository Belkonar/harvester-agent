import unittest
import parsers

class JsonParserTests(unittest.TestCase):
    def test_basics(self):
        json_data = """
{
  "restaurant": {
    "id": "rest_12345",
    "name": "The Golden Fork",
    "cuisine": "Contemporary American",
    "locations": [
      {
        "address": "123 Main St",
        "city": "Boston",
        "state": null,
        "coordinates": {
          "latitude": 42.3601,
          "longitude": -71.0589
        },
        "seating_capacity": 85
      }
    ],
    "menu_items": [
      {
        "name": "Truffle Mac & Cheese",
        "price": 18.99,
        "categories": [
          "pasta",
          "vegetarian"
        ],
        "allergens": [
          "dairy",
          "gluten"
        ],
        "available": true
      }
    ],
    "ratings": {
      "overall": 4.5,
      "service": 4.7,
      "ambiance": 4.3,
      "food": 4.6
    }
  }
}
        """

        data = parsers.scan(json_data)
        
        self.assertIn("object", data[""])
        self.assertIn("str", data[".restaurant.id"])
        self.assertIn("nonetype", data[".restaurant.locations[].state"])
        self.assertIn("array", data[".restaurant.locations"])
        self.assertIn("float", data[".restaurant.locations[].coordinates.latitude"])
        self.assertIn("boolean", data[".restaurant.menu_items[].available"])


    def test_adt(self):
        json_data = """
{
  "name": "Mixed Array Example",
  "description": "Array with different data types",
  "mixed_array": [
    42,
    "Hello World",
    {
      "key": "value",
      "active": true
    }
  ]
}
        """

        data = parsers.scan(json_data)

        self.assertIn("object", data[""])

        self.assertIn("str", data[".mixed_array[]"])
        self.assertIn("object", data[".mixed_array[]"])
        self.assertIn("int", data[".mixed_array[]"])
        self.assertIn("str", data[".mixed_array[].key"])


