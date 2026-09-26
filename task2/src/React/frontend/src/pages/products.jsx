import { useCallback } from "react";

import Table from "../component/table";
import useFetch from "../hooks/usefetch";
import { getProducts } from "../api";

function Products() {

    const fetchProducts = useCallback(() => {
        return getProducts();
    }, []);

    const { data, loading, error } = useFetch(fetchProducts);

    if (loading) {
        return <h2>Loading products...</h2>;
    }

    if (error) {
        return <h2>{error}</h2>;
    }

    return (
        <div className="dashboard">

            <div className="dashboard-header">
                <h1>Products</h1>
                <p>Product information</p>
            </div>

            <div className="card-grid">

                <div className="data-card">
                    <h2>Total Products</h2>
                    <p>{data.length}</p>
                </div>

            </div>

            <Table title="Product Data" data={data} />

        </div>
    );
}

export default Products;