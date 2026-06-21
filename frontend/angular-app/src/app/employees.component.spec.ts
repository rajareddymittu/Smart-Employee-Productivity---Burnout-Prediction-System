import { TestBed } from '@angular/core/testing';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { EmployeesComponent } from './employees.component';
import { ApiService } from './services/api.service';

describe('EmployeesComponent', () => {
  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [EmployeesComponent, HttpClientTestingModule],
      providers: [ApiService]
    }).compileComponents();
  });

  it('creates', () => {
    const fixture = TestBed.createComponent(EmployeesComponent);
    expect(fixture.componentInstance).toBeTruthy();
  });
});
