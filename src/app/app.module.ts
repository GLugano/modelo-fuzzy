import { HttpClientModule } from '@angular/common/http';
import { NgModule } from '@angular/core';
import { ReactiveFormsModule, FormsModule } from '@angular/forms';
import { MatButtonModule, MatFormFieldModule, MatIconModule, MatInputModule, MatSelectModule, MatTableModule, MatTabsModule, MatToolbarModule } from '@angular/material';
import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { VariaveisComponent } from './variaveis/variaveis.component';
import { RegrasComponent } from './regras/regras.component';
import { SimulacaoComponent } from './simulacao/simulacao.component';


@NgModule({
  imports: [
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    MatToolbarModule,
    MatButtonModule,
    MatFormFieldModule,
    MatInputModule,
    MatSelectModule,
    ReactiveFormsModule,
    MatTableModule,
    MatIconModule,
    MatTabsModule,
    HttpClientModule,
    FormsModule
  ],
  declarations: [
    AppComponent,
    VariaveisComponent,
    RegrasComponent,
    SimulacaoComponent
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
