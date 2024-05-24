import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [],
  templateUrl: './home.component.html',
  styleUrls: [
    './home.component.css',
    '../../../assets/style/cores.css',
    '../../../assets/style/global.css'
  ]
})
export class HomeComponent {

  constructor(
    private router: Router,
  ) { }

  public pesquisaEDireciona(): void{
    this.router.navigate(["/buscar"]);
  }
}
