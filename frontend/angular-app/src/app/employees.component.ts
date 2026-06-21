import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApiService } from './services/api.service';

@Component({
  standalone: true,
  selector: 'app-employees',
  imports: [CommonModule],
  template: `
    <section>
      <div class="title">Employees</div>
      <div class="card">
        <div class="spaced" style="margin-bottom:0.6rem">
          <button class="btn" (click)="refresh()">Refresh</button>
          <div class="muted small">Click refresh to load employees from backend</div>
        </div>
        <table class="table">
          <thead><tr><th>ID</th><th>Code</th><th>Name</th><th>Email</th></tr></thead>
          <tbody>
            <tr *ngFor="let e of employees">
              <td>{{e.id}}</td>
              <td>{{e.employee_code || '-'}}</td>
              <td>{{e.first_name}} {{e.last_name}}</td>
              <td>{{e.email || '-'}}</td>
            </tr>
          </tbody>
        </table>
        <div *ngIf="!employees.length && !message" class="muted">No employees loaded</div>
        <div *ngIf="message" class="muted">{{message}}</div>
      </div>
    </section>
  `
})
export class EmployeesComponent implements OnInit {
  employees: any[] = [];
  message = '';
  constructor(private api: ApiService) {}

  ngOnInit(): void {
    // load on enter
    this.refresh();
  }

  refresh(){
    this.message = 'Loading...';
    // choose endpoint based on role
    const rolesRaw = sessionStorage.getItem('roles') || '[]';
    let roles: string[] = [];
    try{ roles = JSON.parse(rolesRaw); }catch(e){ roles = []; }

    if(roles.includes('HR')){
      // HR sees all employees
      this.api.getEmployees().subscribe({ next: this.handleList.bind(this), error: this.handleErr.bind(this) });
      return;
    }

    if(roles.includes('Manager')){
      // Manager sees only their reportees
      const mgrId = Number(sessionStorage.getItem('employee_id') || 0);
      if(!mgrId){ this.message='Manager id missing'; return; }
      this.api.getReportees(mgrId).subscribe({ next: this.handleList.bind(this), error: this.handleErr.bind(this) });
      return;
    }

    // Default: Employee sees only their own record
    const empId = Number(sessionStorage.getItem('employee_id') || 0);
    if(!empId){ this.message='Employee id missing'; return; }
    this.api.getEmployee(empId).subscribe({ next: (data:any)=>{ this.handleList(Array.isArray(data)?data:[data]); }, error: this.handleErr.bind(this) });
  }

  private handleList(data:any){
    const list = Array.isArray(data) ? data : [];
    this.employees = list.map((r:any)=>({
      id: r.id,
      employee_code: r.employee_code,
      first_name: r.first_name || r.name || '',
      last_name: r.last_name || '',
      email: r.email || (r.first_name && r.last_name ? `${r.first_name.toLowerCase()}.${r.last_name.toLowerCase()}@example.com` : undefined),
      experience: (r.experience !== null && r.experience !== undefined && Number(r.experience) > 0) ? r.experience : null
    }));
    this.message='';
  }

  private handleErr(err:any){ console.error('Error fetching employees', err); this.message = 'Error fetching employees'; }
}
