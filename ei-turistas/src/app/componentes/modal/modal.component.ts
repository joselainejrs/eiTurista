import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { FormBuilder, ReactiveFormsModule } from '@angular/forms';

@Component({
  selector: 'app-modal',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './modal.component.html',
  styleUrl: './modal.component.css'
})
export class ModalComponent {
  tipos = [
    { nome:'Restaurante', value: 'Restaurante'},
    { nome:'Hotel', value: 'Hotel'},
    { nome:'Passeios', value: 'Passeios'},
  ]

  constructor(
    private formBuilder: FormBuilder,
    ) { }

  tipoAvaliacao = this.formBuilder.group({
    state: [this.tipos]
  });
}
