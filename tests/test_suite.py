from unittest.mock import MagicMock, patch

from monitor_app.main import SystemRecord


# Test Initialization
def test_initialization(app_instance):
    assert app_instance.is_recording is False
    assert app_instance.update_interval == 1000
    assert app_instance.start_time is None


# Test Update Statistics
@patch("psutil.cpu_percent", return_value=25.0)
@patch("psutil.virtual_memory")
@patch("psutil.disk_usage")
def test_update_stats(mock_disk, mock_memory, mock_cpu, app_instance):
    mock_memory.return_value = MagicMock(available=8 * 1024**3, total=16 * 1024**3)
    mock_disk.return_value = MagicMock(free=200 * 1024**3, total=500 * 1024**3)
    
    app_instance.update_stats()
    
    assert app_instance.cpu_label.config()['text'][-1] == "CPU: 25.0%"
    assert "8.0GB/16GB" in app_instance.ram_label.config()['text'][-1]
    assert "200.0GB/500GB" in app_instance.storage_label.config()['text'][-1]


# Test Start Recording
def test_start_recording(app_instance):
    with patch("time.time", return_value=1000):
        app_instance.start_recording()
    
    assert app_instance.is_recording is True
    assert app_instance.start_time == 1000


# Test Stop Recording
def test_stop_recording(app_instance):
    app_instance.start_button.grid = MagicMock()
    app_instance.stop_button.grid_remove = MagicMock()
    app_instance.is_recording = True
    app_instance.stop_recording()
    
    assert app_instance.is_recording is False
    assert app_instance.start_button.grid.assert_called_once
    assert app_instance.stop_button.grid_remove.assert_called_once


# Test Data Recording
def test_record_data(app_instance, test_db):
    app_instance.record_data(25.0, 50.0, 30.0)
    
    records = test_db.query(SystemRecord).all()
    assert len(records) == 1
    record = records[0]
    assert record.cpu_load == 25.0
    assert record.ram_load == 50.0
    assert record.storage_load == 30.0


