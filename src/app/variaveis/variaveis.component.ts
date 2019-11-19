import { Component, ViewChild, OnDestroy } from '@angular/core';
import { FormBuilder, NgForm, Validators } from '@angular/forms';
import { MatTableDataSource } from '@angular/material';
import { HttpService } from '../services/http.service';
import { Subscription, Observable, zip } from 'rxjs';

@Component({
  selector: 'app-variaveis',
  templateUrl: './variaveis.component.html',
  styleUrls: ['./variaveis.component.scss']
})
export class VariaveisComponent implements OnDestroy {
  @ViewChild('f', { static: true }) formValores: NgForm;

  formGroupVariavel = this.formBuilder.group({
    id: [null],
    tipo: [1, Validators.required],
    nome: ['', Validators.required]
  });
  formGroupAtributos = this.formBuilder.group({
    nome: [null, Validators.required],
    suporteIni: [null, Validators.required],
    suporteFim: [null, Validators.required],
    nucleoIni: [null, Validators.required],
    nucleoFim: [null, Validators.required]
  });
  displayedColumns: string[] = ['id', 'valor', 'suporte', 'nucleo', 'actions'];
  dataSource = new MatTableDataSource<any>();

  displayedColumnsList: string[] = ['id', 'nome', 'actions'];
  dataSourceList = new MatTableDataSource<any>();

  charts: string[];

  variablesRequest: Subscription;

  selectedTab = 0;

  constructor(public formBuilder: FormBuilder, private http: HttpService) {
    this.getVariables();
    this.getCharts();
  }

  ngOnDestroy() {
    if (this.variablesRequest) {
      this.variablesRequest.unsubscribe();
    }
  }

  getVariables() {
    this.variablesRequest = this.http.route('variavel/').get().subscribe((response: any[]) => {
      this.dataSourceList.data = response;
      this.selectedTab = 0;
    });
  }

  addValue(): void {
    if (this.formGroupAtributos.invalid) {
      return;
    }

    let max = 0;

    this.dataSource.data.forEach(el => {
      if (el.id > max) {
        max = el.id;
      }
    });

    const data = this.formGroupAtributos.getRawValue();
    data.id = max + 1;
    this.dataSource.data = [...this.dataSource.data, data];
    this.formGroupAtributos.reset();
    this.formValores.resetForm();

    Object.keys(this.formGroupAtributos.controls).forEach(key => {
      this.formGroupAtributos.controls[key].setErrors(null);
    });
  }

  save() {
    const formDataVariavel = this.formGroupVariavel.getRawValue();
    let formDataAtributos: any[] = this.dataSource.data.map((data) => {
      let returnObj: any = {
        fimBase: data.suporteFim,
        fimNucleo: data.nucleoFim,
        inicioBase: data.suporteIni,
        inicioNucleo: data.nucleoIni,
        nome: data.nome
      };

      if (data.id) {
        returnObj.id = data.id;
      }

      return returnObj;
    });

    const data: any = {
      nome: formDataVariavel.nome,
      flObjetivo: formDataVariavel.tipo === 2,
      atributos: formDataAtributos
    };

    let obs: Observable<any>;

    if (formDataVariavel.id) {
      data.id = formDataVariavel.id;
      obs = this.http.route('cadastro').put(data.id, data);
    } else {
      obs = zip(
        this.http.route('atributo').post(formDataAtributos),
        this.http.route('variavel').post({
          nome: formDataVariavel.nome,
          flObjetivo: formDataVariavel.tipo === 2,
        }),
      );
    }

    obs.subscribe(() => {
      this.dataSource.data = [];
      this.formGroupVariavel.reset();
      this.formGroupAtributos.reset();
      this.getVariables();
      this.getCharts();
    }, (error) => {
      console.warn(error);
    });
  }

  edit(element: any) {
    this.formGroupVariavel.get('id').setValue(element.id);
    this.formGroupVariavel.get('nome').setValue(element.nome);
    this.formGroupVariavel.get('tipo').setValue(element.flObjetivo ? 2 : 1);

    this.dataSource.data = element.atributos.map((el) => ({
      suporteFim: el.fimBase,
      nucleoFim: el.fimNucleo,
      suporteIni: el.inicioBase,
      nucleoIni: el.inicioNucleo,
      nome: el.nome,
      id: el.id,
    }));

    this.selectedTab = 1;
  }

  remove(id: number) {
    this.http.route('variavel').delete(id).subscribe((response) => {
      this.getVariables();
      this.getCharts();
    }, (error) => {
      console.warn(error);
    });
  }

  removeValue(element: any) {
    this.dataSource.data = this.dataSource.data.filter((el: any) => el.nome !== el.nome);
  }

  getCharts() {
    this.http.route('graficos').get().subscribe((response: string[]) => {
      this.charts = response.map((chart) => `data:image/png;base64,${chart}`);
    }, (error) => {
      console.warn(error);
    });
  }
}
