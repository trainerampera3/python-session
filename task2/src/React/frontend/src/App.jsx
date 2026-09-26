import { Routes, Route } from "react-router-dom";

import Dashboard from "./pages/dashboard";
import Customers from "./pages/customers";
import Orders from "./pages/orders";
import Products from "./pages/products";
import Stores from "./pages/stores";

function App() {
    return (
        <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/customers" element={<Customers />} />
            <Route path="/orders" element={<Orders />} />
            <Route path="/products" element={<Products />} />
            <Route path="/stores" element={<Stores />} />
        </Routes>
    );
}

export default App;