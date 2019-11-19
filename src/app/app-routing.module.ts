import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { VariaveisComponent } from './variaveis/variaveis.component';
import { RegrasComponent } from './regras/regras.component';
import { SimulacaoComponent } from './simulacao/simulacao.component';

const routes: Routes = [
  { path: 'variaveis', component: VariaveisComponent },
  { path: 'regras', component: RegrasComponent },
  { path: 'simulacao', component: SimulacaoComponent },
  { path: '', redirectTo: 'variaveis', pathMatch: 'full' }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
