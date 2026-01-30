import { FavoriteCity } from '../../core/models/weather.model';

const STORAGE_KEY = 'weather_favorite_city';

export class FavoritesUtil {
  /**
   * Save favorite city
   */
  static saveFavorite(city: string, country: string): void {
    const favorite: FavoriteCity = {
      name: city,
      country: country,
      savedAt: new Date().toISOString()
    };
    localStorage.setItem(STORAGE_KEY, JSON.stringify(favorite));
  }

  /**
   * Get favorite city
   */
  static getFavorite(): FavoriteCity | null {
    const stored = localStorage.getItem(STORAGE_KEY);
    if (!stored) return null;
    
    try {
      return JSON.parse(stored) as FavoriteCity;
    } catch {
      return null;
    }
  }

  /**
   * Remove favorite city
   */
  static removeFavorite(): void {
    localStorage.removeItem(STORAGE_KEY);
  }

  /**
   * Check if city is favorite
   */
  static isFavorite(city: string): boolean {
    const favorite = this.getFavorite();
    return favorite?.name.toLowerCase() === city.toLowerCase();
  }
}