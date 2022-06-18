import concurrent.futures
import subprocess

PING_COUNT = 2
MAX_WORKERS = 256
EXCLUDED_IPS = [56, 45, 23]


def ping(ip, count):
    completed_process = subprocess.run(["ping", "-c", "{}".format(count), "-q", "-o", ip], capture_output=True)
    return ip, completed_process.returncode


def ping_test(subnet_a, subnet_b, start_ip, end_ip, excluded_ips, ping_count, max_workers):
    futures = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as pool:
        for i in range(start_ip, end_ip + 1):
            if i not in excluded_ips:
                futures.append(pool.submit(ping, "{}.{}".format(subnet_a, i), ping_count))
                futures.append(pool.submit(ping, "{}.{}".format(subnet_b, i), ping_count))

    results = {}
    for future in concurrent.futures.as_completed(futures):
        results[future.result()[0]] = future.result()[1]

    # for ip in sorted(results.keys(), key=lambda x: tuple(map(int, x.split('.')))):
    #     print(ip, results[ip])

    # print("IP addresses on the network: ")
    count = 0
    unique_ips = []
    up_ips = []
    for ip in sorted(results.keys(), key=lambda x: tuple(map(int, x.split('.')))):
        if results[ip] == 0:
            count += 1
            up_ips.append(ip)
    for i in range(start_ip, end_ip + 1):
        if i not in excluded_ips:
            ip_a = "{}.{}".format(subnet_a, i)
            ip_b = "{}.{}".format(subnet_b, i)
            if ip_a in up_ips and ip_b not in up_ips:
                unique_ips.append(ip_a)
            elif ip_a not in up_ips and ip_b in up_ips:
                unique_ips.append(ip_b)
    # print("{} IP address up on the network.".format(count))
    return unique_ips

# start_time = time.time()
# unique_ips = ping_test("192.168.2", "192.168.3", 1, 255, EXCLUDED_IPS)
# print("Number of unique ips: {}".format(len(unique_ips)))
# print("\n".join(unique_ips))
# print("Number of unique ips: {}".format(len(unique_ips)))
# end_time = time.time()
# print("Time: {:10.2f}".format(end_time - start_time))
