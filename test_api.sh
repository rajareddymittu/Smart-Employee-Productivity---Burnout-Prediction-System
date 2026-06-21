#!/bin/bash

# API Testing Quick Start Guide
# Test the implemented endpoints

BASE_URL="http://localhost:8001/api"

echo "=== AI-Powered Employee Productivity API - Testing ==="
echo "Base URL: $BASE_URL"
echo ""

# Health Check
echo "1. Health Check"
curl -s "$BASE_URL/health" | jq . || curl -s "$BASE_URL/health"
echo -e "\n---\n"

# Create Employee
echo "2. Create Employee"
curl -s -X POST "$BASE_URL/employees" \
  -H "Content-Type: application/json" \
  -d '{
    "employee_code": "EMP001",
    "first_name": "John",
    "last_name": "Doe",
    "gender": "Male",
    "department_id": 1,
    "experience": 5.5,
    "salary_grade": "Senior",
    "status": "active"
  }' | jq . || echo "Check if backend is running on port 8001"
echo -e "\n---\n"

# Get Employees
echo "3. Get All Employees"
curl -s "$BASE_URL/employees?skip=0&limit=10" | jq . 2>/dev/null || echo "No employees yet"
echo -e "\n---\n"

# Get Specific Employee
echo "4. Get Employee by ID"
curl -s "$BASE_URL/employees/1" | jq . 2>/dev/null || echo "Employee not found"
echo -e "\n---\n"

# Create Prediction
echo "5. Create Prediction (Burnout Analysis)"
curl -s -X POST "$BASE_URL/predictions/burnout?employee_id=1" \
  -H "Content-Type: application/json" \
  -d '{
    "employee_id": 1,
    "working_hours_per_day": 9.0,
    "overtime_hours": 5.0,
    "meeting_hours": 4.0,
    "leave_count": 3,
    "late_arrivals": 2,
    "task_count": 15,
    "task_completion_percent": 85.0,
    "performance_rating": 4.5,
    "experience_years": 5.5,
    "project_count": 3
  }' | jq . 2>/dev/null || echo "Prediction failed"
echo -e "\n---\n"

# Get Predictions
echo "6. Get All Predictions"
curl -s "$BASE_URL/predictions?skip=0&limit=10" | jq . 2>/dev/null || echo "No predictions yet"
echo -e "\n---\n"

echo "=== Testing Complete ==="
echo ""
echo "Additional endpoints to test:"
echo "- POST   /api/attendance/checkin"
echo "- POST   /api/attendance/checkout"
echo "- POST   /api/leaves (apply for leave)"
echo "- PUT    /api/leaves/{id}/approve"
echo "- POST   /api/tasks (create task)"
echo "- POST   /api/projects (create project)"
echo ""
echo "For interactive API documentation, visit:"
echo "http://localhost:8001/docs"
