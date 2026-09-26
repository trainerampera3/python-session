const API_URL = "http://127.0.0.1:8000";

export async function getCustomers() {
    const response = await fetch(`${API_URL}/customers`);

    if (!response.ok) {
        throw new Error("Failed to fetch customers");
    }

    return response.json();
}

export async function getOrders() {
    const response = await fetch(`${API_URL}/orders`);

    if (!response.ok) {
        throw new Error("Failed to fetch orders");
    }

    return response.json();
}

export async function getProducts() {
    const response = await fetch(`${API_URL}/products`);

    if (!response.ok) {
        throw new Error("Failed to fetch products");
    }

    return response.json();
}

export async function getStores() {
    const response = await fetch(`${API_URL}/stores/stores`);

    if (!response.ok) {
        throw new Error("Failed to fetch stores");
    }

    return response.json();
}