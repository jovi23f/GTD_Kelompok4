import csv
from locust import HttpUser, task, between, events, LoadTestShape
from statistics import mean
import time

# Base host (change if necessary)
BASE_HOST = "http://127.0.0.1:8000"

# List of endpoints to rotate during the test
ENDPOINTS = [
    #"/events?page=1&limit=15&iyear=2005&region_name=South%20Asia&sortby=iday&order=asc",
    #"/groups?page=1&limit=15&sortby=gname&order=asc",
    #"/weapons?page=1&limit=5&sortby=type&order=desc",
    #"/targets?page=1&limit=15&sortby=targtype1_txt&order=asc",
    #"/regions?page=1&limit=55&sortby=region&order=asc",
    # "/countries?page=1&limit=15&sortby=country&order=asc",
    "/attacks?page=1&limit=15&sortby=attacktype&order=asc"
]

# Load phases
STAGES = [
    {"name": "Light", "duration": 240, "users": 100, "spawn_rate": 100},
    {"name": "Medium", "duration": 240, "users": 300, "spawn_rate": 300},
    {"name": "Heavy", "duration": 240, "users": 500, "spawn_rate": 500}
]

# Global variables to collect metrics
metrics = {
    "response_times": [],
    "throughput": [],
    "error_rate": []
}

# Global state to manage endpoint and stage rotation
current_endpoint_index = 0
current_stage_index = 0
test_started = False

# Event listener to collect metrics on each request
@events.request.add_listener
def on_request(request_type, name, response_time, response_length, response, context, exception, start_time, url, **kwargs):
    if response:
        metrics["response_times"].append(response_time)
        metrics["throughput"].append(response_length)
        if response.status_code >= 400:
            metrics["error_rate"].append(1)
        else:
            metrics["error_rate"].append(0)
    else:
        metrics["error_rate"].append(1)

class LoadTestUser(HttpUser):
    wait_time = between(1, 3)
    host = BASE_HOST

    @task
    def test_endpoint(self):
        global current_endpoint_index
        if current_endpoint_index < len(ENDPOINTS):
            endpoint = ENDPOINTS[current_endpoint_index]
            self.client.get(endpoint)

# Custom load shape to handle multiple scenarios and rotate endpoints
class StepLoadShape(LoadTestShape):
    def tick(self):
        global current_endpoint_index, current_stage_index, test_started

        # If we finished all endpoints, stop the test
        if current_endpoint_index >= len(ENDPOINTS):
            return None
        
        # Get the current stage
        stage = STAGES[current_stage_index]
        
        # Start the stage only once
        if not test_started:
            print(f"\nStarting {stage['name']} Load Test for {ENDPOINTS[current_endpoint_index]}")
            test_started = True
            metrics["response_times"].clear()
            metrics["throughput"].clear()
            metrics["error_rate"].clear()
            self.start_time = time.time()

        # Check if the stage duration is complete
        if time.time() - self.start_time >= stage["duration"]:
            # Save the results to CSV
            save_results(stage["name"])

            # Move to the next stage
            current_stage_index += 1
            test_started = False

            # If all stages are done, reset for the next endpoint
            if current_stage_index >= len(STAGES):
                current_stage_index = 0
                current_endpoint_index += 1

            # If still within range, prepare for the next stage
            if current_endpoint_index < len(ENDPOINTS):
                print(f"\nCompleted all stages for {ENDPOINTS[current_endpoint_index - 1]}.\n")
        
        return (stage["users"], stage["spawn_rate"])

# Function to save the metrics
def save_results(stage_name):
    if metrics["response_times"]:
        average_response_time = mean(metrics["response_times"])
        latency_p95 = sorted(metrics["response_times"])[int(len(metrics["response_times"]) * 0.95)]
        latency_p99 = sorted(metrics["response_times"])[int(len(metrics["response_times"]) * 0.99)]
    else:
        average_response_time = latency_p95 = latency_p99 = 0

    rps = len(metrics["response_times"]) / STAGES[current_stage_index]["duration"]
    error_rate = sum(metrics["error_rate"]) / len(metrics["error_rate"]) if metrics["error_rate"] else 0
    throughput = mean(metrics["throughput"]) if metrics["throughput"] else 0

    # Append results to CSV (not overwrite)
    with open("loadtest_endpoint7_results.csv", "a", newline="") as csvfile:
        fieldnames = ["endpoint", "stage", "average_response_time", "latency_p95", "latency_p99", "rps", "error_rate", "throughput"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # If the file is new, write the header
        if csvfile.tell() == 0:
            writer.writeheader()
        
        writer.writerow({
            "endpoint": ENDPOINTS[current_endpoint_index],
            "stage": stage_name,
            "average_response_time": average_response_time,
            "latency_p95": latency_p95,
            "latency_p99": latency_p99,
            "rps": rps,
            "error_rate": error_rate,
            "throughput": throughput
        })

    print(f"Results saved for {ENDPOINTS[current_endpoint_index]} - {stage_name}")
