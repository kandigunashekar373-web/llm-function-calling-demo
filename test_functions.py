from app.functions import calculator, draft_email, get_weather, schedule_meeting

def test_calculator():
    assert calculator("25 * 8")["result"] == 200

def test_email():
    assert draft_email("a@example.com", "Hello", "Test")["status"] == "draft_created"

def test_meeting():
    assert schedule_meeting("Review", "2026-07-20", "3 PM")["status"] == "mock_meeting_created"

def test_weather():
    assert get_weather("Chicago")["status"] == "mock_weather"
