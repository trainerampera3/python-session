import { useCallback } from "react";
import Table from "../component/table";
import useFetch from "../hooks/usefetch";
import { getCustomers } from "../api";

function Customers() {

    const fetchCustomers = useCallback(() => {
        return getCustomers();
    }, []);

    const { data, loading, error } = useFetch(fetchCustomers);

    if (loading) {
        return <h2>Loading customers...</h2>;
    }

    if (error) {
        return <h2>{error}</h2>;
    }

    return (
        <div className="dashboard">

            <div className="dashboard-header">
                <h1>Customers</h1>
                <p>Customer information</p>
            </div>

            <div className="card-grid">

                <div className="data-card">
                    <h2>Total Customers</h2>
                    <p>{data.length}</p>
                </div>

                <div className="data-card">
                    <h2>Active Customers</h2>
                    <p>
                        {data.filter(
                            (customer) => customer.status === "active"
                        ).length}
                    </p>
                </div>

            </div>

            <Table title="Customer Data" data={data} />

        </div>
    );
}

export default Customers;