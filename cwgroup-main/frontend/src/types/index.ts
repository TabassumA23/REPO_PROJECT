// User Interface (RestaurantSiteUser)
export interface User {
    id: number;
    username: string;
    first_name: string;
    last_name: string;
    email: string;
    date_of_birth: string; 
    password?: string; 
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
    price_range: "$" | "$$" | "$$$"; 
    opening_hours: Record<string, string>;
    website?: string;
    contact_number?: string;
}

// Review Interface
export interface Review {
    id: number;
    user: User;
    restaurant: Restaurant;
    rating: 1 | 2 | 3 | 4 | 5; 
    comment?: string;
    created_at: string; 
}

// Reservation Interface
export interface Reservation {
    id: number;
    user: User;
    restaurant: Restaurant;
    reservation_time: string; 
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
    reason: string;
}
