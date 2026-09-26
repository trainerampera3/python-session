import { Link } from "react-router-dom";
import { useAppContext } from "../context/Appcontext";

function Card({ title, count, path }) {

    const { setSelectedTable } = useAppContext();

    const handleClick = () => {
        setSelectedTable(title);
    };

    return (
        <Link
            to={path}
            className="card-link"
            onClick={handleClick}
        >
            <div className="data-card">

                <h2>{title}</h2>

                <p>{count}</p>

                <span>View Data →</span>

            </div>
        </Link>
    );
}

export default Card;