import { Routes } from '@angular/router';
import { HomeComponent } from './pages/home/home.component';
import { BuscadorAtivoComponent } from './pages/buscador-ativo/buscador-ativo.component';

export const routes: Routes = [
    {
        path:'',
        redirectTo:'/home',
        pathMatch:'full'
    },
    {
        path:'home',
        component: HomeComponent
    },
    {
        path:'buscar',
        component: BuscadorAtivoComponent
    }
];
