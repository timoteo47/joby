import concurrent.futures

from ping3 import ping

DEFAULT_PING_TIMEOUT = 1  # 1 second.


def ping_thread(ip: str, ping_count: int) -> (str, bool):
    """
    Ping device using ping3 module. Ping device ping_count times. Routine is run on its own thread.

    Args:
        ip (str): IP address to ping.
        ping_count (int): Number of times to ping IP address.

    Returns:
        ip (str): IP address that was pinged.
        return_code (bool): Return code from the ping command. True is success. False is failure.
    """
    pings = 0
    found = False
    try:
        while pings < ping_count and not found:
            pings += 1
            result = ping(ip, timeout=DEFAULT_PING_TIMEOUT)
            found = result is not None
    except OSError as err:
        if err.errno in [64, 65]:
            found = False
        else:
            raise
    return ip, found


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
    Ping device using ping3 module. Ping device ping_count times. Routine is run on its own thread.

    Args:
        subnet_a (str): First subnet to test.
        subnet_b (str): Second subnet to test.
        start_ip (int): 4th octet of starting IP address.
        end_ip (int): 4th octet of ending IP address.
        excluded_ips (list): List of 4th octets to be skipped.
        max_workers (int): Maximum of ping worker threads.

    Returns:
        unique_ips (list): List of IP address that are only pingable from one subnet.

    """
    # Validate inputs
    futures = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as pool:
        for i in range(start_ip, end_ip + 1):
            if i not in excluded_ips:
                future_a = pool.submit(
                    ping_thread, "{}.{}".format(subnet_a, i), ping_count
                )
                futures.append(future_a)
                future_b = pool.submit(
                    ping_thread, "{}.{}".format(subnet_b, i), ping_count
                )
                futures.append(future_b)

    results = {}
    for future in concurrent.futures.as_completed(futures):
        results[future.result()[0]] = future.result()[1]

    count = 0
    unique_ips = []
    up_ips = []
    for ip in sorted(results.keys(), key=lambda x: tuple(map(int, x.split(".")))):
        if results[ip]:
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
