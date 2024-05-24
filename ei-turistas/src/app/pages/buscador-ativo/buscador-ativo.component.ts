import { Component } from '@angular/core';
import { MenuComponent } from '../../componentes/menu/menu.component';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { ModalComponent } from '../../componentes/modal/modal.component';
import { BuscadorService } from '../../services/pages/buscador/buscador.service';
import { NgxSpinnerService } from 'ngx-spinner';

@Component({
  selector: 'app-buscador-ativo',
  standalone: true,
  imports: [MenuComponent, ModalComponent, CommonModule, ReactiveFormsModule],
  templateUrl: './buscador-ativo.component.html',
  styleUrls: [
    './buscador-ativo.component.css',
    '../../../assets/style/cores.css',
    '../../../assets/style/global.css',
    '../../../assets/style/depoimento.css',
    '../../../assets/style/campo-previsao.css',
  ]
})
export class BuscadorAtivoComponent {
  abrirModalFormulario: boolean = false;
  abrirResultadoLocalidade: boolean = false;
  resultLocalidade: any = false;

  tiposDepoimentos = [
    { nome: 'Restaurante', value: 'Restaurante' },
    { nome: 'Hotel', value: 'Hotel' },
    { nome: 'Passeios', value: 'Passeios' },
  ]

  cardsDepoimentos = [
    { nome: 'Restaurante' },
    { nome: 'Hotel' },
    { nome: 'Passeios' },
    { nome: 'Passeios' },
    { nome: 'Passeios' },
  ]

  constructor(
    private formBuilder: FormBuilder,
    private spinner: NgxSpinnerService,
    private buscadorService: BuscadorService
  ) { }

  formSelect = this.formBuilder.group({
    state: [this.tiposDepoimentos]
  });

  formBuscarLocalidade = this.formBuilder.group({
    localidade: ['', Validators.required]
  });
  
  get localidade() {
    return this.formBuscarLocalidade.get('localidade')?.value;
  }

  public btnLocalidade(): void{
    debugger
    if (this.localidade != null) {
      this.buscadorService.getLocalidade(this.localidade)?.subscribe({
        next: (value: any) => {
          console.log(value)
          this.resultLocalidade = value;
        },
        error: (err: Error) => {  },
        complete: () => { 
          this.abrirResultadoLocalidade = true; 
        }
      })
    }
  }

  public abrirFormulario(): void {
    this.abrirModalFormulario = true;

    setTimeout(() => {
      const modalElement = document.getElementById('modalFormulario');
      if (modalElement) {
        modalElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    }, 0);
  }

  public editarFormulario(): void {
    this.abrirModalFormulario = true;

    setTimeout(() => {
      const modalElement = document.getElementById('modalFormulario');
      if (modalElement) {
        modalElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    }, 0);
  }

  public excluirAvaliacao(): void {

  }

}
