import { CommonModule } from '@angular/common';
import { ChangeDetectorRef, Component, EventEmitter, OnInit, Output } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { StorageAvaliacao } from '../../services/pages/storage-avaliacao/storage-avaliacao';
import { DepoimentoI } from '../../interface/departamento';
import { BuscadorService } from '../../services/pages/buscador/buscador.service';

@Component({
  selector: 'app-modal',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './modal.component.html',
  styleUrl: './modal.component.css'
})
export class ModalComponent implements OnInit {
  acao: string = '';
  depoimento!: DepoimentoI;
  @Output() openClose = new EventEmitter()

  avaliacao = this.formBuilder.group({
    tipo: ["", Validators.required],
    detalhes: ["", Validators.required],
  });

  constructor(
    private cdr: ChangeDetectorRef,
    private formBuilder: FormBuilder,
    private buscarService: BuscadorService,
    private StorageAvaliacao: StorageAvaliacao
  ) { }

  get tipo() {
    return this.avaliacao.get('tipo')?.value
  }
  get detalhes() {
    return this.avaliacao.get('detalhes')?.value
  }

  ngOnInit() {
    this.depoimento = this.StorageAvaliacao.getEditarCardDepoimento();
    this.acao = this.StorageAvaliacao.getTipoAcao();

    if (this.acao == "editar") {
      this.avaliacao.patchValue({
        tipo: this.depoimento.tipoDepoimento,
        detalhes: this.depoimento.detalhes
      });
    }
  }

  fecharModal(){
    this.openClose.emit();
  }

  public registrarAvaliacao(): void {
    if (this.acao == "editar") {
      let id = this.depoimento.idDepoimento;
      if (id != null) { this.editarRegistro(id) }

    } else {
      let idLocalidade: number = this.StorageAvaliacao.getIdLocalidade()
      if (idLocalidade != null) { this.salvarRegistro(idLocalidade) }
    }
  }

  private editarRegistro(id: number): void {
    if (this.tipo != null && this.detalhes != null) {
      this.buscarService.patchDepoimento(id, this.tipo, this.detalhes).subscribe({
        next: (value: any) => {
          this.acaoDeSucessoNoregistro();
        },
        error(err) { },
        complete() { },
      })
    }
  }
  private salvarRegistro(id: number): void {
    if (this.tipo != null && this.detalhes != null) {
      this.buscarService.postDepoimento(id, this.tipo, this.detalhes).subscribe({
        next: (value: any) => {
          this.acaoDeSucessoNoregistro();
        },
        error(err) { },
        complete() { },
      })
    }
  }

  private acaoDeSucessoNoregistro(): void {
    this.avaliacao.reset();
    this.cdr.detectChanges();
    this.StorageAvaliacao.setAcaoFormulario('fechar modal')
  }

}