import resource
import time

import click

from jping import ping_test


@click.command()
@click.option("--subnet-a", "-a", default="192.168.2", help="First subnet to test.")
@click.option("--subnet-b", "-b", default="192.168.3", help="Second subnet to test.")
@click.option("--start", default=1, help="Starting IP address in subnet.")
@click.option("--end", default=255, help="Ending IP address in subnet.")
@click.option(
    "--excluded-ips",
    "-e",
    default="",
    help='Quoted, comma seperated list of IP addresses to be excluded. Example: -e "56, 88, 99".',
)
@click.option(
    "--ping-count",
    "-c",
    default=2,
    help="Number of times to attempt pinging IP address.",
)
@click.option(
    "--debug", "-d", default=False, is_flag=True, help="Turn on debug messages."
)
def jping_command(subnet_a, subnet_b, start, end, excluded_ips, ping_count, debug):
    """JPING - ping test two subnets."""
    soft, hard = resource.getrlimit(resource.RLIMIT_NOFILE)
    max_workers = int(3 * soft / 8)
    print("Maximum number of ping processes = ", max_workers)
    start_time = time.time()
    excluded_ips_list = excluded_ips.replace(",", " ").split()
    print("Excluded IPs = {}".format(excluded_ips_list))
    number_of_ips = (end - start + 1 - len(excluded_ips_list)) * 2
    print("Pinging {} IP addresses ...".format(number_of_ips))
    unique_ips = ping_test(
        subnet_a, subnet_b, start, end, excluded_ips_list, ping_count, max_workers
    )
    print("\n".join(unique_ips))
    print("Number of unique IPs: {}".format(len(unique_ips)))
    end_time = time.time()
    print("Time: {:10.2f} seconds.".format(end_time - start_time))


if __name__ == "__main__":
    jping_command()
