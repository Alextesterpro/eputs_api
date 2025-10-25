# Incident API Tests

Comprehensive API autotests for the Incidents section based on Postman collection with Page Object Model (POM) architecture.

## 📋 Overview

This test suite provides comprehensive coverage for the Incidents API endpoints, including:
- **CRUD Operations**: Create, Read, Update, Delete incidents
- **Search & Filtering**: Advanced search with multiple criteria
- **Negative Testing**: Invalid data, security, and error scenarios
- **Performance Testing**: Response times, load testing, and concurrent requests
- **Regression Testing**: Stability and consistency checks

## 🏗️ Architecture

### Page Object Model (POM)
- **API Client**: `IncidentsAPI` - HTTP client for all incident endpoints
- **Data Models**: `IncidentData`, `IncidentListRequest`, `IncidentSearchRequest`
- **Assertions**: `IncidentAssertions` - Reusable assertion methods
- **Test Data**: `IncidentTestData` - Factory for test data generation

### Test Structure
```
test_incidents/
├── conftest.py                    # Pytest fixtures and configuration
├── test_incident_basic.py         # Basic functionality tests
├── test_incident_crud.py          # CRUD operation tests
├── test_incident_search.py        # Search and filtering tests
├── test_incident_negative.py      # Negative test scenarios
├── test_incident_performance.py   # Performance and load tests
└── README.md                      # This documentation
```

## 🚀 Quick Start

### Prerequisites
```bash
# Ensure you're in the project root
cd /path/to/DorisAutomatiomAPI

# Check environment
python run_incident_tests.py check
```

### Running Tests

#### Basic Tests (Recommended for CI/CD)
```bash
python run_incident_tests.py basic
```

#### All Tests
```bash
python run_incident_tests.py all
```

#### Specific Test Categories
```bash
# CRUD operations
python run_incident_tests.py crud

# Search functionality
python run_incident_tests.py search

# Negative scenarios
python run_incident_tests.py negative

# Performance tests
python run_incident_tests.py performance

# With reports
python run_incident_tests.py reports
```

#### Using pytest directly
```bash
# Basic tests only
pytest tests/tests_microservices/tests_incidents/test_incidents/ -m "basic or smoke" -v

# All tests
pytest tests/tests_microservices/tests_incidents/test_incidents/ -v

# Performance tests
pytest tests/tests_microservices/tests_incidents/test_incidents/ -m "performance" -v

# Negative tests
pytest tests/tests_microservices/tests_incidents/test_incidents/ -m "negative" -v
```

## 📊 Test Categories

### 🟢 Basic Tests (`@pytest.mark.basic`)
- API connectivity and authentication
- Basic CRUD operations
- Simple search and listing
- Response structure validation

### 🔥 Smoke Tests (`@pytest.mark.smoke`)
- Critical functionality verification
- API health checks
- Endpoint accessibility
- Basic data validation

### ❌ Negative Tests (`@pytest.mark.negative`)
- Invalid data scenarios
- Security testing (SQL injection, XSS)
- Boundary conditions
- Error handling validation

### ⚡ Performance Tests (`@pytest.mark.performance`)
- Response time validation
- Concurrent request handling
- Load testing
- Memory usage stability

### 🔄 Regression Tests (`@pytest.mark.regression`)
- Stability over time
- Large result set handling
- Mixed workload performance

## 🔧 Configuration

### Environment Variables
```bash
# Required
EPUTS_TOKEN=your_bearer_token_here

# Optional
API_BASE_URL=http://91.227.17.139/services/react/api
PROJECT=98_spb
SERVICE=eputs
```

### Authentication
The test suite uses a centralized authentication system:
- **Priority 1**: `EPUTS_TOKEN` environment variable
- **Priority 2**: Default token from `config/auth.py`
- **Automatic**: Token refresh and expiration handling

### Test Data
- **Fixtures**: Automatic setup and cleanup
- **Data Models**: Type-safe data structures
- **Validation**: Comprehensive response validation
- **Isolation**: Each test runs independently

## 📈 Test Coverage

### API Endpoints Covered
- `POST /incident` - Create incident
- `GET /incident/{id}` - Get incident by ID
- `PUT /incident/{id}` - Update incident
- `DELETE /incident/{id}` - Delete incident
- `POST /incident/list` - List incidents
- `POST /incident/search` - Search incidents

