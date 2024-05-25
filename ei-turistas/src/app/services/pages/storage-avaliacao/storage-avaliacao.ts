import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';
import { DepoimentoI } from '../../../interface/departamento';

@Injectable({
  providedIn: 'root'
})
export class StorageAvaliacao {
  cardDepoimento!: DepoimentoI;
  tipoDeAcao!: string;
  acaoFormulario!: string;
  idLocalidade!: number;

  constructor() { }

  public setEditarCardDepoimento(depoimento: DepoimentoI) {
    this.cardDepoimento = depoimento;
  }

  public getEditarCardDepoimento() {
    return this.cardDepoimento;
  }

  public setTipoAcao(acao: string) {
    this.tipoDeAcao = acao;
  }

  public getTipoAcao() {
    return this.tipoDeAcao;
  }

  public setIdLocalidade(id: number) {
    this.idLocalidade = id;
  }

  public getIdLocalidade() {
    return this.idLocalidade;
  }

  public setAcaoFormulario(acao: string) {
    this.acaoFormulario = acao;
  }

  public getAcaoFormulario() {
    return this.acaoFormulario;
  }

}
