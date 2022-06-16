import concurrent.futures
import ipaddress

import time
import subprocess


def pingf(ip):
    # print("In pingf -- pinging: {}".format(ip))
    completed_process = subprocess.run(["ping", "-c", "3", "-q", "-o", ip], capture_output=True)
    return ip, completed_process.returncode


def main():
    futures = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=1024) as pool:
        for i in range(1, 255):
            futures.append(pool.submit(pingf, "172.168.2.{}".format(i)))
            futures.append(pool.submit(pingf, "172.168.3.{}".format(i)))
            futures.append(pool.submit(pingf, "172.168.4.{}".format(i)))
            futures.append(pool.submit(pingf, "172.168.5.{}".format(i)))

    results = {}
    for future in concurrent.futures.as_completed(futures):
        results[future.result()[0]] = future.result()[1]

    # for ip in sorted(results.keys(), key=lambda x: tuple(map(int, x.split('.')))):
    #     print(ip, results[ip])

    print("IP addresses on the network: ")
    count = 0
    for ip in sorted(results.keys(), key=lambda x: tuple(map(int, x.split('.')))):
        if results[ip] == 0:
            count += 1
            # print(ip, results[ip])
    print("{} IP address up on the network.".format(count))


start_time = time.time()
main()
end_time = time.time()
print("Time: {:10.2f}".format(end_time - start_time))
