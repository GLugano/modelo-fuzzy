import { Component, ViewChild, OnDestroy } from '@angular/core';
import { FormBuilder, NgForm, Validators } from '@angular/forms';
import { MatTableDataSource } from '@angular/material';
import { HttpService } from '../services/http.service';
import { Subscription } from 'rxjs';

@Component({
  selector: 'app-regras',
  templateUrl: './regras.component.html',
  styleUrls: ['./regras.component.scss']
})
export class RegrasComponent implements OnDestroy {
  @ViewChild('f', { static: true }) formValores: NgForm;

  formGroupRegra = this.formBuilder.group({
    descricao: ['', Validators.required]
  });

  displayedColumnsList: string[] = ['id', 'descricao'];
  dataSourceList = new MatTableDataSource<any>();

  regraRequest: Subscription;

  selectedTab = 0;

  constructor(public formBuilder: FormBuilder, private http: HttpService) {
    this.getRules();
  }

  ngOnDestroy() {
    if (this.regraRequest) {
      this.regraRequest.unsubscribe();
    }
  }

  getRules() {
    this.regraRequest = this.http.route('regra/').get().subscribe((response: any[]) => {
      this.dataSourceList.data = response;
      this.selectedTab = 0;
    });
  }

  saveRule() {
    const formDataVariavel = this.formGroupRegra.getRawValue();

    this.http.route('regra/').post(formDataVariavel).subscribe((response) => {
      this.getRules();
    }, (error) => {
      console.warn(error);
    });
  }
}
