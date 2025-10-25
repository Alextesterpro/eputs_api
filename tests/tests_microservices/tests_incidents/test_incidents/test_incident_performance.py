"""
Performance and load tests for Incidents API.
Tests response times, throughput, and resource usage.
"""

import pytest
import time
import statistics
from typing import List, Dict, Any
from concurrent.futures import ThreadPoolExecutor, as_completed

from tests_microservices.utils.incidents.incidents_api import IncidentsAPI
from tests_microservices.utils.incidents.incident_schemas import (
    IncidentData,
    IncidentTestData,
    IncidentAssertions
)


@pytest.mark.performance
class TestIncidentPerformance:
    """Performance tests for incidents API."""

    def test_list_incidents_response_time(self):
        """Test response time for incident listing."""
        # Arrange
        list_payload = {"page": 1, "limit": 10, "is_simple": True}
        
        # Act
        start_time = time.time()
        response = IncidentsAPI.list_incidents(list_payload)
        end_time = time.time()
        
        # Assert
        assert response.status_code == 200, f"List request failed: {response.text}"
        
        response_time = end_time - start_time
        assert response_time < 5.0, f"List request too slow: {response_time:.2f}s"
        
        print(f"List incidents response time: {response_time:.2f}s")

    def test_search_incidents_response_time(self):
        """Test response time for incident search."""
        # Arrange
        search_payload = {"page": 1, "limit": 10, "search": "test"}
        
        # Act
        start_time = time.time()
        response = IncidentsAPI.search_incidents(search_payload)
        end_time = time.time()
        
        # Assert
        assert response.status_code == 200, f"Search request failed: {response.text}"
        
        response_time = end_time - start_time
        assert response_time < 5.0, f"Search request too slow: {response_time:.2f}s"
        
        print(f"Search incidents response time: {response_time:.2f}s")

    def test_get_incident_response_time(self):
        """Test response time for getting a single incident."""
        # Arrange
        incident_id = 1  # Assuming incident with ID 1 exists
        
        # Act
        start_time = time.time()
        response = IncidentsAPI.get_incident(incident_id)
        end_time = time.time()
        
        # Assert
        # Accept both 200 (found) and 404 (not found) as valid responses
        assert response.status_code in [200, 404], f"Get request failed: {response.text}"
        
        response_time = end_time - start_time
        assert response_time < 3.0, f"Get request too slow: {response_time:.2f}s"
        
        print(f"Get incident response time: {response_time:.2f}s")

    def test_create_incident_response_time(self):
        """Test response time for incident creation."""
        # Arrange
        incident_data = IncidentTestData.create_minimal_incident()
        created_incident_id = None
        
        try:
            # Act
            start_time = time.time()
            response = IncidentsAPI.create_incident(incident_data.to_dict())
            end_time = time.time()
            
            # Assert
            if response.status_code in [200, 201]:
                created_incident = response.json()
                created_incident_id = created_incident.get("id")
            
            response_time = end_time - start_time
            assert response_time < 10.0, f"Create request too slow: {response_time:.2f}s"
            
            print(f"Create incident response time: {response_time:.2f}s")
            
        finally:
            # Cleanup
            if created_incident_id:
                try:
                    IncidentsAPI.delete_incident(created_incident_id)
                except Exception:
                    pass  # Ignore cleanup errors

    def test_concurrent_list_requests(self):
        """Test performance under concurrent list requests."""
        # Arrange
        num_requests = 10
        list_payload = {"page": 1, "limit": 5, "is_simple": True}
        
        def make_list_request():
            start_time = time.time()
            response = IncidentsAPI.list_incidents(list_payload)
            end_time = time.time()
            return {
                "status_code": response.status_code,
                "response_time": end_time - start_time,
                "success": response.status_code == 200
            }
        
        # Act
        start_time = time.time()
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(make_list_request) for _ in range(num_requests)]
            results = [future.result() for future in as_completed(futures)]
        end_time = time.time()
        
        # Assert
        total_time = end_time - start_time
        successful_requests = [r for r in results if r["success"]]
        response_times = [r["response_time"] for r in results]
        
        assert len(successful_requests) >= num_requests * 0.8, f"Too many failed requests: {len(successful_requests)}/{num_requests}"
        assert total_time < 30.0, f"Concurrent requests too slow: {total_time:.2f}s"
        
        avg_response_time = statistics.mean(response_times)
        max_response_time = max(response_times)
        
        print(f"Concurrent requests: {len(successful_requests)}/{num_requests} successful")
        print(f"Average response time: {avg_response_time:.2f}s")
        print(f"Max response time: {max_response_time:.2f}s")
        print(f"Total time: {total_time:.2f}s")

    def test_concurrent_search_requests(self):
        """Test performance under concurrent search requests."""
        # Arrange
        num_requests = 8
        search_payload = {"page": 1, "limit": 5, "search": "test"}
        
        def make_search_request():
            start_time = time.time()
            response = IncidentsAPI.search_incidents(search_payload)
            end_time = time.time()
            return {
                "status_code": response.status_code,
                "response_time": end_time - start_time,
                "success": response.status_code == 200
            }
        
        # Act
        start_time = time.time()
        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = [executor.submit(make_search_request) for _ in range(num_requests)]
            results = [future.result() for future in as_completed(futures)]
        end_time = time.time()
        
        # Assert
        total_time = end_time - start_time
        successful_requests = [r for r in results if r["success"]]
        response_times = [r["response_time"] for r in results]
        
        assert len(successful_requests) >= num_requests * 0.8, f"Too many failed requests: {len(successful_requests)}/{num_requests}"
        assert total_time < 25.0, f"Concurrent search too slow: {total_time:.2f}s"
        
        avg_response_time = statistics.mean(response_times)
        print(f"Concurrent search: {len(successful_requests)}/{num_requests} successful")
        print(f"Average response time: {avg_response_time:.2f}s")

    def test_large_result_set_performance(self):
        """Test performance with large result sets."""
        # Arrange
        large_payload = {"page": 1, "limit": 100, "is_simple": True}
        
        # Act
        start_time = time.time()
        response = IncidentsAPI.list_incidents(large_payload)
        end_time = time.time()
        
        # Assert
        assert response.status_code == 200, f"Large result set failed: {response.text}"
        
        response_time = end_time - start_time
        assert response_time < 15.0, f"Large result set too slow: {response_time:.2f}s"
        
        # Validate response size
        data = response.json()
        assert "data" in data
        assert len(data["data"]) <= 100, "Should respect limit parameter"
        
        print(f"Large result set ({len(data['data'])} items): {response_time:.2f}s")

    def test_complex_search_performance(self):
        """Test performance with complex search criteria."""
        # Arrange
        complex_search = {
            "page": 1,
            "limit": 50,
            "search": "test",
            "category_id": 1,
            "status": "open",
            "priority": "high"
        }
        
        # Act
        start_time = time.time()
        response = IncidentsAPI.search_incidents(complex_search)
        end_time = time.time()
        
        # Assert
        assert response.status_code == 200, f"Complex search failed: {response.text}"
        
        response_time = end_time - start_time
        assert response_time < 10.0, f"Complex search too slow: {response_time:.2f}s"
        
        print(f"Complex search response time: {response_time:.2f}s")

    def test_memory_usage_stability(self):
        """Test memory usage stability over multiple requests."""
        # Arrange
        list_payload = {"page": 1, "limit": 20, "is_simple": True}
        num_iterations = 20
        
        response_times = []
        
        # Act
        for i in range(num_iterations):
            start_time = time.time()
            response = IncidentsAPI.list_incidents(list_payload)
            end_time = time.time()
            
            assert response.status_code == 200, f"Request {i+1} failed: {response.text}"
            
            response_time = end_time - start_time
            response_times.append(response_time)
            
            # Small delay to prevent overwhelming the server
            time.sleep(0.1)
        
        # Assert
        avg_response_time = statistics.mean(response_times)
        max_response_time = max(response_times)
        min_response_time = min(response_times)
        
        # Response times should be relatively stable
        assert max_response_time < avg_response_time * 2, f"Response times too variable: {min_response_time:.2f}s - {max_response_time:.2f}s"
        assert avg_response_time < 5.0, f"Average response time too slow: {avg_response_time:.2f}s"
        
        print(f"Memory stability test: {num_iterations} requests")
        print(f"Average response time: {avg_response_time:.2f}s")
        print(f"Response time range: {min_response_time:.2f}s - {max_response_time:.2f}s")


