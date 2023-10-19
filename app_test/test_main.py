import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient
import pandas as pd
from app.main import app

client = TestClient(app)


class APITest(unittest.TestCase):
    @patch("app.main.pd.read_csv")
    def test_aggregate_polygon(self, mock_read_csv):
        mock_read_csv.return_value = pd.DataFrame(
            {
                "geopos": pd.Series(
                    [
                        "{'type': 'Point', 'coordinates': [37.510331, 55.542905]}",
                        "{'type': 'Point', 'coordinates': [37.511544, 55.543516]}",
                        "{'type': 'Point', 'coordinates': [37.516422, 55.544148]}",
                        "{'type': 'Point', 'coordinates': [37.516323, 55.542936]}",
                        "{'type': 'Point', 'coordinates': [37.516494, 55.543633]}",
                        "{'type': 'Point', 'coordinates': [37.517949, 55.543628]}",
                        "{'type': 'Point', 'coordinates': [37.518282, 55.542767]}",
                        "{'type': 'Point', 'coordinates': [37.519737, 55.54263]}",
                    ]
                ),
                "price": pd.Series(
                    [
                        280734.0,
                        273883.0,
                        253490.0,
                        250847.0,
                        223698.0,
                        183780.0,
                        223536.0,
                        293412.0,
                    ]
                ),
            }
        )
        response = client.post(
            "/aggregate_polygon",
            json={
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [37.520123, 55.54413],
                            [37.515671, 55.54399],
                            [37.514662, 55.541793],
                            [37.521218, 55.542612],
                            [37.520123, 55.54413],
                        ]
                    ],
                },
                "field": "price",
                "aggr": "avg",
            },
        )
        assert float(response.text) == 235054.6
        assert response.status_code == 200

        mock_read_csv.return_value = pd.DataFrame(
            {
                "geopos": pd.Series(
                    [
                        "{'type': 'Point', 'coordinates': [37.510331, 55.542905]}",
                        "{'type': 'Point', 'coordinates': [37.511544, 55.543516]}",
                        "{'type': 'Point', 'coordinates': [37.516422, 55.544148]}",
                        "{'type': 'Point', 'coordinates': [37.516323, 55.542936]}",
                        "{'type': 'Point', 'coordinates': [37.516494, 55.543633]}",
                        "{'type': 'Point', 'coordinates': [37.517949, 55.543628]}",
                        "{'type': 'Point', 'coordinates': [37.518282, 55.542767]}",
                        "{'type': 'Point', 'coordinates': [37.519737, 55.54263]}",
                    ]
                ),
                "apartments": pd.Series(
                    [
                        118,
                        311,
                        132,
                        175,
                        69,
                        95,
                        263,
                        169,
                    ]
                ),
            }
        )

        response = client.post(
            "/aggregate_hex_radius",
            json={
                "geometry": {"type": "Point", "coordinates": [37.517259, 55.542444]},
                "field": "apartments",
                "aggr": "sum",
                "r": 4,
            },
        )

        assert float(response.text) == 903.0
        assert response.status_code == 200

    @patch("app.main.pd.read_csv")
    def test_aggregate_hex_radius(self, mock_read_csv):
        mock_read_csv.return_value = pd.DataFrame(
            {
                "geopos": pd.Series(
                    [
                        "{'type': 'Point', 'coordinates': [37.510331, 55.542905]}",
                        "{'type': 'Point', 'coordinates': [37.511544, 55.543516]}",
                        "{'type': 'Point', 'coordinates': [37.516422, 55.544148]}",
                        "{'type': 'Point', 'coordinates': [37.516323, 55.542936]}",
                        "{'type': 'Point', 'coordinates': [37.516494, 55.543633]}",
                        "{'type': 'Point', 'coordinates': [37.517949, 55.543628]}",
                        "{'type': 'Point', 'coordinates': [37.518282, 55.542767]}",
                        "{'type': 'Point', 'coordinates': [37.519737, 55.54263]}",
                    ]
                ),
                "apartments": pd.Series(
                    [
                        118,
                        311,
                        132,
                        175,
                        69,
                        95,
                        263,
                        169,
                    ]
                ),
            }
        )

        response = client.post(
            "/aggregate_hex_radius",
            json={
                "geometry": {"type": "Point", "coordinates": [37.517259, 55.542444]},
                "field": "apartments",
                "aggr": "sum",
                "r": 4,
            },
        )

        assert float(response.text) == 903.0
        assert response.status_code == 200
