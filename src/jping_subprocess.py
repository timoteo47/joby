import concurrent.futures
import subprocess

import click

PING_COUNT = 2
MAX_WORKERS = 256
EXCLUDED_IPS = [56, 45, 23]
progress_bar = None


def update_progress_callback(future):
    """Return state of port.

    Args:
        port (int): Number of port. None returns status of all ports. Default = None - all ports.

    Returns:
        (str): State of port(s).

    Raises:
        RuntimeError: When it fails to get the status.
    """

    global progress_bar
    progress_bar.update(1)


def ping(ip: str, count: int) -> (str, int):
    """
    Create subprocess to ping one IP address. Uses the built-in ping command. The -o option is used to return once at
    least one valid response is received for the target IP address.

    Args:
        ip (str): IP address to ping.
        count (int): Number of times to ping IP address.

    Returns:
        ip (str): IP address that was pinged.
        returncode (int): Return code from the ping command. 0 is success. 2 is failure.
    """
    completed_process = subprocess.run(
        ["ping", "-c", "{}".format(count), "-q", "-o", ip], capture_output=True
    )
    return ip, completed_process.returncode


def ping_subnets(
        subnet_a: str,
        subnet_b: str,
        start_ip: int,
        end_ip: int,
        excluded_ips: list,
        ping_count: int,
        max_workers: int,
) -> list:
    """

    :param subnet_a:
    :param subnet_b:
    :param start_ip:
    :param end_ip:
    :param excluded_ips:
    :param ping_count:
    :param max_workers:
    :return:
    """
    # Validate inputs
    global progress_bar
    futures = []
    number_of_ips = (end_ip - start_ip + 1 - len(excluded_ips)) * 2
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as pool:
        with click.progressbar(length=number_of_ips, label="IPs pinged ...") as bar:
            progress_bar = bar
            for i in range(start_ip, end_ip + 1):
                if i not in excluded_ips:
                    future_a = pool.submit(
                        ping, "{}.{}".format(subnet_a, i), ping_count
                    )
                    future_a.add_done_callback(update_progress_callback)
                    futures.append(future_a)
                    future_b = pool.submit(
                        ping, "{}.{}".format(subnet_b, i), ping_count
                    )
                    future_b.add_done_callback(update_progress_callback)
                    futures.append(future_b)

    results = {}
    for future in concurrent.futures.as_completed(futures):
        results[future.result()[0]] = future.result()[1]

    count = 0
    unique_ips = []
    up_ips = []
    for ip in sorted(results.keys(), key=lambda x: tuple(map(int, x.split(".")))):
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
