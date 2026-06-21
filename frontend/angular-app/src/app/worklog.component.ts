import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService } from './services/api.service';

@Component({
  standalone: true,
  selector: 'app-worklog',
  imports: [CommonModule, FormsModule],
  template: `
    <section>
      <div class="title">Log Shift / Worklog</div>
      <div class="card">
        <form (ngSubmit)="submit()">
          <label>Employee ID
            <input [(ngModel)]="model.employee_id" name="employee_id" required />
          </label>
          <label>Date
            <input type="date" [(ngModel)]="model.date" name="date" required />
          </label>
          <label>Working hours
            <input type="number" step="0.1" [(ngModel)]="model.working_hours" name="working_hours" />
          </label>
          <label>Meeting hours
            <input type="number" step="0.1" [(ngModel)]="model.meeting_hours" name="meeting_hours" />
          </label>
          <label>Task count
            <input type="number" [(ngModel)]="model.task_count" name="task_count" />
          </label>
          <label>Task completion %
            <input type="number" [(ngModel)]="model.task_completion_percent" name="task_completion_percent" />
          </label>
          <div class="spaced" style="margin-top:0.6rem">
            <button class="btn" type="submit">Submit</button>
          </div>
        </form>
        <div *ngIf="message" class="muted small">{{message}}</div>
      </div>

      <div style="margin-top:1rem">
        <div class="title">Recent logs</div>
        <div *ngIf="logs?.length">
          <table>
            <thead><tr><th>Date</th><th>Hours</th><th>Meeting</th><th>Tasks</th><th>Completion%</th></tr></thead>
            <tbody>
              <tr *ngFor="let l of logs">
                <td>{{l.date}}</td>
                <td>{{l.working_hours}}</td>
                <td>{{l.meeting_hours}}</td>
                <td>{{l.task_count}}</td>
                <td>{{l.task_completion_percent}}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </section>
  `
})
export class WorklogComponent{
  model:any = { employee_id: '', date: '', working_hours:8, meeting_hours:1, task_count:0, task_completion_percent:80 };
  message = '';
  logs:any[] = [];
  constructor(private api: ApiService){
    const emp = sessionStorage.getItem('employee_id');
    if(emp){ this.model.employee_id = emp; this.loadLogs(); }
  }

  submit(){
    this.message = 'Saving...';
    const body = { ...this.model };
    // basic client-side validation / coercion to avoid API 422
    if(!body.employee_id){ this.message = 'Employee ID required'; return; }
    if(!body.date){ this.message = 'Date required'; return; }
    body.employee_id = Number(body.employee_id);
    if(isNaN(body.employee_id) || body.employee_id <= 0){ this.message = 'Invalid employee id'; return; }
    // ensure date is ISO YYYY-MM-DD
    try{ body.date = new Date(body.date).toISOString().slice(0,10); }catch(e){ this.message='Invalid date'; return; }

    this.api.createWorklog(body).subscribe({ next: (r:any)=>{ this.message='Saved'; this.loadLogs(); }, error: (e:any)=>{ this.message='Error saving'; console.error(e); } });
  }

  loadLogs(){
    const emp = Number(sessionStorage.getItem('employee_id') || this.model.employee_id || 0);
    if(!emp) return;
    this.api.getWorklogsForEmployee(emp).subscribe({ next: (res:any)=>{ this.logs = res || []; }, error: (e)=>{ console.error(e); } });
  }
}
