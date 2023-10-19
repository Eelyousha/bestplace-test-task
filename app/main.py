import h3
import pandas as pd

from enum import Enum
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field


class GlobalValues(str, Enum):
    filename = "app/apartments.csv"
    coordinates = "coordinates"
    hexed = "hexed"
    geopos = "geopos"


class Aggr(str, Enum):
    sum = "sum"
    avg = "avg"
    min = "min"
    max = "max"


class DFField(str, Enum):
    apartments = "apartments"
    price = "price"
    year = "year"


class PolygonItem(BaseModel):
    geometry: dict = Field(
        example=[
            {
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
            }
        ]
    )
    field: DFField
    aggr: Aggr


class PointItem(BaseModel):
    geometry: dict = Field(
        example={"type": "Point", GlobalValues.coordinates: [37.517259, 55.542444]}
    )
    field: DFField
    aggr: Aggr
    r: int


app = FastAPI()


class data_frame(object):
    def __init__(self):
        df = pd.DataFrame(pd.read_csv(GlobalValues.filename))
        df[GlobalValues.hexed] = df[GlobalValues.geopos].apply(
            lambda x: coordinates_to_hex(eval(x).get(GlobalValues.coordinates))
        )

        self.df = df

    def filter_hexes_by_coordinates(self, hexes) -> pd.DataFrame:
        return self.df[self.df[GlobalValues.hexed].isin(hexes)]


def coordinates_to_hex(coords: list[float]) -> str:
    return h3.geo_to_h3(coords[1], coords[0], 11)


def aggregate_by_field(filtered_df: pd.DataFrame, field: Field, aggr: Aggr):
    match aggr:
        case Aggr.sum:
            return float(filtered_df[field].sum())
        case Aggr.avg:
            return float(filtered_df[field].mean())
        case Aggr.min:
            return filtered_df[field].min()
        case Aggr.max:
            return filtered_df[field].max()


@app.exception_handler(ValueError)
async def value_error_exception_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=400,
        content={"message": str(exc)},
    )


@app.post("/aggregate_polygon")
async def aggregate_polygon(item: PolygonItem):
    hexes_in_polygon = h3.polyfill(item.geometry, 11, True)
    filtered_df = data_frame().filter_hexes_by_coordinates(hexes_in_polygon)

    return aggregate_by_field(filtered_df, item.field, item.aggr)


@app.post("/aggregate_hex_radius")
async def aggregate_hex_radius(item: PointItem):
    hexes_in_radius = h3.k_ring(
        coordinates_to_hex(item.geometry[GlobalValues.coordinates]), item.r
    )

    filtered_df = data_frame().filter_hexes_by_coordinates(hexes_in_radius)

    return aggregate_by_field(filtered_df, item.field, item.aggr)
