import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private apiUrl = 'http://localhost:8000';

  constructor() { }

  login(email: string, password: string) {
    return fetch(`${this.apiUrl}/users/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email, password })
    }).then(res => res.json());
  }

  getToken(): string | null {
    return localStorage.getItem('access_token');
  }

  setToken(token: string, role: string): void {
    localStorage.setItem('access_token', token);
    localStorage.setItem('role', role);
  }

  setName(name: string): void {
    localStorage.setItem('user_name', name);
  }

  getName(): string | null {
    return localStorage.getItem('user_name');
  }

  getRole(): string | null {
    return localStorage.getItem('role');
  }

  logout(): void {
    localStorage.removeItem('access_token');
    localStorage.removeItem('role');
    localStorage.removeItem('user_name');
    localStorage.removeItem('user_id');
  }

  isAuthenticated(): boolean {
    return !!this.getToken();
  }
}
