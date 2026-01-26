import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { CurrentWeather } from '../../core/models/weather.model';
import { FavoritesUtil } from '../../shared/utils/favorites.util';

@Component({
  selector: 'app-current-weather',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './current-weather.component.html',
  styleUrls: ['./current-weather.component.css']
})
export class CurrentWeatherComponent {
  @Input() weather!: CurrentWeather;
  @Input() city!: string;
  @Input() country!: string;
  
  isFavorite = false;

  ngOnInit(): void {
    this.checkFavorite();
  }

  ngOnChanges(): void {
    this.checkFavorite();
  }

  checkFavorite(): void {
    if (this.city) {
      this.isFavorite = FavoritesUtil.isFavorite(this.city);
    }
  }

  toggleFavorite(): void {
    if (this.isFavorite) {
      FavoritesUtil.removeFavorite();
      this.isFavorite = false;
    } else {
      FavoritesUtil.saveFavorite(this.city, this.country);
      this.isFavorite = true;
    }
  }

  getWeatherIcon(icon: string): string {
    return `https://openweathermap.org/img/wn/${icon}@4x.png`;
  }

  getConditionTranslation(condition: string): string {
    const translations: { [key: string]: string } = {
      'Clear': 'Dégagé',
      'Clouds': 'Nuageux',
      'Rain': 'Pluie',
      'Drizzle': 'Bruine',
      'Thunderstorm': 'Orage',
      'Snow': 'Neige',
      'Mist': 'Brume',
      'Fog': 'Brouillard'
    };
    return translations[condition] || condition;
  }
}