import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable, BehaviorSubject, throwError } from 'rxjs';
import { catchError, tap, shareReplay } from 'rxjs/operators';
import { WeatherResponse, CitySearchResult } from '../models/weather.model';

@Injectable({
  providedIn: 'root'
})
export class WeatherService {
  private readonly API_URL = 'http://localhost:8000/api';
  
  // État global de l'application
  private weatherSubject = new BehaviorSubject<WeatherResponse | null>(null);
  public weather$ = this.weatherSubject.asObservable();
  
  private loadingSubject = new BehaviorSubject<boolean>(false);
  public loading$ = this.loadingSubject.asObservable();
  
  private errorSubject = new BehaviorSubject<string | null>(null);
  public error$ = this.errorSubject.asObservable();

  constructor(private http: HttpClient) {}

  /**
   * Récupère la météo par nom de ville
   */
  getWeatherByCity(city: string): Observable<WeatherResponse> {
    this.loadingSubject.next(true);
    this.errorSubject.next(null);
    
    const params = new HttpParams().set('city', city);
    
    return this.http.get<WeatherResponse>(`${this.API_URL}/weather`, { params })
      .pipe(
        tap(data => {
          this.weatherSubject.next(data);
          this.loadingSubject.next(false);
        }),
        catchError(error => {
          this.loadingSubject.next(false);
          const errorMsg = error.error?.detail || 'Impossible de récupérer la météo';
          this.errorSubject.next(errorMsg);
          return throwError(() => new Error(errorMsg));
        }),
        shareReplay(1)
      );
  }

  /**
   * Récupère la météo par coordonnées GPS
   */
  getWeatherByCoordinates(lat: number, lon: number): Observable<WeatherResponse> {
    this.loadingSubject.next(true);
    this.errorSubject.next(null);
    
    const params = new HttpParams()
      .set('lat', lat.toString())
      .set('lon', lon.toString());
    
    return this.http.get<WeatherResponse>(`${this.API_URL}/weather`, { params })
      .pipe(
        tap(data => {
          this.weatherSubject.next(data);
          this.loadingSubject.next(false);
        }),
        catchError(error => {
          this.loadingSubject.next(false);
          const errorMsg = error.error?.detail || 'Impossible de récupérer la météo';
          this.errorSubject.next(errorMsg);
          return throwError(() => new Error(errorMsg));
        }),
        shareReplay(1)
      );
  }

  /**
   * Recherche de villes pour l'autocomplétion
   */
  searchCities(query: string, limit: number = 5): Observable<any> {
    if (query.length < 2) {
      return new Observable(observer => {
        observer.next({ results: [] });
        observer.complete();
      });
    }
    
    const params = new HttpParams()
      .set('q', query)
      .set('limit', limit.toString());
    
    return this.http.get<any>(`${this.API_URL}/search`, { params })
      .pipe(
        catchError(error => {
          console.error('Erreur recherche villes:', error);
          return throwError(() => error);
        })
      );
  }

  /**
   * Détecte la position géographique de l'utilisateur
   */
  getUserLocation(): Promise<GeolocationPosition> {
    return new Promise((resolve, reject) => {
      if (!navigator.geolocation) {
        reject(new Error('Géolocalisation non supportée'));
        return;
      }
      
      navigator.geolocation.getCurrentPosition(
        position => resolve(position),
        error => {
          let message = 'Erreur de géolocalisation';
          switch(error.code) {
            case error.PERMISSION_DENIED:
              message = 'Permission de géolocalisation refusée';
              break;
            case error.POSITION_UNAVAILABLE:
              message = 'Position indisponible';
              break;
            case error.TIMEOUT:
              message = 'Délai de géolocalisation dépassé';
              break;
          }
          reject(new Error(message));
        },
        { enableHighAccuracy: true, timeout: 5000, maximumAge: 0 }
      );
    });
  }

  /**
   * Charge la météo via géolocalisation
   */
  async loadWeatherByGeolocation(): Promise<void> {
    try {
      const position = await this.getUserLocation();
      this.getWeatherByCoordinates(
        position.coords.latitude,
        position.coords.longitude
      ).subscribe();
    } catch (error: any) {
      this.errorSubject.next(error.message);
      throw error;
    }
  }

  /**
   * Réinitialise l'état
   */
  clearError(): void {
    this.errorSubject.next(null);
  }

  clearWeather(): void {
    this.weatherSubject.next(null);
  }
}