# Phase 6 - Angular Frontend Design & UI/UX Specification

# 1. Frontend Stack

-   Angular 19
-   Standalone Components
-   Angular Material
-   RxJS / Signals
-   Chart.js
-   Bootstrap 5

------------------------------------------------------------------------

# 2. Navigation

Login → Dashboard → Employees → Departments → Attendance → Leave →
Projects → Tasks → Performance → AI Analytics → Reports → Profile →
Logout

------------------------------------------------------------------------

# 3. User Roles

-   Admin
-   HR
-   Manager
-   Employee

Each role has route guards and menu visibility.

------------------------------------------------------------------------

# 4. Screen List

1.  Login
2.  Dashboard
3.  Employee List
4.  Employee Profile
5.  Department Management
6.  Attendance
7.  Leave Management
8.  Projects
9.  Tasks
10. Meetings
11. Performance Reviews
12. AI Burnout Dashboard
13. Productivity Dashboard
14. Reports
15. Notifications
16. User Management
17. Audit Logs
18. Settings
19. Profile
20. About

------------------------------------------------------------------------

# 5. Dashboard Widgets

-   Total Employees
-   Attendance Today
-   Pending Leaves
-   Active Projects
-   Burnout Distribution
-   Productivity Trend
-   Department Performance
-   Recent Activities

------------------------------------------------------------------------

# 6. Component Structure

app/ - layout/ - shared/ - auth/ - dashboard/ - employees/ -
attendance/ - leave/ - projects/ - tasks/ - reports/ - analytics/ -
admin/

------------------------------------------------------------------------

# 7. Route Guards

-   AuthGuard
-   AdminGuard
-   HRGuard
-   ManagerGuard

------------------------------------------------------------------------

# 8. Forms

Reactive Forms

Validation: - Required - Email - Min Length - Max Length - Pattern

------------------------------------------------------------------------

# 9. Charts

-   Line Chart
-   Bar Chart
-   Pie Chart
-   Doughnut Chart

Used for analytics and ML predictions.

------------------------------------------------------------------------

# 10. Responsive Design

Desktop Tablet Mobile

Material responsive grid system.

------------------------------------------------------------------------

# 11. Theme

Primary: Blue Accent: Green Typography: Roboto Dark Mode Supported

------------------------------------------------------------------------

# 12. API Integration

Angular Service → HTTP Client → FastAPI → JWT Header → JSON Response →
UI Update

------------------------------------------------------------------------

# 13. Security

-   JWT Interceptor
-   Route Guards
-   Session Timeout
-   Refresh Token Flow

------------------------------------------------------------------------

# 14. UX Principles

-   Minimal clicks
-   Clear navigation
-   Accessible forms
-   Consistent layouts
-   Real-time feedback
-   Error messages
