import resource
import time

import click

from jping import ping_test


@click.command()
@click.option('--subnet-a', '-a', default='192.168.2')
@click.option('--subnet-b', '-b', default='192.168.3')
@click.option('--start', default=1)
@click.option('--end', default=255)
@click.option('--excluded-ips', '-e', default=[])
@click.option('--ping-count', '-c', default=2)
@click.option('--debug', '-d', default=False, is_flag=True, help='Turn on debug messages.')
def jping_command(subnet_a, subnet_b, start, end, excluded_ips, ping_count, debug):
    """JPING - ping test two subnets."""
    soft, hard = resource.getrlimit(resource.RLIMIT_NOFILE)
    max_workers = int(soft / 2 - 8)
    print("Max Workers = ", max_workers)
    start_time = time.time()
    unique_ips = ping_test(subnet_a, subnet_b, start, end, excluded_ips, ping_count, max_workers)
    print("\n".join(unique_ips))
    print("Number of unique ips: {}".format(len(unique_ips)))
    end_time = time.time()
    print("Time: {:10.2f} seconds.".format(end_time - start_time))


if __name__ == '__main__':
    jping_command()
