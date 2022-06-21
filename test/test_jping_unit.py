import pytest

from src.jping_test import ping_subnets

SUBNET_A = "192.168.2"
SUBNET_B = "192.168.3"
START = 1
END = 254
PING_COUNT = 3
MAX_WORKERS = 96
EXCLUDED_IPS = []


def test_001_value_checking_start_ip_gt_254():
    with pytest.raises(ValueError, match="Starting IP address not in range 1 - 254."):
        start_ip = 300
        unique_ips = ping_subnets(
            SUBNET_A, SUBNET_B, start_ip, END, EXCLUDED_IPS, PING_COUNT, MAX_WORKERS
        )


def test_002_value_checking_start_ip_lt_1():
    with pytest.raises(ValueError, match="Starting IP address not in range 1 - 254."):
        start_ip = -9
        unique_ips = ping_subnets(
            SUBNET_A, SUBNET_B, start_ip, END, EXCLUDED_IPS, PING_COUNT, MAX_WORKERS
        )


def test_003_value_checking_end_ip_gt_254():
    with pytest.raises(ValueError, match="Ending IP address not in range 1 - 254."):
        end_ip = 300
        unique_ips = ping_subnets(
            SUBNET_A, SUBNET_B, START, end_ip, EXCLUDED_IPS, PING_COUNT, MAX_WORKERS
        )


def test_004_value_checking_end_ip_lt_1():
    with pytest.raises(ValueError, match="Ending IP address not in range 1 - 254."):
        end_ip = -10
        unique_ips = ping_subnets(
            SUBNET_A, SUBNET_B, START, end_ip, EXCLUDED_IPS, PING_COUNT, MAX_WORKERS
        )


def test_005_value_checking_start_lt_end_ip():
    with pytest.raises(
        ValueError, match="Starting IP address greater than ending IP address."
    ):
        start_ip = 20
        end_ip = 19
        unique_ips = ping_subnets(
            SUBNET_A, SUBNET_B, start_ip, end_ip, EXCLUDED_IPS, PING_COUNT, MAX_WORKERS
        )


def test_006_value_checking_subnet_a():
    with pytest.raises(ValueError):
        subnet_a = "192.168.1111"
        unique_ips = ping_subnets(
            subnet_a, SUBNET_B, START, END, EXCLUDED_IPS, PING_COUNT, MAX_WORKERS
        )


def test_007_value_checking_subnet_b():
    with pytest.raises(ValueError):
        subnet_b = "192.168.22222"
        unique_ips = ping_subnets(
            SUBNET_A, subnet_b, START, END, EXCLUDED_IPS, PING_COUNT, MAX_WORKERS
        )


def test_008_value_checking_max_workers():
    with pytest.raises(ValueError, match="Max Workers must be greater than 0."):
        max_workers = -1
        unique_ips = ping_subnets(
            SUBNET_A, SUBNET_B, START, END, EXCLUDED_IPS, PING_COUNT, max_workers
        )


def test_009_value_checking_ping_count():
    with pytest.raises(ValueError, match="Ping count must be greater than 0."):
        ping_count = -1
        unique_ips = ping_subnets(
            SUBNET_A, SUBNET_B, START, END, EXCLUDED_IPS, ping_count, MAX_WORKERS
        )


def test_010_value_checking_ping_count():
    with pytest.raises(
        ValueError,
        match="The 4th octet of excluded IP addresses must be in the range 1 - 254.",
    ):
        excluded_ips = [-1, 544]
        unique_ips = ping_subnets(
            SUBNET_A, SUBNET_B, START, END, excluded_ips, PING_COUNT, MAX_WORKERS
        )
