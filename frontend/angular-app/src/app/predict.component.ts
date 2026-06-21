import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService } from './services/api.service';

@Component({
  standalone: true,
  selector: 'app-predict',
  imports: [CommonModule, FormsModule],
  template: `
    <section>
      <div class="row">
        <div class="col">
          <div class="title">Predict Burnout</div>
          <div class="card">
            <form (ngSubmit)="onSubmit()">
              <label>Employee ID
                <input [(ngModel)]="model.employee_id" name="employee_id" required />
              </label>
              <div class="row">
                <div class="col">
                  <label>Working hours (per day)
                    <input [(ngModel)]="model.working_hours_per_day" name="working_hours_per_day" type="number" step="0.1" />
                  </label>
                  <div class="muted small">Typical work hours per day (e.g. 8)</div>

                  <label>Overtime hours (per week)
                    <input [(ngModel)]="model.overtime_hours" name="overtime_hours" type="number" step="0.1" />
                  </label>
                  <div class="muted small">Total overtime hours in a typical week</div>
                </div>
                <div class="col">
                  <label>Meeting hours (per day)
                    <input [(ngModel)]="model.meeting_hours" name="meeting_hours" type="number" step="0.1" />
                  </label>
                  <div class="muted small">Average meeting hours per day</div>

                  <label>Leave count (per month)
                    <input [(ngModel)]="model.leave_count" name="leave_count" type="number" />
                  </label>
                  <div class="muted small">Number of leave days in a typical month</div>
                </div>
              </div>
              <label>Late arrivals (per month) <input [(ngModel)]="model.late_arrivals" name="late_arrivals" type="number" /></label>
              <div class="muted small">Number of late arrivals in a typical month</div>
              <label>Task completion % <input [(ngModel)]="model.task_completion_percent" name="task_completion_percent" type="number" /></label>
              <div class="muted small">Percentage of tasks completed on time (0-100)</div>
              <label>Performance rating (1-5) <input [(ngModel)]="model.performance_rating" name="performance_rating" type="number" step="0.1" /></label>
              <div class="muted small">Manager-provided performance rating (1 low - 5 high)</div>
              <div style="margin-top:0.6rem" class="spaced">
                <button class="btn" type="submit">Predict</button>
                <button type="button" class="btn secondary" (click)="reset()">Reset</button>
                <div class="muted small" *ngIf="message">{{message}}</div>
              </div>
            </form>
            <div *ngIf="result" class="result">
              <div><strong>Burnout:</strong> {{result.burnout_risk}}</div>
              <div *ngIf="result.productivity_score"><strong>Predicted productivity:</strong> {{result.productivity_score}}</div>
            </div>
          </div>
        </div>
      </div>
    </section>
  `
})
export class PredictComponent {
  model: any = { employee_id: '', working_hours_per_day:8, overtime_hours:0, meeting_hours:1, leave_count:0, late_arrivals:0, task_count:0, task_completion_percent:80, performance_rating:3.5, experience_years:1, project_count:0 };
  result: any = null;
  message = '';
  constructor(private api: ApiService) {}

  onSubmit(){
    this.message = 'Calling API...';
    const payload = { ...this.model };

    const sendRequest = (body:any)=>{
      this.api.predict(body).subscribe({next: res=>{ this.result = res; this.message=''; }, error: (err:any)=>{ console.error('Prediction error', err); this.message = 'Prediction error'; }});
    };

    // ensure required numeric fields exist
    payload.task_count = payload.task_count || 0;
    payload.experience_years = payload.experience_years || 0;
    payload.project_count = payload.project_count || 0;

    // employee_id may be an employee code like EMP001 — try to resolve to numeric id
    const eid = payload.employee_id;
    if (typeof eid === 'string' && eid.toUpperCase().startsWith('EMP')){
      this.api.getEmployees().subscribe({ next: (list:any[])=>{
        const found = (list||[]).find(x=> x.employee_code === eid);
        if (found) {
          payload.employee_id = found.id;
        } else {
          // fallback: try numeric part
          const n = parseInt(eid.replace(/[^0-9]/g,''),10);
          payload.employee_id = isNaN(n) ? 0 : n;
        }
        sendRequest(payload);
      }, error: (err)=>{ console.error('Failed to fetch employees to resolve id', err); payload.employee_id = 0; sendRequest(payload); } });
    } else {
      // ensure numeric
      payload.employee_id = Number(payload.employee_id) || 0;
      sendRequest(payload);
    }
  }

  reset(){ this.model = { employee_id: '', working_hours_per_day:8, overtime_hours:0, meeting_hours:1, leave_count:0, late_arrivals:0, task_count:0, task_completion_percent:80, performance_rating:3.5, experience_years:1, project_count:0 }; this.result=null; }
}
