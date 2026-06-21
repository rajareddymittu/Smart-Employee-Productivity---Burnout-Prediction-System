import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, Router } from '@angular/router';

@Component({
  standalone: true,
  selector: 'app-navbar',
  imports: [CommonModule, RouterModule],
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.css']
})
export class NavbarComponent implements OnInit {
  isLogged = false;
  username?: string;
  roles: string[] = [];

  constructor(private router: Router) {}

  ngOnInit(){
    this.updateAuth();
    window.addEventListener('storage', () => this.updateAuth());
  }

  updateAuth(){
    const token = sessionStorage.getItem('access_token');
    this.isLogged = !!token;
    this.username = sessionStorage.getItem('username') || undefined;
    try{ this.roles = JSON.parse(sessionStorage.getItem('roles')||'[]'); }catch(e){ this.roles = []; }
  }

  logout(){
    sessionStorage.removeItem('access_token');
    sessionStorage.removeItem('username');
    sessionStorage.removeItem('roles');
    this.updateAuth();
    // notify root component and navigate to root (which shows login when unauthenticated)
    window.dispatchEvent(new Event('authchange'));
    this.router.navigate(['/']);
  }
}
