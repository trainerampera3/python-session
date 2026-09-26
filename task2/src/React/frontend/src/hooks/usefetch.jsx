import { useEffect, useState } from "react";

function useFetch(fetchFunction) {

    const [data, setData] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    useEffect(() => {

        fetchFunction()
            .then((result) => {
                setData(result.data ?? result);
                setLoading(false);
            })
            .catch((error) => {
                setError(error.message);
                setLoading(false);
            });

    }, [fetchFunction]);

    return { data, loading, error };
}

export default useFetch;