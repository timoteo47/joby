import resource
import time

import click

from jping_test import ping_subnets


@click.command()
@click.option(
    "--subnet-a",
    "-a",
    default="192.168.2",
    help="First subnet to test. (default: 192.168.2)",
)
@click.option(
    "--subnet-b",
    "-b",
    default="192.168.3",
    help="Second subnet to test. (default: 192.168.3)",
)
@click.option("--start", default=1, help="Starting IP address in subnet. (default: 1)")
@click.option("--end", default=254, help="Ending IP address in subnet. (default: 254")
@click.option(
    "--excluded-ips",
    "-e",
    default="",
    help='Quoted, comma seperated list of IP addresses to be excluded. Example: -e "56, 88, 99".',
)
@click.option(
    "--ping-count",
    "-c",
    default=5,
    help="Number of times to attempt pinging IP address. (default: 5)",
)
@click.option(
    "--quiet", "-q", default=False, is_flag=True, help="Turn off debug messages."
)
@click.option(
    "--ping3", "-p", default=False, is_flag=True, help="Use ping3 module (faster)."
)
def jping_command(
        subnet_a, subnet_b, start, end, excluded_ips, ping_count, quiet, ping3
):
    """jping - ping test two subnets."""
    # The maximum number of ping threads is based on the maximum number user processes.
    soft, hard = resource.getrlimit(resource.RLIMIT_NPROC)
    max_workers = int(3 * soft / 8)
    start_time = time.time()
    excluded_ips_list = excluded_ips.replace(",", " ").split()
    number_of_ips = (end - start + 1 - len(excluded_ips_list)) * 2
    if not quiet:
        print("Pinging {} IP addresses.".format(number_of_ips))
        print("Excluded IPs = {}".format(excluded_ips_list))
        print("Maximum number of ping threads = ", max_workers)
    unique_ips = ping_subnets(
        subnet_a,
        subnet_b,
        start,
        end,
        excluded_ips_list,
        ping_count,
        max_workers,
        use_built_in=not ping3,
    )
    end_time = time.time()
    if not quiet:
        print("IP addresses pingable on only one subnet:")
    print("\n".join(unique_ips))
    if not quiet:
        print("Number of unique IPs: {}".format(len(unique_ips)))
        print("Time: {:10.2f} seconds.".format(end_time - start_time))


if __name__ == "__main__":
    jping_command()
