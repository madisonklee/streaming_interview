from typing import Any, Iterable, Generator
# station_data will look like - { "Foster Weather Station" : { "most_recent_timestamp" :  "2022-01-01 00:00:00", "temp_list" : [13, 25.5, 30, 23.5] } }
# Input: events, an iterable where each item is a dictionary with string keys and value Any type
# Output: returns a generator that yields dictionaries with string keys and any type of value
def process_events(events: Iterable[dict[str, Any]]) -> Generator[dict[str, Any], None, None]:
    station_data = {}   # aggregated data from each station    
    for event in events:
        as_of = max((station['most_recent_timestamp'] for station in station_data.values()), default=None)    
        if event["type"] == "sample":   # PROCESS SAMPLE MSG
            station_name = event.get("stationName")
            timestamp = event.get("timestamp")
            temp = event.get("temperature")
            # UPDATE STATION_DATA w/ new sample data
            if station_name not in station_data:    # APPEND
                station_data[station_name] = {
                    "most_recent_timestamp" : timestamp,
                    "temp_list" : [temp]
                }
            else:       # UPDATE w/ new temp + new timestamp
                station_data[station_name]["most_recent_timestamp"] = timestamp
                station_data[station_name]["temp_list"].append(temp)
        elif  event["type"] == "control":   # PROCESS CONTROL MSG SNAPSHOT
            if event.get("command") == "snapshot":
                if not station_data:       # if station_data is empty
                    yield {
                        "type" : "snapshot",
                        "asOf" : "No as of value available with no station data",
                        "stations" : "No station data available for snapshot."
                    }
                else:       # station_data exists --> build out snapshot
                    stations = {}
                    for station_name, info in station_data.items():
                        high = max(info["temp_list"])  # get high
                        low = min(info["temp_list"])   # get low
                        # append to stations
                        stations[station_name] = {"high": high, "low": low}
                    snapshot =  {
                        "type" : "snapshot",
                        "asOf" : as_of,
                        "stations" : stations
                    }
                    yield snapshot
            elif event.get("command") == "reset":   # PROCESS CONTROL MSG RESET
                if not station_data:    # if station_data is empty
                    yield {
                        "type" : "reset",
                        "asOf" : "No as of value available with no station data."
                    }
                else:   # reset the aggregated state
                    station_data.clear()
                    reset = {       # return confirmation message
                        "type" : "reset",
                        "asOf" : as_of
                    }
                    yield reset
            else:   # raise an informative exception
                raise ValueError(f"Unknown Command in Control Message: {event['command']}")
        else:       # then throw exception
            raise ValueError(f"Unknown Type of Message: {event['type']}")
