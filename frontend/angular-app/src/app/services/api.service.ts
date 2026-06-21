import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class ApiService {
  base = 'http://127.0.0.1:8000/api';
  constructor(private http: HttpClient) {}

  private authHeaders(): { headers: HttpHeaders } {
    const token = sessionStorage.getItem('access_token');
    if (token) {
      return { headers: new HttpHeaders({ Authorization: `Bearer ${token}` }) };
    }
    return { headers: new HttpHeaders() };
  }

  getEmployees(): Observable<any> {
    return this.http.get(`${this.base}/employees`, this.authHeaders());
  }

  predict(payload: any): Observable<any> {
    return this.http.post(`${this.base}/predict/burnout`, payload, this.authHeaders());
  }

  login(payload: { username: string; password: string; email?: string }): Observable<any> {
    return this.http.post(`${this.base}/auth/login`, payload);
  }

  getCurrentUser(): Observable<any> {
    return this.http.get(`${this.base}/auth/me`, this.authHeaders());
  }

  getEmployee(employee_id:number): Observable<any>{
    return this.http.get(`${this.base}/employees/${employee_id}`, this.authHeaders());
  }

  // Worklogs
  createWorklog(payload:any): Observable<any>{
    return this.http.post(`${this.base}/worklogs/`, payload, this.authHeaders());
  }

  getWorklogsForEmployee(employee_id:number): Observable<any>{
    return this.http.get(`${this.base}/worklogs/employee/${employee_id}`, this.authHeaders());
  }

  // Manager reportees
  getReportees(manager_id:number): Observable<any>{
    return this.http.get(`${this.base}/managers/${manager_id}/reportees`, this.authHeaders());
  }

  // HR endpoints
  getManagerBurnout(): Observable<any>{
    return this.http.get(`${this.base}/hr/manager-burnout`, this.authHeaders());
  }

  getRecentHires(q?: string): Observable<any>{
    const url = q ? `${this.base}/hr/recent-hires?q=${encodeURIComponent(q)}` : `${this.base}/hr/recent-hires`;
    return this.http.get(url, this.authHeaders());
  }
}
