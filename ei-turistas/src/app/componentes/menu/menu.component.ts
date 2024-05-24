import { Component } from '@angular/core';
import { RouterLink, RouterOutlet } from '@angular/router';

@Component({
  selector: 'app-menu',
  standalone: true,
  imports: [RouterOutlet, RouterLink],
  templateUrl: './menu.component.html',
  styleUrls: [
    './menu.component.css',
    '../../../assets/style/cores.css',
    '../../../assets/style/global.css'
  ]
})
export class MenuComponent {

}
