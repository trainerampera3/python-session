function Table({ title, data }) {

    if (!Array.isArray(data) || data.length === 0) { 
        return (
            <div className="table-container">
                <h2>{title}</h2>
                <p>No data available</p>
            </div>
        );
    }

    const columns = Object.keys(data[0]);

    return (
        <div className="table-container">

            <div className="table-header">
                <div>
                    <h2>{title}</h2>
                    <p>{data.length} records</p>
                </div>
            </div>

            <div className="table-grid">

                <div className="table-row table-heading">
                    {columns.map((column) => (
                        <div className="table-cell" key={column}>
                            {column}
                        </div>
                    ))}
                </div>

                {data.map((row, index) => (
                    <div className="table-row" key={index}>

                        {columns.map((column) => (
                            <div className="table-cell" key={column}>
                                {typeof row[column] === "object"
                                    ? JSON.stringify(row[column])
                                    : row[column]}
                            </div>
                        ))}

                    </div>
                ))}

            </div>

        </div>
    );
}

export default Table;