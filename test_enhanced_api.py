#!/usr/bin/env python3
"""
Test script for enhanced Sentinel API endpoints.
"""
import requests
import json
import time
from datetime import datetime

BASE_URL = "http://localhost:8000"

def test_endpoint(endpoint, method="GET", data=None):
    """Test an API endpoint and return results."""
    url = f"{BASE_URL}{endpoint}"
    try:
        if method == "GET":
            response = requests.get(url, timeout=10)
        elif method == "POST":
            response = requests.post(url, json=data, timeout=10)
        
        print(f"✅ {method} {endpoint}: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, dict) and 'timestamp' in result:
                print(f"   📅 Timestamp: {result['timestamp']}")
            if isinstance(result, dict) and 'status' in result:
                print(f"   📊 Status: {result['status']}")
            return result
        else:
            print(f"   ❌ Error: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"❌ {method} {endpoint}: Connection error - {e}")
        return None
    except Exception as e:
        print(f"❌ {method} {endpoint}: Unexpected error - {e}")
        return None

def test_real_time_monitor():
    """Test the real-time monitoring endpoint."""
    print("\n🔍 Testing real-time monitoring (10 seconds)...")
    try:
        response = requests.get(f"{BASE_URL}/monitor?duration=10", stream=True, timeout=15)
        if response.status_code == 200:
            print("✅ Real-time monitoring stream started")
            count = 0
            for line in response.iter_lines():
                if line:
                    count += 1
                    if count <= 3:  # Show first 3 updates
                        data = line.decode('utf-8')
                        if data.startswith('data: '):
                            try:
                                json_data = json.loads(data[6:])
                                print(f"   📊 Update {count}: {json_data.get('events_count', 0)} events, {json_data.get('alerts_count', 0)} alerts")
                            except:
                                pass
                    if count >= 6:  # Stop after 6 updates (30 seconds)
                        break
            print(f"   ✅ Received {count} monitoring updates")
        else:
            print(f"❌ Monitoring failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Monitoring test failed: {e}")

def main():
    """Run all API tests."""
    print("🧪 Testing Enhanced Sentinel API v1.0.0")
    print("=" * 50)
    
    # Test basic endpoints
    print("\n🔍 Testing Basic Endpoints:")
    test_endpoint("/")
    test_endpoint("/health")
    test_endpoint("/status")
    
    # Test data endpoints
    print("\n📊 Testing Data Endpoints:")
    test_endpoint("/events?limit=5")
    test_endpoint("/alerts?limit=5")
    test_endpoint("/events?event_type=process&limit=3")
    test_endpoint("/alerts?severity=high&limit=3")
    
    # Test advanced endpoints
    print("\n🚀 Testing Advanced Endpoints:")
    test_endpoint("/rules")
    test_endpoint("/stats?hours=24")
    test_endpoint("/processes?limit=5&sort_by=cpu")
    test_endpoint("/network?limit=5")
    
    # Test manual scan
    print("\n🔍 Testing Manual Scan:")
    test_endpoint("/scan", method="POST")
    
    # Test real-time monitoring
    test_real_time_monitor()
    
    # Test rules reload
    print("\n🔄 Testing Rules Reload:")
    test_endpoint("/rules/reload", method="POST")
    
    print("\n🎉 API Testing Complete!")
    print("=" * 50)
    print("📚 View full API documentation at: http://localhost:8000/docs")
    print("🔍 Test individual endpoints manually for detailed responses")

if __name__ == "__main__":
    main() 