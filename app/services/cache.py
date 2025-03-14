import json
from functools import wraps
from aiocache import Cache
from fastapi import HTTPException

def cache_response(ttl: int = 300, namespace: str = "main"):
    """
    Caching decorator for FastAPI endpoints.

    ttl: Time to live for the cache in seconds.
    namespace: Namespace for cache keys in Redis.
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            user_id = kwargs.get('user_data')
            cache_key = f"{namespace}:user:{user_id}"

            # cache = Cache.MEMORY(endpoint="localhost", port=6379, namespace=namespace)
            cache = Cache.MEMORY(namespace=namespace)

            # Try to retrieve data from cache
            cached_value = await cache.get(cache_key)
            if cached_value:
                return json.loads(cached_value)  # Return cached data

            # Call the actual function if cache is not hit
            response = await func(*args, **kwargs)

            try:
                await cache.set(cache_key, json.dumps(response), ttl=ttl)
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Error caching data: {e}")

            return response
        return wrapper
    return decorator
