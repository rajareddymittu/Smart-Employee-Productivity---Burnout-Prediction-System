import { ApplicationConfig, importProvidersFrom } from '@angular/core';
import { provideZoneChangeDetection } from '@angular/core';
import { provideRouter } from '@angular/router';
import { provideHttpClient } from '@angular/common/http';
import { DashboardComponent } from './dashboard.component';
import { EmployeesComponent } from './employees.component';
import { PredictComponent } from './predict.component';
import { LoginComponent } from './login.component';
import { WorklogComponent } from './worklog.component';
import { ReporteesComponent } from './reportees.component';
import { HrComponent } from './hr.component';

const routes = [
  { path: '', component: DashboardComponent },
  { path: 'employees', component: EmployeesComponent },
  { path: 'predict', component: PredictComponent },
  { path: 'worklog', component: WorklogComponent },
  { path: 'reportees', component: ReporteesComponent },
  { path: 'hr', component: HrComponent },
  { path: 'login', component: LoginComponent },
];

export const appConfig: ApplicationConfig = {
  providers: [
    provideZoneChangeDetection({ eventCoalescing: true }),
    provideRouter(routes),
    provideHttpClient(),
  ]
};