### Test Scenarios
- ✅ **Positive**: Valid data, successful operations
- ❌ **Negative**: Invalid data, error conditions
- 🔍 **Search**: Text search, filtering, pagination
- ⚡ **Performance**: Response times, concurrent requests
- 🔒 **Security**: Injection attacks, unauthorized access
- 🔄 **Regression**: Stability and consistency

## 🎯 Best Practices

### Test Design
- **Isolation**: Each test is independent
- **Cleanup**: Automatic resource cleanup
- **Data**: Realistic test data generation
- **Assertions**: Comprehensive validation

### Performance
- **Timeouts**: Reasonable response time limits
- **Concurrency**: Controlled concurrent requests
- **Monitoring**: Response time tracking
- **Thresholds**: Configurable performance limits

### Security
- **Input Validation**: Malicious input testing
- **Authentication**: Token validation
- **Authorization**: Permission testing
- **Data Sanitization**: XSS and injection prevention

## 📊 Reports

### HTML Report
```bash
python run_incident_tests.py reports
# Generates: reports/incident_tests_report.html
```

### Allure Report
```bash
python run_incident_tests.py reports
# Generates: reports/allure-results/
# View with: allure serve reports/allure-results
```

### Console Output
- Colored output for better readability
- Detailed error messages
- Performance metrics
- Test execution summary

## 🔍 Troubleshooting

### Common Issues

#### Authentication Errors
```bash
# Check token
echo $EPUTS_TOKEN

# Verify auth config
python -c "from config.auth import auth_manager; print(auth_manager.get_headers())"
```

#### Import Errors
```bash
# Ensure you're in project root
pwd
# Should show: /path/to/DorisAutomatiomAPI

# Check Python path
python -c "import sys; print(sys.path)"
```

#### Test Failures
```bash
# Run with verbose output
pytest tests/tests_microservices/tests_incidents/test_incidents/ -v -s

# Run specific test
pytest tests/tests_microservices/tests_incidents/test_incidents/test_incident_basic.py::TestIncidentsBasic::test_list_incidents_basic -v
```

### Debug Mode
```bash
# Enable debug logging
export PYTEST_DEBUG=1
pytest tests/tests_microservices/tests_incidents/test_incidents/ -v -s --tb=long
```

## 📚 API Reference

### IncidentsAPI Client
```python
from tests_microservices.utils.incidents.incidents_api import IncidentsAPI

# Create incident
response = IncidentsAPI.create_incident(incident_data)

# Get incident
response = IncidentsAPI.get_incident(incident_id)

# Update incident
response = IncidentsAPI.update_incident(incident_id, update_data)

# Delete incident
response = IncidentsAPI.delete_incident(incident_id)

# List incidents
response = IncidentsAPI.list_incidents(list_payload)

# Search incidents
response = IncidentsAPI.search_incidents(search_payload)
```

### Data Models
```python
from tests_microservices.utils.incidents.incident_schemas import IncidentData, IncidentListRequest

# Create incident data
incident = IncidentData(
    name="Test Incident",
    description="Test description",
    category_id=1,
    priority="high",
    status="open"
)

# Create list request
list_request = IncidentListRequest(
    page=1,
    limit=10,
    is_simple=True,
    category_id=1
)
```

### Assertions
```python
from tests_microservices.utils.incidents.incident_schemas import IncidentAssertions

# Assert incident creation
IncidentAssertions.assert_incident_created(response, incident_data)

# Assert incident retrieval
IncidentAssertions.assert_incident_retrieved(response, incident_id)

# Assert incident list
IncidentAssertions.assert_incident_list(response, expected_count=5)
```

## 🤝 Contributing

### Adding New Tests
1. Create test file in appropriate category
2. Use existing fixtures and data models
3. Follow naming conventions
4. Add appropriate markers
5. Update documentation

### Test Naming Conventions
- **Files**: `test_incident_*.py`
- **Classes**: `TestIncident*`
- **Methods**: `test_*_incident_*`
- **Markers**: Use appropriate pytest markers

### Code Quality
- **Type Hints**: Use type annotations
- **Docstrings**: Document all functions
- **Error Handling**: Comprehensive exception handling
- **Cleanup**: Always cleanup test data

## 📞 Support

For issues and questions:
1. Check this documentation
2. Review test logs and error messages
3. Verify environment configuration
4. Check API connectivity and authentication

---

**Last Updated**: 2024-01-01  
**Version**: 1.0.0  
**Status**: ✅ Production Ready
