from typing import Any, Iterable, Generator

'''
station_data will look something like this: 

{
    "Foster Weather Station" : {
        "most_recent_timestamp" :  "2022-01-01 00:00:00",
        "temp_list" : [13, 25.5, 30, 23.5]
    }
}
'''

# Input: events, an iterable where each item is a dictionary with string keys and value Any type
# Output: returns a generator that yields dictionaries with string keys and any type of value
def process_events(events: Iterable[dict[str, Any]]) -> Generator[dict[str, Any], None, None]:
    station_data = {}   # aggregated data from each station
    
    for event in events:
        asOf = retrieve_asOf(station_data) if station_data else None
        
        # PROCESS SAMPLE MSG    
        if event["type"] == "sample":
            # process weather sample data
            station_name = event.get("stationName")
            timestamp = event.get("timestamp")
            temp = event.get("temperature")
            
            # update station_data with new sample
            if station_name not in station_data:    # APPEND
                station_data[station_name] = {
                    "most_recent_timestamp" : timestamp,
                    "temp_list" : [temp]
                }
            else:       # UPDATE w/ new temp + new timestamp
                station_data[station_name]["most_recent_timestamp"] = timestamp
                station_data[station_name]["temp_list"].append(temp)
                
        # CONTROL MESSAGES - snapshot and reset
        elif  event["type"] == "control":
            # PROCESS CONTROL MSG SNAPSHOT
            if event.get("command") == "snapshot":
                # if station_data is empty (aka if first message it receives is a control message)
                if not station_data:
                    yield {
                        "type" : "snapshot",
                        "asOf" : "No as of value available with no station data",
                        "stations" : "No station data available for snapshot."
                    }
                else:       # station_data exists
                    # build out stations dictionary for return value
                    stations = {}
                    for station in station_data:
                        high = max(station_data[station]["temp_list"])  # get high
                        low = min(station_data[station]["temp_list"])   # get low
                        
                        # append to stations
                        stations[station] = {"high": high, "low": low}
                        
                    snapshot =  {
                        "type" : "snapshot",
                        "asOf" : asOf,
                        "stations" : stations
                    }
                    
                    yield snapshot
                
            # PROCESS CONTROL MSG RESET
            elif event.get("command") == "reset":
                # if station_data is empty (aka if first message it receives is a control message)
                if not station_data:
                    yield {
                        "type" : "reset",
                        "asOf" : "No as of value available with no station data."
                    }
                else:
                    # reset the aggregated state
                    station_data.clear()
                    
                    # return confirmation message
                    reset = {
                        "type" : "reset",
                        "asOf" : asOf
                    }
                    
                    yield reset
            
            # If the program encounters an unknown message type, it should raise an informative exception
            else:   
                raise ValueError(f"Unknown Command in Control Message (not snapshot or reset): {event['command']}")
        
        else:       # then throw exception
            raise ValueError(f"Unknown Type of Message (not sample or control): {event['type']}")

# Input: station_data dictionary of dictionaries
# Output: returns the most recent timestamp out of all stations
def retrieve_asOf(station_data):
    most_recent_timestamp = None
    
    for curr_station in  station_data.values():
        # get current station's timestamp
        current_timestamp = curr_station['most_recent_timestamp']
        
        # update return val if this is most recent
        if (most_recent_timestamp is None) or (current_timestamp > most_recent_timestamp):
            most_recent_timestamp =  current_timestamp
        
    return most_recent_timestamp