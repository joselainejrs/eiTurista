import { ComponentFixture, TestBed } from '@angular/core/testing';

import { BuscadorAtivoComponent } from './buscador-ativo.component';

describe('BuscadorAtivoComponent', () => {
  let component: BuscadorAtivoComponent;
  let fixture: ComponentFixture<BuscadorAtivoComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [BuscadorAtivoComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(BuscadorAtivoComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
