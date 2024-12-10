import numpy as np
import pandas as pd


def does_contain_street_name(bus_stop, streets):
    for street_name in streets:
        if street_name[:-1] in bus_stop:
            return True
    return False


df_bus_stops = pd.read_csv("data/bus_stops.csv")["bus_stop"]
df_streets = pd.read_csv("data/streets.csv")["street"]

street_candidates = df_streets[df_streets.str.endswith("通")].values

bus_stops_containing_intersection = df_bus_stops[
    df_bus_stops.apply(
        lambda bus_stop: does_contain_street_name(bus_stop, street_candidates)
    )
]

bus_stops_containing_intersection.to_csv(
    "data/bus_stops_containing_intersection.csv", index=False
)
