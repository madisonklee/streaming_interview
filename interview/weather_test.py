from . import weather

test_data1 = [
    {"type": "sample", "stationName": "Foster Weather Station", "timestamp": 1672531200000, "temperature": 37.1}, 
    {"type": "sample", "stationName": "Foster Weather Station", "timestamp": 1672531400000, "temperature": 32.5}, 
    {"type": "control", "command": "snapshot"},
    {"type": "control", "command": "reset"}
]

expected_output1 = [
    {"type": "snapshot", "asOf": 1672531400000, "stations": {"Foster Weather Station": {"high": 37.1, "low": 32.5}}},
    {"type": "reset", "asOf": 1672531400000}
]

test_data2 = [
    {"type": "control", "command": "snapshot"},
    {"type": "sample", "stationName": "Foster Weather Station", "timestamp": 1672531200000, "temperature": 37.1}, 
    {"type": "sample", "stationName": "Foster Weather Station", "timestamp": 1672531400000, "temperature": 32.5}, 
    {"type": "control", "command": "reset"}
]

expected_output2 = [
    {"type" : "snapshot", "asOf" : "No as of value available with no station data", "stations" : "No station data available for snapshot."},
    {"type": "reset", "asOf": 1672531400000}
]

test_data3 = [
    {"type": "control", "command": "reset"},
    {"type": "sample", "stationName": "Foster Weather Station", "timestamp": 1672531200000, "temperature": 37.1}, 
    {"type": "sample", "stationName": "Foster Weather Station", "timestamp": 1672531400000, "temperature": 32.5}, 
    {"type": "control", "command": "snapshot"},
]

expected_output3 = [
    {"type" : "reset", "asOf" : "No as of value available with no station data."}, 
    {"type": "snapshot", "asOf": 1672531400000, "stations": {"Foster Weather Station": {"high": 37.1, "low": 32.5}}},
]

def test_weather():
    # print output of weather.py process_events
    # print(list(weather.process_events(test_data2)))
    
    assert expected_output1 == list(weather.process_events(test_data1))
    # print("Made it past test_weather's asset")

test_weather()
