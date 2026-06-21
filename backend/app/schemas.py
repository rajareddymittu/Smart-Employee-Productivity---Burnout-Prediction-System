from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import date, datetime


# ==================== Auth Schemas ====================
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: Optional[int] = None


class TokenData(BaseModel):
    username: Optional[str] = None
    user_id: Optional[int] = None


# ==================== User Schemas ====================
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    employee_id: Optional[int] = None
    role: Optional[str] = None


class LoginRequest(BaseModel):
    username: str
    password: str
    email: Optional[EmailStr] = None


class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    employee_id: Optional[int]
    created_at: datetime
    roles: Optional[List["RoleOut"]] = None

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None


# ==================== Role Schemas ====================
class RoleOut(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


# ==================== Department Schemas ====================
class DepartmentCreate(BaseModel):
    name: str
    manager_id: Optional[int] = None


class DepartmentUpdate(BaseModel):
    name: Optional[str] = None
    manager_id: Optional[int] = None


class DepartmentOut(BaseModel):
    id: int
    name: str
    manager_id: Optional[int]
    created_at: datetime

    class Config:
        orm_mode = True


# ==================== Employee Schemas ====================
class EmployeeCreate(BaseModel):
    employee_code: str
    first_name: str
    last_name: Optional[str] = None
    gender: Optional[str] = None
    dob: Optional[date] = None
    department_id: Optional[int] = None
    manager_id: Optional[int] = None
    joining_date: Optional[date] = None
    experience: Optional[float] = None
    salary_grade: Optional[str] = None
    status: str = "active"


class EmployeeUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    gender: Optional[str] = None
    dob: Optional[date] = None
    department_id: Optional[int] = None
    experience: Optional[float] = None
    salary_grade: Optional[str] = None
    status: Optional[str] = None


class EmployeeOut(BaseModel):
    id: int
    employee_code: str
    first_name: str
    last_name: Optional[str]
    gender: Optional[str]
    dob: Optional[date]
    department_id: Optional[int]
    manager_id: Optional[int]
    joining_date: Optional[date]
    experience: Optional[float]
    salary_grade: Optional[str]
    status: str
    created_at: datetime

    class Config:
        orm_mode = True


class RecentHireOut(BaseModel):
    id: int
    employee_code: str
    first_name: str
    last_name: Optional[str]
    gender: Optional[str]
    dob: Optional[date]
    department_id: Optional[int]
    manager_id: Optional[int]
    joining_date: Optional[date]
    experience: Optional[float]
    salary_grade: Optional[str]
    status: str
    created_at: datetime
    burnout_score: Optional[float]

    class Config:
        orm_mode = True


# ==================== Attendance Schemas ====================
class AttendanceCreate(BaseModel):
    employee_id: int
    date: date
    check_in: Optional[datetime] = None
    check_out: Optional[datetime] = None
    overtime_hours: Optional[float] = 0


class AttendanceUpdate(BaseModel):
    check_in: Optional[datetime] = None
    check_out: Optional[datetime] = None
    overtime_hours: Optional[float] = None


class AttendanceOut(BaseModel):
    id: int
    employee_id: int
    date: date
    check_in: Optional[datetime]
    check_out: Optional[datetime]
    overtime_hours: float
    created_at: datetime

    class Config:
        orm_mode = True


# ==================== Leave Schemas ====================
class LeaveTypeOut(BaseModel):
    id: int
    name: str
    description: Optional[str]

    class Config:
        orm_mode = True


class LeaveRequestCreate(BaseModel):
    employee_id: int
    leave_type_id: int
    start_date: date
    end_date: date


class LeaveRequestUpdate(BaseModel):
    status: str


class LeaveRequestOut(BaseModel):
    id: int
    employee_id: int
    leave_type_id: int
    start_date: date
    end_date: date
    status: str
    applied_on: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


# ==================== Project Schemas ====================
class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status: str = "active"


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status: Optional[str] = None


class ProjectOut(BaseModel):
    id: int
    name: str
    description: Optional[str]
    start_date: Optional[date]
    end_date: Optional[date]
    status: str
    created_at: datetime

    class Config:
        orm_mode = True


# ==================== Task Schemas ====================
class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    priority: str = "medium"
    due_date: Optional[date] = None
    status: str = "pending"
    project_id: Optional[int] = None


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[str] = None
    due_date: Optional[date] = None
    status: Optional[str] = None
    project_id: Optional[int] = None


class TaskOut(BaseModel):
    id: int
    title: str
    description: Optional[str]
    priority: str
    due_date: Optional[date]
    status: str
    project_id: Optional[int]
    created_at: datetime

    class Config:
        orm_mode = True


# ==================== Meeting Schemas ====================
class MeetingCreate(BaseModel):
    title: str
    description: Optional[str] = None
    duration: Optional[float] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None


class MeetingOut(BaseModel):
    id: int
    title: str
    description: Optional[str]
    duration: Optional[float]
    start_time: Optional[datetime]
    end_time: Optional[datetime]
    created_at: datetime

    class Config:
        orm_mode = True


# ==================== Performance Review Schemas ====================
class PerformanceReviewCreate(BaseModel):
    employee_id: int
    rating: float
    comments: Optional[str] = None
    review_date: Optional[date] = None


class PerformanceReviewOut(BaseModel):
    id: int
    employee_id: int
    rating: float
    comments: Optional[str]
    review_date: Optional[date]
    created_at: datetime

    class Config:
        orm_mode = True


# ==================== Work Log Schemas ====================
class WorkLogCreate(BaseModel):
    employee_id: int
    date: date
    working_hours: Optional[float] = None
    meeting_hours: Optional[float] = None
    task_count: Optional[int] = 0
    task_completion_percent: Optional[float] = None


class WorkLogOut(BaseModel):
    id: int
    employee_id: int
    date: date
    working_hours: Optional[float]
    meeting_hours: Optional[float]
    task_count: int
    task_completion_percent: Optional[float]
    created_at: datetime

    class Config:
        orm_mode = True


# ==================== Prediction Schemas ====================
class PredictRequest(BaseModel):
    employee_id: int
    working_hours_per_day: float = Field(..., ge=0)
    overtime_hours: float = Field(..., ge=0)
    meeting_hours: float = Field(..., ge=0)
    leave_count: int = Field(..., ge=0)
    late_arrivals: int = Field(..., ge=0)
    task_count: int = Field(..., ge=0)
    task_completion_percent: float = Field(..., ge=0, le=100)
    performance_rating: float = Field(..., ge=0, le=5)
    experience_years: float = Field(..., ge=0)
    project_count: int = Field(..., ge=0)


class PredictionOut(BaseModel):
    id: int
    employee_id: int
    burnout_risk: str
    burnout_score: Optional[float]
    productivity_score: Optional[float]
    predicted_on: datetime

    class Config:
        orm_mode = True


# ==================== Audit Log Schemas ====================
class AuditLogOut(BaseModel):
    id: int
    user_id: int
    action: str
    entity: str
    entity_id: Optional[int]
    changes: Optional[str]
    timestamp: datetime

    class Config:
        orm_mode = True


# ==================== Notification Schemas ====================
class NotificationCreate(BaseModel):
    user_id: int
    title: str
    message: str


class NotificationOut(BaseModel):
    id: int
    user_id: int
    title: str
    message: str
    is_read: bool
    created_at: datetime

    class Config:
        orm_mode = True
