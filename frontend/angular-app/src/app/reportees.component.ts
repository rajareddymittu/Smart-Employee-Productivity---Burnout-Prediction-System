import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApiService } from './services/api.service';

@Component({
  standalone: true,
  selector: 'app-reportees',
  imports: [CommonModule],
  template: `
    <section>
      <div class="title">My Reportees</div>
      <div class="card">
        <div *ngIf="reportees?.length">
          <ul>
            <li *ngFor="let e of reportees">{{e.employee_code}} - {{e.first_name}} {{e.last_name}}</li>
          </ul>
        </div>
        <div *ngIf="!reportees || !reportees.length">No reportees found.</div>
      </div>
    </section>
  `
})
export class ReporteesComponent{
  reportees:any[] = [];
  constructor(private api: ApiService){
    const emp = Number(sessionStorage.getItem('employee_id') || 0);
    if(emp){ this.api.getReportees(emp).subscribe({ next: (res:any)=>{ this.reportees = res || []; }, error: (e)=>{ console.error(e); } }); }
  }
}
