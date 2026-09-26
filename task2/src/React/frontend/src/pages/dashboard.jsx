import Card from "../component/cards";
import "../component/table.css";

function Dashboard() {
    return (
        <div className="dashboard">

            <div className="dashboard-header">
                <h1>Data Dashboard</h1>
                <p>Select a table to view its data</p>
            </div>

            <div className="card-grid">

                <Card
                    title="Customers"
                    count="Customers"
                    path="/customers"
                />

                <Card
                    title="Orders"
                    count="Orders"
                    path="/orders"
                />

                <Card
                    title="Products"
                    count="Products"
                    path="/products"
                />

                <Card
                    title="Stores"
                    count="Stores"
                    path="/stores"
                />

            </div>

        </div>
    );
}

export default Dashboard;