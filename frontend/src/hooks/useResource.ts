import { useCallback, useEffect, useState } from "react";
import { api, list } from "../api/client";

export function useResource<T>(path: string | null) {
  const [data, setData] = useState<T[]>([]);
  const [loading, setLoading] = useState(Boolean(path));
  const [error, setError] = useState("");

  const reload = useCallback(() => {
    if (!path) return;
    setLoading(true);
    api
      .get<{ results?: T[] } | T[]>(path)
      .then((payload) => setData(list<T>(payload)))
      .catch((err: Error) => setError(err.message))
      .finally(() => setLoading(false));
  }, [path]);

  useEffect(() => {
    reload();
  }, [reload]);

  return { data, loading, error, reload, setData };
}

export function useOne<T>(path: string | null) {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(Boolean(path));

  const reload = useCallback(() => {
    if (!path) return;
    setLoading(true);
    api
      .get<T>(path)
      .then(setData)
      .finally(() => setLoading(false));
  }, [path]);

  useEffect(() => {
    reload();
  }, [reload]);

  return { data, loading, reload };
}
