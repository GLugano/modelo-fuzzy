import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';

@Injectable({ providedIn: 'root' })
export class HttpService {
  baseUrl = 'http://127.0.0.1:8000';

  constructor(private http: HttpClient) { }

  route(route: string) {
    if (route.indexOf('http://') === -1 && route.indexOf('https://') === -1) {
      route = `${this.baseUrl}/${route}`;
    }

    let headers: HttpHeaders = new HttpHeaders();

    const httpOptions = { headers };

    return {
      get: (data?: any) => {
        let mappedParams = '';

        if (data) {
          mappedParams = '?';
          for (const key in data) {
            if (data.hasOwnProperty(key)) {
              if (mappedParams && mappedParams.length > 1) {
                mappedParams = '&';
              }
              mappedParams += `${key}=${data[key]} `;
            }
          }
        }

        return this.http.get(`${route}${mappedParams}`, httpOptions);
      },
      post: (body: any) => this.http.post(`${route}`, body, httpOptions),
      delete: (id: any) => this.http.delete(`${route}/${id}`, httpOptions),
      put: (id: number, body: any) => this.http.put(`${route}/${id}`, body, httpOptions),
    }
  }
}