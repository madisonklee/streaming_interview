from . import weather

def test_weather():
    assert [{"type": "snapshot", "asOf": 1672531400000, "stations": {"Foster Weather Station": {"high": 37.1, "low": 32.5}}}, {"type": "reset", "asOf": 1672531400000}] == list(weather.process_events([{"type": "sample", "stationName": "Foster Weather Station", "timestamp": 1672531200000, "temperature": 37.1}, {"type": "sample", "stationName": "Foster Weather Station", "timestamp": 1672531400000, "temperature": 32.5}, {"type": "control", "command": "snapshot"}, {"type": "control", "command": "reset"}]))

test_weather()
