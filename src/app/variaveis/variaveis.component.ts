import { Component, ViewChild, OnInit } from '@angular/core';
import { FormBuilder, Validators, NgForm, FormGroup } from '@angular/forms';
import { MatTableDataSource } from '@angular/material';

@Component({
  selector: 'app-variaveis',
  templateUrl: './variaveis.component.html',
  styleUrls: ['./variaveis.component.scss']
})
export class VariaveisComponent implements OnInit {
  @ViewChild('f', { static: true }) formValores: NgForm;

  formGroupVariavel = this.formBuilder.group({
    tipo: [1, Validators.required],
    nome: ['', Validators.required]
  });
  formGroupValores = this.formBuilder.group({
    nome: [null, Validators.required],
    baseIni: [0, Validators.required],
    baseFim: [0, Validators.required],
    nucleoIni: [0, Validators.required],
    nucleoFim: [0, Validators.required]
  });
  displayedColumns: string[] = ['id', 'valor', 'base', 'nucleo', 'actions'];
  dataSource = new MatTableDataSource<any>();

  constructor(public formBuilder: FormBuilder) {}

  ngOnInit() {
    this.dataSource.data = [
      {
        id: 1,
        nome: 'Baixo',
        baseIni: 0,
        baseFim: 15,
        nucleoIni: 8,
        nucleoFim: 10
      }
    ];
  }

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
