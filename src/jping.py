import concurrent.futures
import subprocess

import click

PING_COUNT = 2
MAX_WORKERS = 256
EXCLUDED_IPS = [56, 45, 23]
progress_bar = None


# number_of_ips = 0

def update_progress_callback(future):
    global progress_bar
    progress_bar.update(1)


def ping(ip, count):
    completed_process = subprocess.run(["ping", "-c", "{}".format(count), "-q", "-o", ip], capture_output=True)
    return ip, completed_process.returncode


def ping_test(subnet_a, subnet_b, start_ip, end_ip, excluded_ips, ping_count, max_workers):
    global progress_bar
    futures = []
    number_of_ips = (end_ip - start_ip + 1 - len(excluded_ips)) * 2
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as pool:
        with click.progressbar(length=number_of_ips,
                               label='IPs pinged ...') as bar:
            progress_bar = bar
            for i in range(start_ip, end_ip + 1):
                if i not in excluded_ips:
                    future_a = pool.submit(ping, "{}.{}".format(subnet_a, i), ping_count)
                    future_a.add_done_callback(update_progress_callback)
                    futures.append(future_a)
                    future_b = pool.submit(ping, "{}.{}".format(subnet_b, i), ping_count)
                    future_b.add_done_callback(update_progress_callback)
                    futures.append(future_b)

    results = {}
    for future in concurrent.futures.as_completed(futures):
        results[future.result()[0]] = future.result()[1]

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
    print("{} IP address up on the network.".format(count))
    return unique_ips
