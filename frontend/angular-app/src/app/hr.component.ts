import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService } from './services/api.service';

@Component({
  standalone: true,
  selector: 'app-hr',
  imports: [CommonModule, FormsModule],
  template: `
    <section>
      <div class="title">HR - Recent Hires by Manager</div>
      <div class="card">
        <div style="display:flex;gap:8px;align-items:center;margin-bottom:8px">
          <input placeholder="Search by name or code" [(ngModel)]="q" />
          <button class="btn" (click)="search()">Search</button>
          <button class="btn secondary" (click)="refresh()">Refresh</button>
        </div>

        <div *ngIf="groups?.length; else empty">
          <div *ngFor="let g of groups" style="margin-bottom:1rem">
            <div style="font-weight:700;margin-bottom:6px">{{g.manager_name || 'Unassigned'}}</div>
            <table class="table">
              <thead><tr><th>Code</th><th>Name</th><th>Dept</th><th>Joined</th><th>Exp</th><th>Burnout</th></tr></thead>
              <tbody>
                <tr *ngFor="let r of g.employees">
                  <td>{{r.employee_code}}</td>
                  <td>{{r.first_name}} {{r.last_name || ''}}</td>
                  <td>{{r.department_name || '-'}}</td>
                  <td>{{formatDate(r.joining_date)}}</td>
                  <td>{{r.experience ?? '-'}}</td>
                  <td>
                    <span *ngIf="r.burnout_score !== null && r.burnout_score !== undefined" [ngClass]="badgeClass(r.burnout_score)" class="badge">
                      {{(r.burnout_score*100).toFixed(0)}}%
                    </span>
                    <span *ngIf="r.burnout_score === null || r.burnout_score === undefined">-</span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
        <ng-template #empty>
          <div *ngIf="!message" class="muted">No recent hires</div>
        </ng-template>
        <div *ngIf="message" class="muted">{{message}}</div>
      </div>
    </section>
  `
})
export class HrComponent implements OnInit {
  groups: any[] = [];
  message = '';
  q = '';
  constructor(private api: ApiService) {}
  ngOnInit(): void { this.refresh(); }

  refresh(){
    this.message = 'Loading...';
    this.api.getRecentHires().subscribe({ next: (res:any)=>{ this.groups = res.by_manager || []; this.message=''; }, error: (e)=>{ console.error(e); this.message='Failed to load'; } });
  }

  search(){
    this.message = 'Searching...';
    this.api.getRecentHires(this.q).subscribe({ next: (res:any)=>{ this.groups = res.by_manager || []; this.message=''; }, error: (e)=>{ console.error(e); this.message='Search failed'; } });
  }

  formatDate(d?: string|null){ if(!d) return '-'; try{ const dt = new Date(d); return dt.toISOString().slice(0,10); }catch(e){ return d; } }

  badgeClass(score:number){
    if(score >= 0.66) return 'badge-red';
    if(score >= 0.33) return 'badge-yellow';
    return 'badge-green';
  }
}

/* styles for badges */
const styles = document.createElement('style');
styles.innerHTML = `
.badge { padding:4px 8px; border-radius:12px; color:white; font-weight:600 }
.badge-green { background:#2ecc71 }
.badge-yellow { background:#f1c40f }
.badge-red { background:#e74c3c }
`;
document.head.appendChild(styles);
