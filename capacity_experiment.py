# Experiment 3: KV-cache memory and serving capacity

# Model configuration from bench/model_spec.md
layers = 28
kv_heads = 8
head_dim = 128
bytes_per_element = 2       # FP16
max_model_len = 4096

gpu_memory_gb = 24
gpu_utilization = 0.92
runtime_overhead_gb = 1.6

# KV cache stores both K and V
bytes_per_token = (
    2 * layers * kv_heads * head_dim * bytes_per_element
)

# Convert bytes to GB
kb_per_token = bytes_per_token / 1024
gb_per_token = bytes_per_token / (1024 ** 3)

# Maximum memory available for KV cache
kv_memory_gb = (
    gpu_memory_gb * gpu_utilization
    - runtime_overhead_gb
)

# Memory used by one request at maximum length
memory_per_request_gb = gb_per_token * max_model_len

# Approximate maximum concurrent requests
max_requests = int(kv_memory_gb / memory_per_request_gb)

print("KV-cache capacity analysis")
print("-" * 40)

print(f"KV-cache bytes/token: {bytes_per_token}")
print(f"KV-cache KB/token: {kb_per_token:.2f}")
print(f"KV-cache GB/token: {gb_per_token:.8f}")

print(f"Available KV memory: {kv_memory_gb:.2f} GB")
print(f"Memory per request: {memory_per_request_gb:.3f} GB")
print(f"Max concurrent requests: {max_requests}")