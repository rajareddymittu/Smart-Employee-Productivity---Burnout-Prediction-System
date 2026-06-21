import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterOutlet } from '@angular/router';
import { NavbarComponent } from './navbar.component';
import { LoginComponent } from './login.component';

@Component({
  standalone: true,
  selector: 'app-root',
  imports: [CommonModule, RouterOutlet, NavbarComponent, LoginComponent],
  template: `
    <ng-container *ngIf="!isLoggedIn">
      <app-login (loggedIn)="onLoggedIn()"></app-login>
    </ng-container>

    <ng-container *ngIf="isLoggedIn">
      <app-navbar></app-navbar>
      <main>
        <router-outlet></router-outlet>
      </main>
    </ng-container>
  `,
  styles: [``]
})
export class AppComponent implements OnInit {
  isLoggedIn = false;

  ngOnInit(): void {
    this.updateAuth();
    window.addEventListener('storage', () => this.updateAuth());
    window.addEventListener('authchange', () => this.updateAuth());
  }

  updateAuth(){
    this.isLoggedIn = !!sessionStorage.getItem('access_token');
  }

  onLoggedIn(){
    this.updateAuth();
  }
}
