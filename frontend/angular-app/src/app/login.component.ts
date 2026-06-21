import { Component, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { ApiService } from './services/api.service';

@Component({
  standalone: true,
  selector: 'app-login',
  imports: [CommonModule, FormsModule],
  template: `
    <div class="login-wrapper">
      <div class="login-card">
        <div class="title">Login</div>
        <div class="card">
          <form (ngSubmit)="submit()">
            <label>Username
              <input [(ngModel)]="username" name="username" required />
            </label>
            <label>Email
              <input [(ngModel)]="email" name="email" type="email" />
            </label>
            <label>Password
              <input [(ngModel)]="password" name="password" type="password" required />
            </label>
            <div class="spaced" style="margin-top:0.6rem; display:flex; gap:0.5rem; flex-wrap:wrap">
              <button class="btn" type="submit">Login</button>
              <button type="button" class="btn secondary" (click)="demoEmployee()">Demo Employee</button>
              <button type="button" class="btn secondary" (click)="demoManager()">Demo Manager</button>
              <button type="button" class="btn secondary" (click)="demoHr()">Demo HR</button>
            </div>
          </form>
          <div *ngIf="message" class="muted small" style="margin-top:0.6rem">{{message}}</div>
        </div>
        </div>
      </div>
  `
  ,
  styles: [
    `:host { display: block; }
     .login-wrapper { min-height: 100vh; display:flex; align-items:center; justify-content:center; padding:2rem; }
     .login-card { width:420px; }
     .card { padding:1.1rem }
    `
  ]
})
export class LoginComponent {
  username = '';
  email = '';
  password = '';
  message = '';
  constructor(private api: ApiService, private router: Router) {}

  @Output() loggedIn = new EventEmitter<boolean>();

  submit(){
    this.message = 'Logging in...';
    const emailToSend = this.email && this.email.length ? this.email : (this.username.includes('@') ? this.username : `${this.username}@example.com`);
    this.api.login({ username: this.username, password: this.password, email: emailToSend }).subscribe({
      next: (res: any) => {
        if (res && res.access_token) {
          sessionStorage.setItem('access_token', res.access_token);
          // fetch current user and store details
          this.api.getCurrentUser().subscribe({ next: (u:any)=>{
            sessionStorage.setItem('username', u.username);
            sessionStorage.setItem('user_id', String(u.id));
            sessionStorage.setItem('employee_id', String(u.employee_id || ''));
            sessionStorage.setItem('roles', JSON.stringify((u.roles||[]).map((r:any)=>r.name)));
            this.message = 'Login successful';
            this.loggedIn.emit(true);
            this.router.navigate(['/']);
          }, error: ()=>{ this.message='Login succeeded but failed to fetch user'; this.loggedIn.emit(true); this.router.navigate(['/']); }});
        } else {
          this.message = 'Unexpected response from server';
        }
      },
      error: (err) => {
        this.message = err?.error?.detail || 'Login failed';
      }
    });
  }

  demo(){
    this.demoEmployee();
  }

  demoEmployee(){
    this.username = 'demo1'; this.email = 'demo1@example.com'; this.password = 'DemoPass1'; this.submit();
  }

  demoManager(){
    this.username = 'manager'; this.email = 'manager@example.com'; this.password = 'ManagerPass1'; this.submit();
  }

  demoHr(){
    this.username = 'hr'; this.email = 'hr@example.com'; this.password = 'HRPass1'; this.submit();
  }
}
