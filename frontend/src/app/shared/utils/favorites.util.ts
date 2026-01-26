import { FavoriteCity } from '../../core/models/weather.model';

const STORAGE_KEY = 'weather_favorite_city';

export class FavoritesUtil {
  /**
   * Sauvegarde la ville favorite
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
   * Récupère la ville favorite
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
   * Supprime la ville favorite
   */
  static removeFavorite(): void {
    localStorage.removeItem(STORAGE_KEY);
  }

  /**
   * Vérifie si une ville est favorite
   */
  static isFavorite(city: string): boolean {
    const favorite = this.getFavorite();
    return favorite?.name.toLowerCase() === city.toLowerCase();
  }
}