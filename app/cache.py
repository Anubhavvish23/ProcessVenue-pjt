import json
import redis.asyncio as aioredis
from redis.exceptions import ConnectionError, RedisError

# Redis connection with error handling
try:
    r = aioredis.Redis(host="localhost", port=6379, decode_responses=True)
    print("✅ Redis connection established")
except Exception as e:
    print(f"⚠️ Redis connection failed: {e}")
    r = None

async def get_cache(key):
    """Get data from Redis cache with error handling"""
    if r is None:
        print("⚠️ Redis not available, skipping cache")
        return None
    
    try:
        data = await r.get(key)
        if data:
            return json.loads(data)
        return None
    except (ConnectionError, RedisError) as e:
        print(f"⚠️ Redis error in get_cache: {e}")
        return None
    except Exception as e:
        print(f"⚠️ Unexpected error in get_cache: {e}")
        return None

async def set_cache(key, value, ex=60):
    """Set data in Redis cache with error handling"""
    if r is None:
        print("⚠️ Redis not available, skipping cache")
        return
    
    try:
        await r.set(key, json.dumps(value), ex=ex)
        print(f"✅ Cached data for key: {key}")
    except (ConnectionError, RedisError) as e:
        print(f"⚠️ Redis error in set_cache: {e}")
    except Exception as e:
        print(f"⚠️ Unexpected error in set_cache: {e}")

async def test_redis_connection():
    """Test Redis connection"""
    if r is None:
        return False
    
    try:
        await r.ping()
        print("✅ Redis connection test successful")
        return True
    except Exception as e:
        print(f"❌ Redis connection test failed: {e}")
        return False
