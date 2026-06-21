import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService } from './services/api.service';

interface EmployeeRow {
  id: number;
  employee_code: string;
  first_name: string;
  last_name?: string;
  joining_date?: string;
  experience?: number;
  department_id?: number | null;
  status?: string;
  burnout_score?: number;
}

@Component({
  standalone: true,
  selector: 'app-dashboard',
  imports: [CommonModule, FormsModule],
  template: `
    <section>
      <div class="title">Dashboard</div>

      <div class="row" style="margin-bottom:1rem">
        <div class="col card">
          <div class="small muted">Headcount</div>
          <div style="font-size:1.6rem;margin-top:0.5rem">{{headcount}}</div>
        </div>
        <div class="col card">
          <div class="small muted">Active</div>
          <div style="font-size:1.6rem;margin-top:0.5rem">{{activeCount}}</div>
        </div>
        <div class="col card">
          <div class="small muted">Recent Joins (30d)</div>
          <div style="font-size:1.6rem;margin-top:0.5rem">{{recentJoins}}</div>
        </div>
        <div class="col card">
          <div class="small muted">Avg Experience (yrs)</div>
          <div style="font-size:1.6rem;margin-top:0.5rem">{{avgExperience | number:'1.1-1'}}</div>
        </div>
      </div>

      <div class="card">
        <div style="display:flex;justify-content:space-between;align-items:center">
          <div class="small muted">Recent Hires</div>
          <div>
            <input placeholder="Search by name or code" [(ngModel)]="q" style="padding:0.35rem;border-radius:6px;border:1px solid rgba(255,255,255,0.04);background:transparent;color:var(--text)" />
          </div>
        </div>

        <table class="table" style="margin-top:0.6rem">
          <thead>
            <tr>
              <th>Code</th>
              <th>Name</th>
              <th>Dept</th>
              <th>Joined</th>
              <th>Exp</th>
              <th>Burnout</th>
            </tr>
          </thead>
          <tbody>
            <tr *ngFor="let e of filtered.slice(0,20)">
              <td>{{e.employee_code}}</td>
              <td>{{e.first_name}} {{e.last_name}}</td>
              <td>{{e.department_id || '-'}}</td>
              <td>{{e.joining_date || '-'}}</td>
              <td>{{e.experience || '-'}}</td>
              <td>
                <div style="display:flex;align-items:center;gap:0.5rem">
                  <div style="width:80px;background:rgba(255,255,255,0.03);border-radius:6px;padding:0.2rem">
                    <div [style.width.%]="e.burnout_score" style="height:8px;background:linear-gradient(90deg,#f97316,#ef4444);border-radius:6px"></div>
                  </div>
                  <div style="min-width:32px;text-align:right">{{e.burnout_score}}%</div>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>
  `
})
export class DashboardComponent implements OnInit {
  employees: EmployeeRow[] = [];
  q = '';
  headcount = 0;
  activeCount = 0;
  recentJoins = 0;
  avgExperience = 0;

  constructor(private api: ApiService) {}

  ngOnInit(): void {
    this.load();
  }

  get filtered() {
    const q = (this.q || '').toLowerCase().trim();
    if (!q) return this.employees.sort((a,b) => (b.joining_date || '').localeCompare(a.joining_date || ''));
    return this.employees.filter(e => (`${e.first_name} ${e.last_name}`.toLowerCase().includes(q) || e.employee_code.toLowerCase().includes(q)) ).sort((a,b) => (b.joining_date || '').localeCompare(a.joining_date || ''));
  }

  load(){
    this.api.getEmployees().subscribe({
      next: (res:any) => {
        if (Array.isArray(res)){
          this.employees = res.map((r:any) => ({
            id: r.id,
            employee_code: r.employee_code,
            first_name: r.first_name,
            last_name: r.last_name,
            joining_date: r.joining_date ? r.joining_date.split('T')[0] : undefined,
            experience: r.experience ? Number(r.experience) : undefined,
            department_id: r.department_id,
            status: r.status,
            burnout_score: Math.round(Math.max(5, Math.min(95, (Math.random()*60) + (r.experience? (Number(r.experience)%10)*3 : 10) )))
          }));
          // compute derived metrics once to avoid ExpressionChangedAfterItHasBeenCheckedError
          this.headcount = this.employees.length;
          this.activeCount = this.employees.filter(e=> e.status === 'active' || !e.status).length;
          const cutoff = new Date();
          cutoff.setDate(cutoff.getDate() - 30);
          this.recentJoins = this.employees.filter(e => {
            if (!e.joining_date) return false;
            const d = new Date(e.joining_date);
            return d >= cutoff;
          }).length;
          const ex = this.employees.map(e => e.experience || 0);
          this.avgExperience = ex.length ? Number((ex.reduce((a,b)=>a+b,0)/ex.length).toFixed(1)) : 0;
        }
      },
      error: (err) => {
        console.error('Failed to load employees', err);
      }
    })
  }
}
