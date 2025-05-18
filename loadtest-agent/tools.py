import subprocess
import os
import pandas as pd

def run_jmeter(jmx_file="test.jmx", jtl_file="results.jtl"):
    print(f"Running JMeter test: {jmx_file}")
    cmd = ["jmeter", "-n", "-t", jmx_file, "-l", jtl_file]
    subprocess.run(cmd)
    return jtl_file

def analyze_results(jtl_file="results.jtl"):
    df = pd.read_csv(jtl_file)
    avg_time = df['elapsed'].mean()
    error_rate = df[df['responseCode'] != '200'].shape[0] / df.shape[0]
    throughput = df.shape[0] / ((df['timeStamp'].max() - df['timeStamp'].min()) / 1000)

    print(f"Average response time: {avg_time:.2f} ms")
    print(f"Error rate: {error_rate * 100:.2f}%")
    print(f"Throughput: {throughput:.2f} req/sec")

    return {
        "avg_response_time": avg_time,
        "error_rate": error_rate,
        "throughput": throughput
    }