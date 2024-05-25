import { Component, EventEmitter, Input, Output } from '@angular/core';
import { MenuComponent } from '../../componentes/menu/menu.component';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { ModalComponent } from '../../componentes/modal/modal.component';
import { BuscadorService } from '../../services/pages/buscador/buscador.service';
import { LoadingService } from '../../services/loading-spinner/loading-spinner';
import { LocalidadeI } from '../../interface/localidade';
import { DepoimentoI } from '../../interface/departamento';
import { StorageAvaliacao } from '../../services/pages/storage-avaliacao/storage-avaliacao';

@Component({
  selector: 'app-buscador-ativo',
  standalone: true,
  imports: [
      MenuComponent, 
      ModalComponent, 
      CommonModule, 
      ReactiveFormsModule,
    ],
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
  resultLocalidade: LocalidadeI = {};
  cardsDepoimentos: DepoimentoI[] = [];
  tiposDepoimentos: string[] = [];
  todosTiposAvaliacao: string[] = [];

  constructor(
    private formBuilder: FormBuilder,
    public loadingService: LoadingService,
    private buscadorService: BuscadorService,
    private StorageAvaliacao: StorageAvaliacao
  ) { }

  formSelect = this.formBuilder.group({
    todos: [this.todosTiposAvaliacao],
    tipo: [this.tiposDepoimentos]
  });

  formBuscarLocalidade = this.formBuilder.group({
    localidade: ['', Validators.required]
  });
  
  get localidade() {
    return this.formBuscarLocalidade.get('localidade')?.value;
  }

  ngOnInit() {
    const respFormulario = this.StorageAvaliacao.getAcaoFormulario();
    if(respFormulario == 'fechar modal'){
      this.abrirModalFormulario = false;
    }
  }

  public btnLocalidade(): void{
    // debugger
    if (this.localidade != null) {
      this.loadingService.show(); 
      this.buscadorService.getLocalidade(this.localidade)?.subscribe({
        next: (value: any) => {
          console.log(value)
          this.resultLocalidade = value.localidade;
          this.abrirModalFormulario = false;

          if (value.depoimentos && Array.isArray(value.depoimentos)) {
            this.cardsDepoimentos = value.depoimentos;
            this.tiposDepoimentos = this.extractUniqueTipos(this.cardsDepoimentos);
          } else {
            console.error('Depoimentos não encontrados ou não são um array.');
            this.cardsDepoimentos = [];
            this.tiposDepoimentos = []; 
          }
        },
        error: (err: Error) => { 
          console.log(err)
          this.loadingService.hide(); 
        },
        complete: () => { 
          this.abrirResultadoLocalidade = true; 
          this.loadingService.hide();
        }
      })
    }
  }

  private extractUniqueTipos(depoimentos: DepoimentoI[]): string[] {
    const tipos = depoimentos.map(d => d.tipoDepoimento).filter((tipo): tipo is string => typeof tipo === 'string');
    return Array.from(new Set(tipos));
  }

  public abrirFormulario(): void {
    this.abrirModalFormulario = true;

    let id = this.resultLocalidade.id
    if(id != null){
      this.StorageAvaliacao.setIdLocalidade(id)
    }
    
    setTimeout(() => {
      const modalElement = document.getElementById('modalFormulario');
      if (modalElement) {
        modalElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    }, 0);
  }

  public editarFormulario(cardDepoimento: DepoimentoI): void {
    this.abrirModalFormulario = true;
    this.StorageAvaliacao.setEditarCardDepoimento(cardDepoimento)
    this.StorageAvaliacao.setTipoAcao('editar')

    setTimeout(() => {
      const modalElement = document.getElementById('modalFormulario');
      if (modalElement) {
        modalElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    }, 0);
  }

  public excluirAvaliacao(id: number): void {
    this.buscadorService.deleteDepoimento(id)?.subscribe({
      next: (value: any) => {
        console.log('ok')
      },
      error: (err: Error) => {},
      complete: () => {}
    })
  }

}
