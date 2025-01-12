import redis

def fetch_redis_data(redis_host, redis_port, index_prefix):
    try:
        # Connect to Redis
        client = redis.StrictRedis(host=redis_host, port=redis_port, decode_responses=True)
        
        # Check if the connection is successful
        if not client.ping():
            print("Unable to connect to Redis server.")
            return None
        
        # Fetch all keys with the given prefix
        keys = client.keys(f"{index_prefix}*")
        
        # Fetch data for each key
        data = {}
        for key in keys:
            data[key] = client.get(key)
        
        return data

    except redis.ConnectionError as e:
        print(f"Connection error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Configuration
redis_host = "localhost"  # Replace with your Redis host
redis_port = 6379         # Replace with your Redis port
index_prefix = "your_prefix"  # Replace with your index prefix

# Fetch and display data
if __name__ == "__main__":
    redis_data = fetch_redis_data(redis_host, redis_port, index_prefix)
    if redis_data:
        for key, value in redis_data.items():
            print(f"{key}: {value}")
