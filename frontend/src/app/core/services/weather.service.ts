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
  
  // Global state management
  private weatherSubject = new BehaviorSubject<WeatherResponse | null>(null);
  public weather$ = this.weatherSubject.asObservable();
  
  private loadingSubject = new BehaviorSubject<boolean>(false);
  public loading$ = this.loadingSubject.asObservable();
  
  private errorSubject = new BehaviorSubject<string | null>(null);
  public error$ = this.errorSubject.asObservable();

  constructor(private http: HttpClient) {}

  /**
   * Weather retrieval by city name
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
          const errorMsg = error.error?.detail || 'Unable to retrieve weather data';
          this.errorSubject.next(errorMsg);
          return throwError(() => new Error(errorMsg));
        }),
        shareReplay(1)
      );
  }

  /**
   * Weather retrieval by GPS coordinates
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
          const errorMsg = error.error?.detail || 'Unable to retrieve weather data';
          this.errorSubject.next(errorMsg);
          return throwError(() => new Error(errorMsg));
        }),
        shareReplay(1)
      );
  }

  /**
   * Search for cities matching the query
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
          console.error('Error searching cities:', error);
          return throwError(() => error);
        })
      );
  }

  /**
   * DDetects the user's geographic location
   */
  getUserLocation(): Promise<GeolocationPosition> {
    return new Promise((resolve, reject) => {
      if (!navigator.geolocation) {
        reject(new Error('Geolocation not supported'));
        return;
      }
      
      console.log('Requesting geolocation...');
      navigator.geolocation.getCurrentPosition(
        position => {
          console.log('Geolocation success:', position);
          resolve(position);
        },
        error => {
          console.error('Geolocation error code:', error.code, 'message:', error.message);
          let message = 'Geolocation error';
          switch(error.code) {
            case error.PERMISSION_DENIED:
              message = 'Geolocation permission denied';
              break;
            case error.POSITION_UNAVAILABLE:
              message = 'Position unavailable';
              break;
            case error.TIMEOUT:
              message = 'Geolocation request timeout';
              break;
          }
          reject(new Error(message));
        },
        { timeout: 5000 }
      );
    });
  }

  /**
   * Wather retrieval using geolocation
   */
  async loadWeatherByGeolocation(): Promise<void> {
    try {
      const position = await this.getUserLocation();
      console.log('Got position:', position.coords.latitude, position.coords.longitude);
      
      // Subscribe to the weather request and handle both success and error
      this.getWeatherByCoordinates(
        position.coords.latitude,
        position.coords.longitude
      ).subscribe({
        next: (data) => {
          console.log('Weather loaded successfully:', data);
        },
        error: (error) => {
          console.error('Error loading weather by coordinates:', error);
          this.errorSubject.next(error.message);
        }
      });
    } catch (error: any) {
      console.error('Geolocation error in loadWeatherByGeolocation:', error);
      this.errorSubject.next(error.message);
      throw error;
    }
  }

  /**
   * Resets the state
   */
  clearError(): void {
    this.errorSubject.next(null);
  }

  clearWeather(): void {
    this.weatherSubject.next(null);
  }
}