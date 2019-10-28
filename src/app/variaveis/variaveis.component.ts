import { Component, ViewChild } from '@angular/core';
import { FormBuilder, NgForm, Validators } from '@angular/forms';
import { MatTableDataSource } from '@angular/material';

@Component({
  selector: 'app-variaveis',
  templateUrl: './variaveis.component.html',
  styleUrls: ['./variaveis.component.scss']
})
export class VariaveisComponent {
  @ViewChild('f', { static: true }) formValores: NgForm;

  formGroupVariavel = this.formBuilder.group({
    tipo: [1, Validators.required],
    nome: ['', Validators.required]
  });
  formGroupValores = this.formBuilder.group({
    nome: [null, Validators.required],
    baseIni: [null, Validators.required],
    baseFim: [null, Validators.required],
    nucleoIni: [null, Validators.required],
    nucleoFim: [null, Validators.required]
  });
  displayedColumns: string[] = ['id', 'valor', 'base', 'nucleo', 'actions'];
  dataSource = new MatTableDataSource<any>();

  constructor(public formBuilder: FormBuilder) {}

  addValue(): void {
    if (this.formGroupValores.invalid) {
      return;
    }

    let max = 0;

    this.dataSource.data.forEach(el => {
      if (el.id > max) {
        max = el.id;
      }
    });

    const data = this.formGroupValores.getRawValue();
    data.id = max + 1;
    this.dataSource.data = [...this.dataSource.data, data];
    this.formGroupValores.reset();
    this.formValores.resetForm();

    Object.keys(this.formGroupValores.controls).forEach(key => {
      this.formGroupValores.controls[key].setErrors(null);
    });
  }
}
