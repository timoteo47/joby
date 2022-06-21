import concurrent.futures
import subprocess
from ipaddress import ip_address
from typing import List

from ping3 import ping

DEFAULT_PING_TIMEOUT = 1  # 1 second.


def ping_subprocess(ip: str, count: int) -> (str, int):
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
    found = completed_process.returncode == 0
    return ip, found


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
    pings: int = 0
    found: bool = False
    # Need to catch OSErrors for host down and route not reachable errors that are not caught by the ping3 library.
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
        use_built_in: bool = True,
) -> List[str]:
    """
    Ping IP addresses using ping3 module. Ping device ping_count times. Routine is run on its own thread. The number of ping
    threads is limited by max_workers.

    Args:
        subnet_a (str): First subnet to test.
        subnet_b (str): Second subnet to test.
        start_ip (int): 4th octet of starting IP address.
        end_ip (int): 4th octet of ending IP address.
        excluded_ips (List[int]): List of 4th octets to be skipped.
        ping_count (int): Number of times to ping IP address.
        max_workers (int): Maximum of ping worker threads.
        use_built_in (bool): Call the built-in ping command using subprocess.

    Returns:
        unique_ips (List[str]): List of IP address that are only pingable on one subnet.

    """
    # Validate inputs
    if start_ip not in range(255):
        raise ValueError("Starting IP address not in range 1 - 254.")
    if end_ip not in range(255):
        raise ValueError("Ending IP address not in range 1 - 254.")
    if start_ip > end_ip:
        raise ValueError("Starting IP address greater than ending IP address.")
    # Validate IP subnets and starting/ending IP addresses.
    # ip_address will raise a ValueError if the IP address is invalid.
    ip_address("{}.{}".format(subnet_a, start_ip))
    ip_address("{}.{}".format(subnet_a, end_ip))
    ip_address("{}.{}".format(subnet_b, start_ip))
    ip_address("{}.{}".format(subnet_b, end_ip))
    if max_workers < 1:
        raise ValueError("Max Workers must be greater than 0.")
    if ping_count < 1:
        raise ValueError("Ping count must be greater than 0.")
    for excluded_ip in excluded_ips:
        if excluded_ip not in range(255):
            raise ValueError(
                "The 4th octet of excluded IP addresses must be in the range 1 - 254."
            )

    futures = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as pool:
        for i in range(start_ip, end_ip + 1):
            if i not in excluded_ips:
                if not use_built_in:
                    # Use the ping3 module to send pings because it is faster.
                    future_a = pool.submit(
                        ping_thread, "{}.{}".format(subnet_a, i), ping_count
                    )
                    future_b = pool.submit(
                        ping_thread, "{}.{}".format(subnet_b, i), ping_count
                    )
                else:
                    # Use the built-in ping command by call it with subprocess because it is more reliable.
                    future_a = pool.submit(
                        ping_subprocess, "{}.{}".format(subnet_a, i), ping_count
                    )
                    future_b = pool.submit(
                        ping_subprocess, "{}.{}".format(subnet_b, i), ping_count
                    )
                futures.append(future_a)
                futures.append(future_b)

    # Capture the results of the ping threads in a dictionary with IP addresses as keys.
    results = {}
    for future in concurrent.futures.as_completed(futures):
        results[future.result()[0]] = future.result()[1]

    count = 0
    unique_ips: List[str] = []
    up_ips = []
    # Sort the pingable IP addresses and append them to the up_ips list.
    for ip in sorted(results.keys(), key=lambda x: tuple(map(int, x.split(".")))):
        if results[ip]:
            count += 1
            up_ips.append(ip)

    # Check to see if the IP address with the same 4th octet is pingable on both subnets.
    # If not, the add the IP address to the list of unique_ips.
    for i in range(start_ip, end_ip + 1):
        if i not in excluded_ips:
            ip_a = "{}.{}".format(subnet_a, i)
            ip_b = "{}.{}".format(subnet_b, i)
            if ip_a in up_ips and ip_b not in up_ips:
                unique_ips.append(ip_a)
            elif ip_a not in up_ips and ip_b in up_ips:
                unique_ips.append(ip_b)

    # Return the IP addresses that are only pingable on one subnet.
    return unique_ips
