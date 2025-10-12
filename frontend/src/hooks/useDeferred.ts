import 'client-only';
import { useMemo, useRef, useState } from 'react';

type Deferred<T> = {
  promise: Promise<T>;
  resolve: (value: T) => void;
  reject: (error: Error) => void;
};

export type DeferredResult<T> =
  | { state: 'resolved'; result: T }
  | { state: 'rejected'; error: Error }
  | {
      state: 'pending';
      promise: Promise<T>;
      resolve: (value: T) => void;
      reject: (error: Error) => void;
    };

const Empty = Symbol('empty');

export function useDeferred<T>(): DeferredResult<T> {
  const deferred = useRef<Deferred<T> | null>(null);
  const [result, setResult] = useState<T | Symbol>(Empty);
  const [error, setError] = useState<Error | Symbol>(Empty);

  if (!deferred.current) {
    let deferredValue: Deferred<T> = {
      promise: Promise.resolve('temp' as unknown as T),
      resolve: () => {},
      reject: () => {},
    };

    deferredValue.promise = new Promise<T>((resolve, reject) => {
      deferredValue.resolve = resolve;
      deferredValue.reject = reject;
    });

    deferred.current = deferredValue;
  }

  const resolvedState = useMemo(() => {
    if (result === Empty) {
      return null;
    }
    return { state: 'resolved' as const, result: result as T };
  }, [result]);

  const rejectedState = useMemo(() => {
    if (error === Empty) {
      return null;
    }
    return { state: 'rejected' as const, error: error as Error };
  }, [error]);

  const pendingState = useMemo(
    () => ({
      state: 'pending' as const,
      promise: deferred.current!.promise,
      resolve: (value: T) => {
        setResult(value);
        deferred.current!.resolve(value);
      },
      reject: (error: Error) => {
        setError(error);
        deferred.current!.reject(error);
      },
    }),
    [],
  );

  return resolvedState || rejectedState || pendingState;
}