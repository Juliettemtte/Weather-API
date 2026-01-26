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

  constructor(private weatherService: WeatherService) {
    // Debounce pour éviter trop de requêtes
    this.searchSubject.pipe(
      debounceTime(300),
      distinctUntilChanged(),
      switchMap(query => {
        if (query.length < 2) {
          this.searchResults = [];
          this.showResults = false;
          return [];
        }
        this.isSearching = true;
        return this.weatherService.searchCities(query);
      })
    ).subscribe({
      next: (response) => {
        this.searchResults = response.results || [];
        this.showResults = this.searchResults.length > 0;
        this.isSearching = false;
      },
      error: () => {
        this.isSearching = false;
        this.searchResults = [];
      }
    });
  }

  onSearchInput(): void {
    this.searchSubject.next(this.searchQuery);
  }

  selectCity(city: CitySearchResult): void {
    this.searchQuery = `${city.name}, ${city.country}`;
    this.showResults = false;
    this.citySelected.emit(city.name);
  }

  useGeolocation(): void {
    this.weatherService.loadWeatherByGeolocation().catch(error => {
      console.error('Erreur géolocalisation:', error);
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