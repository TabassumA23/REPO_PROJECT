// User Interface (RestaurantSiteUser)
export interface User {
    id: number;
    username: string;
    first_name: string;
    last_name: string;
    email: string;
    date_of_birth: string; // YYYY-MM-DD format
    password?: string; // Optional for security reasons
    fav_cuisines: Cuisine[];
    dietary_restrictions: DietaryRestriction[];
    saved_restaurants: Restaurant[];
    disliked_restaurants: Restaurant[];
}

// Cuisine Interface
export interface Cuisine {
    id: number;
    name: string;
}

// Dietary Restriction Interface
export interface DietaryRestriction {
    id: number;
    name: string;
}

// Restaurant Interface
export interface Restaurant {
    id: number;
    name: string;
    address: string;
    cuisine: Cuisine;
    dietary_options: DietaryRestriction[];
    price_range: "$" | "$$" | "$$$"; // Enum-like structure for price
    opening_hours: Record<string, string>; // Example: { "Monday": "9AM-10PM" }
    website?: string;
    contact_number?: string;
}

// Review Interface
export interface Review {
    id: number;
    user: User;
    restaurant: Restaurant;
    rating: 1 | 2 | 3 | 4 | 5; // Ensures valid ratings
    comment?: string;
    created_at: string; // ISO date format
}

// Reservation Interface
export interface Reservation {
    id: number;
    user: User;
    restaurant: Restaurant;
    reservation_time: string; // ISO date format (e.g., "2024-02-19T19:30:00Z")
    number_of_people: number;
    status: "Pending" | "Confirmed" | "Cancelled";
}

// Wishlist Interface
export interface Wishlist {
    id: number;
    user: User;
    name: string;
    restaurants: Restaurant[];
}

// Recommendation Interface
export interface Recommendation {
    id: number;
    user: User;
    restaurant: Restaurant;
    reason: string; // "Based on your preferences", "Highly rated near you"
}
