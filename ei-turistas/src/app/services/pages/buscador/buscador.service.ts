import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class BuscadorService {

  urlBase: string = 'http://localhost:5000/localidade/';

  constructor(private http: HttpClient) { }

  public getLocalidade(localidade: string): Observable<any>{
    return this.http.get(`${this.urlBase}+${localidade}`)
  }
}
