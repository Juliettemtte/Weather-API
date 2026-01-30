import { Component, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { WeatherService } from '../../core/services/weather.service';
import { CitySearchResult } from '../../core/models/weather.model';
import { debounceTime, distinctUntilChanged, Subject, switchMap } from 'rxjs';

@Component({
  selector: 'app-search',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './search.component.html',
  styleUrls: ['./search.component.css']
})
export class SearchComponent {
  @Output() citySelected = new EventEmitter<string>();
  
  searchQuery = '';
  searchResults: CitySearchResult[] = [];
  showResults = false;
  isSearching = false;
  
  private searchSubject = new Subject<string>();
  private currentSearchQuery = '';

  constructor(private weatherService: WeatherService) {
    // Debounce to avoid too many requests (reduced to 100ms for faster updates)
    this.searchSubject.pipe(
      debounceTime(100),
      distinctUntilChanged(),
      switchMap(query => {
        this.currentSearchQuery = query;
        if (query.length < 2) {
          this.searchResults = [];
          this.showResults = false;
          return [];
        }
        this.isSearching = true;
        this.showResults = true;
        return this.weatherService.searchCities(query);
      })
    ).subscribe({
      next: (response) => {
        // Only update results if this response matches the current search query
        if (this.currentSearchQuery === this.searchQuery) {
          this.searchResults = response.results || [];
          this.showResults = true;
          this.isSearching = false;
        }
      },
      error: () => {
        this.isSearching = false;
        this.showResults = true;
      }
    });
  }

  onSearchInput(): void {
    if (this.searchQuery.length >= 2) {
      this.showResults = true;
    } else {
      this.showResults = false;
      this.searchResults = [];
    }
    this.searchSubject.next(this.searchQuery);
  }

  selectCity(city: CitySearchResult): void {
    this.searchQuery = `${city.name}, ${city.country}`;
    this.showResults = false;
    this.citySelected.emit(city.name);
  }

  useGeolocation(): void {
    this.weatherService.loadWeatherByGeolocation().catch(error => {
      console.error('Geolocation error:', error);
      // Auto-dismiss  errors after 3 seconds since they're not critical
      setTimeout(() => {
        this.weatherService.clearError();
      }, 3000);
    });
  }

  onBlur(): void {
    // Délai pour permettre le clic sur un résultat
    setTimeout(() => {
      this.showResults = false;
    }, 200);
  }

  onFocus(): void {
    if (this.searchResults.length > 0) {
      this.showResults = true;
    }
  }
}