import { Component, ViewChild, OnDestroy } from '@angular/core';
import { FormBuilder, NgForm, Validators } from '@angular/forms';
import { MatTableDataSource } from '@angular/material';
import { HttpService } from '../services/http.service';
import { Subscription } from 'rxjs';

@Component({
  selector: 'app-simulacao',
  templateUrl: './simulacao.component.html',
  styleUrls: ['./simulacao.component.scss']
})
export class SimulacaoComponent implements OnDestroy {
  formGroupRegra = this.formBuilder.group({
    descricao: ['', Validators.required]
  });

  variablesRequest: Subscription;

  selectedTab = 0;
  names: string[] = [];
  values: string[] = [];
  variables: any[] = [];

  constructor(public formBuilder: FormBuilder, private http: HttpService) {
    this.getVariables();
  }

  ngOnDestroy() {
    if (this.variablesRequest) {
      this.variablesRequest.unsubscribe();
    }
  }

  getVariables() {
    this.variablesRequest = this.http.route('variavel/').get().subscribe((response: any[]) => {
      this.variables = response;
      this.selectedTab = 0;

      this.variables.forEach((variable) => {
        if (variable.flObjetivo) {
          this.names.push(variable.nome);
          this.values.push(null);
        }
      });
    });
  }

  trackByItems(el: any): number { return el.id; }

  simulate() {
    let params: any = {};

    this.values.forEach((variable, i) => {
      params[this.names[i]] = this.values[i];
    });

    this.http.route('simular/').post(params).subscribe((response: any[]) => {
    });
  }
}
