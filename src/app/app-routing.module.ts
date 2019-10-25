import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { VariaveisComponent } from './variaveis/variaveis.component';

const routes: Routes = [
  { path: 'variaveis', component: VariaveisComponent },
  { path: '', redirectTo: 'variaveis', pathMatch: 'full' }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule {}
