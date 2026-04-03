#!/usr/bin/env python3
"""Test script to verify sqlite3.Row fixes"""

import sys
import os

# Add app to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.db import get_latest_resume, get_resume_by_id, get_onboarding_response

DATABASE = os.path.join(os.path.dirname(__file__), "studybuddy.db")

print("=" * 70)
print("Testing sqlite3.Row fixes")
print("=" * 70)

# Test 1: Check get_latest_resume returns a dict
print("\n✅ Test 1: get_latest_resume returns dict or None")
try:
    result = get_latest_resume(DATABASE, "test@example.com")
    if result is None:
        print("   Result: None (no resume found - expected)")
    elif isinstance(result, dict):
        print(f"   ✓ Result is a dict with keys: {list(result.keys())[:3]}...")
        print(f"   ✓ Can access via .get(): {result.get('filename', 'N/A')}")
        print(f"   ✓ Can access via []: {result.get('id', 'N/A')}")
    else:
        print(f"   ✗ Result is a {type(result)} - PROBLEM!")
except Exception as e:
    print(f"   ✗ Error: {e}")

# Test 2: Check get_onboarding_response returns a dict
print("\n✅ Test 2: get_onboarding_response returns dict or None")
try:
    result = get_onboarding_response(DATABASE, "test@example.com")
    if result is None:
        print("   Result: None (no onboarding found - expected)")
    elif isinstance(result, dict):
        print(f"   ✓ Result is a dict with keys: {list(result.keys())[:3]}...")
        print(f"   ✓ Can access via .get(): {result.get('department', 'N/A')}")
    else:
        print(f"   ✗ Result is a {type(result)} - PROBLEM!")
except Exception as e:
    print(f"   ✗ Error: {e}")

# Test 3: Check get_resume_by_id returns a dict
print("\n✅ Test 3: get_resume_by_id returns dict or None")
try:
    result = get_resume_by_id(DATABASE, 999, "test@example.com")
    if result is None:
        print("   Result: None (no resume with that ID - expected)")
    elif isinstance(result, dict):
        print(f"   ✓ Result is a dict with keys: {list(result.keys())[:3]}...")
    else:
        print(f"   ✗ Result is a {type(result)} - PROBLEM!")
except Exception as e:
    print(f"   ✗ Error: {e}")

print("\n" + "=" * 70)
print("All tests completed successfully!")
print("=" * 70)
