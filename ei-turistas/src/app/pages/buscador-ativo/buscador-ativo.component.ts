import { Component } from '@angular/core';
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
  abrirFrase: boolean = true;
  abrirModalFormulario: boolean = false;
  abrirResultadoLocalidade: boolean = false;
  resultLocalidade: LocalidadeI = {};
  cardsDepoimentos: DepoimentoI[] = [];
  tiposDepoimentos: any[] = [];
  tipoDepoimentoSelecionado: string = ''; 

  constructor(
    private formBuilder: FormBuilder,
    public loadingService: LoadingService,
    private buscadorService: BuscadorService,
    private StorageAvaliacao: StorageAvaliacao
  ) { }

  formBuscarLocalidade = this.formBuilder.group({
    localidade: ['', Validators.required]
  });

  get localidade() {
    return this.formBuscarLocalidade.get('localidade')?.value;
  }

  ngOnInit() {
    const respFormulario = this.StorageAvaliacao.getAcaoFormulario();
    if (respFormulario == 'fechar modal') {
      this.abrirModalFormulario = false;
    }
  }

  public btnLocalidade(): void {
    if (this.localidade != null) {
      this.loadingService.show();
      this.buscadorService.getLocalidade(this.localidade)?.subscribe({
        next: (value: any) => {
          console.log('ok')
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
          this.abrirFrase = false;
          this.abrirResultadoLocalidade = true;
          this.loadingService.hide();
        }
      })
    }
  }

  public filtrarTodosPorLocalidade(): void {
    let idLocalidade = this.resultLocalidade.id
    this.tipoDepoimentoSelecionado = '';
    if (idLocalidade != null) {
      this.buscadorService.getFiltrarTodosDepoimentosPorLocalidade(idLocalidade)
        .subscribe({
          next: (value: any) => {
            console.log('ok')
            this.cardsDepoimentos = value;
          },
          error: (err: Error) => { },
          complete: () => { }
        })
    }
  }

  public filtroPorLocalidade(tipoSelecionado: any): void {
    let idLocalidade = this.resultLocalidade.id
    this.tipoDepoimentoSelecionado = tipoSelecionado;
    if (idLocalidade != null) {
      this.buscadorService.getFiltrarPorTipoDepoimentoPorLocalidade(tipoSelecionado, idLocalidade)
        .subscribe({
          next: (value: any) => {
            console.log('ok')
            this.cardsDepoimentos = value;
          },
          error: (err: Error) => { },
          complete: () => { }
        })
    }
  }

  private extractUniqueTipos(depoimentos: DepoimentoI[]): string[] {
    const tipos = depoimentos.map(d => d.tipo_depoimento).filter((tipo): tipo is string => typeof tipo === 'string');
    return Array.from(new Set(tipos));
  }

  public abrirFormulario(): void {
    this.abrirModalFormulario = true;
    this.StorageAvaliacao.setTipoAcao('cadastrar')

    let id = this.resultLocalidade.id
    if (id != null) {
      this.StorageAvaliacao.setIdLocalidade(id)
    }
    this.renderizaParaModal();
  }

  public editarFormulario(cardDepoimento: DepoimentoI): void {
    this.abrirModalFormulario = true;
    this.StorageAvaliacao.setEditarCardDepoimento(cardDepoimento)
    this.StorageAvaliacao.setTipoAcao('editar')
    this.renderizaParaModal();
  }

  private renderizaParaModal():void{
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
        this.filtrarTodosPorLocalidade();
        // window.location.reload();
      },
      error: (err: Error) => { },
      complete: () => { }
    })
  }

  public closeModal(): void{
    this.abrirModalFormulario = false;
    this.filtrarTodosPorLocalidade();
  }

}
