import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClientModule } from '@angular/common/http';
import { Observable } from 'rxjs';

import { WeatherService } from './core/services/weather.service';
import { WeatherResponse } from './core/models/weather.model';
import { FavoritesUtil } from './shared/utils/favorites.util';

import { SearchComponent } from './features/search/search.component';
import { CurrentWeatherComponent } from './features/current-weather/current-weather.component';
import { HourlyForecastComponent } from './features/hourly-forecast/hourly-forecast.component';
import { DailyForecastComponent } from './features/daily-forecast/daily-forecast.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [
    CommonModule,
    HttpClientModule,
    SearchComponent,
    CurrentWeatherComponent,
    HourlyForecastComponent,
    DailyForecastComponent
  ],
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  weather$: Observable<WeatherResponse | null>;
  loading$: Observable<boolean>;
  error$: Observable<string | null>;
  hasNoFavorites = false;

  constructor(public weatherService: WeatherService) {
    this.weather$ = this.weatherService.weather$;
    this.loading$ = this.weatherService.loading$;
    this.error$ = this.weatherService.error$;
  }

  ngOnInit(): void {
    // Load favorite city on startup
    this.loadFavoriteCity();
  }

  loadFavoriteCity(): void {
    const favorite = FavoritesUtil.getFavorite();
    if (favorite) {
      this.onCitySelected(favorite.name);
      this.hasNoFavorites = false;
    } else {
      // No favorite saved - show message instead of trying geolocation
      this.hasNoFavorites = true;
    }
  }

  onCitySelected(city: string): void {
    this.weatherService.getWeatherByCity(city).subscribe();
  }

  clearError(): void {
    this.weatherService.clearError();
  }

  getTimeUntilExpiry(expiryDate?: string): string {
    if (!expiryDate) return '...';
    
    const now = new Date();
    const expiry = new Date(expiryDate);
    const diffMinutes = Math.floor((expiry.getTime() - now.getTime()) / 60000);
    
    if (diffMinutes < 1) return 'less than 1 minute';
    if (diffMinutes === 1) return '1 minute';
    return `${diffMinutes} minutes`;
  }
}