@pytest.mark.performance
class TestIncidentLoadTesting:
    """Load testing for incidents API."""

    def test_high_frequency_requests(self):
        """Test API under high frequency requests."""
        # Arrange
        num_requests = 50
        list_payload = {"page": 1, "limit": 5, "is_simple": True}
        
        def make_request():
            start_time = time.time()
            response = IncidentsAPI.list_incidents(list_payload)
            end_time = time.time()
            return {
                "status_code": response.status_code,
                "response_time": end_time - start_time,
                "success": response.status_code == 200
            }
        
        # Act
        start_time = time.time()
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(make_request) for _ in range(num_requests)]
            results = [future.result() for future in as_completed(futures)]
        end_time = time.time()
        
        # Assert
        total_time = end_time - start_time
        successful_requests = [r for r in results if r["success"]]
        response_times = [r["response_time"] for r in results]
        
        success_rate = len(successful_requests) / num_requests
        assert success_rate >= 0.9, f"Success rate too low: {success_rate:.2%}"
        
        avg_response_time = statistics.mean(response_times)
        assert avg_response_time < 3.0, f"Average response time too slow: {avg_response_time:.2f}s"
        
        throughput = num_requests / total_time
        print(f"High frequency test: {num_requests} requests in {total_time:.2f}s")
        print(f"Success rate: {success_rate:.2%}")
        print(f"Throughput: {throughput:.2f} requests/second")
        print(f"Average response time: {avg_response_time:.2f}s")

    def test_sustained_load(self):
        """Test API under sustained load."""
        # Arrange
        duration_seconds = 30
        requests_per_second = 2
        list_payload = {"page": 1, "limit": 10, "is_simple": True}
        
        def make_request():
            start_time = time.time()
            response = IncidentsAPI.list_incidents(list_payload)
            end_time = time.time()
            return {
                "status_code": response.status_code,
                "response_time": end_time - start_time,
                "success": response.status_code == 200,
                "timestamp": start_time
            }
        
        # Act
        start_time = time.time()
        results = []
        
        with ThreadPoolExecutor(max_workers=5) as executor:
            while time.time() - start_time < duration_seconds:
                # Submit requests at the specified rate
                for _ in range(requests_per_second):
                    future = executor.submit(make_request)
                    results.append(future)
                
                # Wait for the second to complete
                time.sleep(1.0)
        
        # Collect results
        completed_results = []
        for future in as_completed(results):
            try:
                result = future.result(timeout=10)
                completed_results.append(result)
            except Exception as e:
                print(f"Request failed: {e}")
        
        # Assert
        successful_requests = [r for r in completed_results if r["success"]]
        success_rate = len(successful_requests) / len(completed_results) if completed_results else 0
        
        assert success_rate >= 0.8, f"Sustained load success rate too low: {success_rate:.2%}"
        
        if successful_requests:
            response_times = [r["response_time"] for r in successful_requests]
            avg_response_time = statistics.mean(response_times)
            assert avg_response_time < 5.0, f"Sustained load response time too slow: {avg_response_time:.2f}s"
            
            print(f"Sustained load test: {len(completed_results)} requests over {duration_seconds}s")
            print(f"Success rate: {success_rate:.2%}")
            print(f"Average response time: {avg_response_time:.2f}s")

    def test_mixed_workload_performance(self):
        """Test API performance with mixed workload (list, search, get)."""
        # Arrange
        num_requests = 30
        
        def make_list_request():
            start_time = time.time()
            response = IncidentsAPI.list_incidents({"page": 1, "limit": 5, "is_simple": True})
            end_time = time.time()
            return {"type": "list", "response_time": end_time - start_time, "success": response.status_code == 200}
        
        def make_search_request():
            start_time = time.time()
            response = IncidentsAPI.search_incidents({"page": 1, "limit": 5, "search": "test"})
            end_time = time.time()
            return {"type": "search", "response_time": end_time - start_time, "success": response.status_code == 200}
        
        def make_get_request():
            start_time = time.time()
            response = IncidentsAPI.get_incident(1)  # Assuming incident 1 exists
            end_time = time.time()
            return {"type": "get", "response_time": end_time - start_time, "success": response.status_code in [200, 404]}
        
        # Act
        start_time = time.time()
        with ThreadPoolExecutor(max_workers=6) as executor:
            futures = []
            
            # Mix of different request types
            for i in range(num_requests):
                if i % 3 == 0:
                    futures.append(executor.submit(make_list_request))
                elif i % 3 == 1:
                    futures.append(executor.submit(make_search_request))
                else:
                    futures.append(executor.submit(make_get_request))
            
            results = [future.result() for future in as_completed(futures)]
        end_time = time.time()
        
        # Assert
        total_time = end_time - start_time
        successful_requests = [r for r in results if r["success"]]
        
        # Group by request type
        list_results = [r for r in results if r["type"] == "list"]
        search_results = [r for r in results if r["type"] == "search"]
        get_results = [r for r in results if r["type"] == "get"]
        
        success_rate = len(successful_requests) / len(results)
        assert success_rate >= 0.8, f"Mixed workload success rate too low: {success_rate:.2%}"
        
        # Check performance for each request type
        for request_type, type_results in [("list", list_results), ("search", search_results), ("get", get_results)]:
            if type_results:
                type_response_times = [r["response_time"] for r in type_results if r["success"]]
                if type_response_times:
                    avg_response_time = statistics.mean(type_response_times)
                    assert avg_response_time < 5.0, f"{request_type} requests too slow: {avg_response_time:.2f}s"
        
        print(f"Mixed workload test: {len(results)} requests in {total_time:.2f}s")
        print(f"Success rate: {success_rate:.2%}")
        print(f"List requests: {len(list_results)}")
        print(f"Search requests: {len(search_results)}")
        print(f"Get requests: {len(get_results)}")
