import { useCallback } from "react";
import Table from "../component/table";
import useFetch from "../hooks/usefetch";
import { getStores } from "../api";

function Stores() {

    const fetchStores = useCallback(() => {
        return getStores();
    }, []);

    const { data, loading, error } = useFetch(fetchStores);

    if (loading) {
        return <h2>Loading stores...</h2>;
    }

    if (error) {
        return <h2>{error}</h2>;
    }

    return (
        <div className="dashboard">

            <div className="dashboard-header">
                <h1>Stores</h1>
                <p>Store information</p>
            </div>

            <div className="card-grid">

                <div className="data-card">
                    <h2>Total Stores</h2>
                    <p>{data.length}</p>
                </div>

            </div>

            <Table title="Store Data" data={data} />

        </div>
    );
}

export default Stores;