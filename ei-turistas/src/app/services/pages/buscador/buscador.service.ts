import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class BuscadorService {

  urlBase: string = 'http://localhost:5000/localidade/';
  urlAvaliacao: string = 'http://localhost:5000/avaliacao';

  constructor(private http: HttpClient) { }

  public getLocalidade(localidade: string): Observable<any> {
    return this.http.get(`${this.urlBase}${localidade}`)
  }

  public getFiltrarPorTipoDepoimentoPorLocalidade(tipo: string, idLocalidade: number): Observable<any> {
    return this.http.get(`${this.urlAvaliacao}/tipo/${tipo}/localidade/${idLocalidade}`)
  }

  public getFiltrarTodosDepoimentosPorLocalidade(idLocalidade: number): Observable<any> {
    return this.http.get(`${this.urlAvaliacao}/localidade/${idLocalidade}`)
  }

  public postDepoimento(id_localidade: number, tipo_depoimento: string, detalhes: string): Observable<any> {
    const payload = {
      id_localidade: id_localidade,
      tipo_depoimento: tipo_depoimento,
      detalhes: detalhes
    }

    return this.http.post(`${this.urlAvaliacao}`, payload)
  }

  public patchDepoimento(id: number, tipoAvaliacao: string, detalhes: string): Observable<any> {
    const payload = {
      tipo_depoimento: tipoAvaliacao,
      detalhes: detalhes
    }

    return this.http.patch(`${this.urlAvaliacao}/${id}`, payload)
  }

  public deleteDepoimento(id: number): Observable<any> {
    return this.http.delete(`${this.urlAvaliacao}/${id}`)
  }
}
