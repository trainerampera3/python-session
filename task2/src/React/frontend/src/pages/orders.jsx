import { useCallback } from "react";

import Table from "../component/table";
import useFetch from "../hooks/usefetch";
import { getOrders } from "../api";

function Orders() {

    const fetchOrders = useCallback(() => {
        return getOrders();
    }, []);

    const { data, loading, error } = useFetch(fetchOrders);

    if (loading) {
        return <h2>Loading orders...</h2>;
    }

    if (error) {
        return <h2>{error}</h2>;
    }

    return (
        <div className="dashboard">

            <div className="dashboard-header">
                <h1>Orders</h1>
                <p>Order information</p>
            </div>

            <div className="card-grid">

                <div className="data-card">
                    <h2>Total Orders</h2>
                    <p>{data.length}</p>
                </div>

            </div>

            <Table title="Order Data" data={data} />

        </div>
    );
}

export default Orders;