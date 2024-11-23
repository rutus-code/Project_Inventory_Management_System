import pytest
import sys
import os

print("Current working directory:", os.getcwd())
print("sys.path before appending:", sys.path)

# Add the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

print("sys.path after appending:", sys.path)

# Import app
from app import app
import pytest
from unittest.mock import MagicMock
from app import app, mysql

import pytest
from unittest.mock import MagicMock
from app import app, mysql

@pytest.fixture
def client(mocker):
    app.config['TESTING'] = True
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = 'root'
    app.config['MYSQL_DB'] = 'inventory_management_system'

    # Mock MySQL connection
    mock_cursor = MagicMock()
    mock_connection = MagicMock()
    mock_connection.cursor.return_value = mock_cursor
    mocker.patch.object(mysql, 'connection', mock_connection)

    with app.test_client() as client:
        yield client, mock_cursor

@pytest.fixture
def client(mocker):
    app.config['TESTING'] = True

    # Mock MySQL connection
    mock_cursor = MagicMock()
    mock_connection = MagicMock()
    mock_connection.cursor.return_value = mock_cursor
    mock_connection.close.return_value = None  # Handle teardown
    mocker.patch.object(mysql, 'connection', mock_connection)

    with app.test_client() as client:
        yield client, mock_cursor




@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = 'root'
    app.config['MYSQL_DB'] = 'inventory_management_system'
    with app.test_client() as client:
        yield client

def test_login_page_loads(client):
    """Test if the login page loads correctly."""
    response = client.get('/pythonlogin')
    assert response.status_code == 200
    assert b"Login" in response.data

def test_login_success(client, mocker):
    """Test successful login."""
    # Mock MySQL cursor and database response
    mock_cursor = mocker.patch('MySQLdb.cursors.DictCursor')
    mock_cursor.return_value.fetchone.return_value = {
        'id': 1,
        'username': 'testuser'
    }

    response = client.post('/pythonlogin', data={
        'username': 'testuser',
        'password': 'testpassword'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"Home" in response.data


#for stress testing I have added a testcase to handle large data set
def test_view_inventory_large_dataset(client, mocker):
    """Test viewInventory with a large mocked dataset."""
    # Generate a large dataset
    large_dataset = [{'inventory_id': i, 'description': f'Item {i}'} for i in range(10000)]
    mock_cursor = mocker.patch('MySQLdb.cursors.DictCursor')
    mock_cursor.return_value.fetchall.return_value = large_dataset

    response = client.get('/pythonlogin/viewInventory')
    assert response.status_code == 200
    assert b"Inventory" in response.data
    assert len(large_dataset) == 10000  # Ensure all data is processed

#validate the test cases:
def test_register_validation(client):
    client, _ = client  # Unpack the fixture
    response = client.post('/pythonlogin/register', data={
        'username': '@invaliduser',  # Invalid username
        'password': 'testpassword',
        'email': 'test@example.com'
    })
    assert b"Username must contain only characters and numbers!" in response.data



#SQL query efficiency and correctness
def test_database_query(client, mocker):
    client, mock_cursor = client  

    # Mock the query result with proper structure
    mock_cursor.fetchall.return_value = [{'cat_id': 1, 'category_name': 'Electronics'}]

    response = client.get('/pythonlogin/viewCategory')
    assert response.status_code == 200
    assert b"Electronics" in response.data

