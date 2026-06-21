import { TestBed } from '@angular/core/testing';
import { FormsModule } from '@angular/forms';
import { PredictComponent } from './predict.component';

describe('PredictComponent', () => {
  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [PredictComponent, FormsModule]
    }).compileComponents();
  });

  it('creates', () => {
    const fixture = TestBed.createComponent(PredictComponent);
    expect(fixture.componentInstance).toBeTruthy();
  });

  it('has Predict title', () => {
    const fixture = TestBed.createComponent(PredictComponent);
    fixture.detectChanges();
    expect(fixture.nativeElement.textContent).toContain('Predict Burnout');
  });
});
