from src.jping_test import ping_subnets

PING_COUNT = 10


def test_101_excluded_ips():
    excluded_ips = [56, 57, 58]
    subnet_a = "192.168.2"
    subnet_b = "192.168.3"
    start = 1
    end = 254
    ping_count = PING_COUNT
    max_workers = 96
    unique_ips_01 = ping_subnets(
        subnet_a, subnet_b, start, end, excluded_ips, ping_count, max_workers
    )
    assert len(unique_ips_01) == 127


def test_102_all_ips():
    excluded_ips = []
    subnet_a = "192.168.2"
    subnet_b = "192.168.3"
    start = 1
    end = 254
    ping_count = PING_COUNT
    max_workers = 96
    unique_ips_02 = ping_subnets(
        subnet_a, subnet_b, start, end, excluded_ips, ping_count, max_workers
    )
    assert len(unique_ips_02) == 127


def test_103_0_unique_ips():
    excluded_ips = []
    subnet_a = "192.168.2"
    subnet_b = "192.168.3"
    start = 1
    end = 10
    ping_count = 2
    max_workers = 96
    unique_ips_03 = ping_subnets(
        subnet_a, subnet_b, start, end, excluded_ips, ping_count, max_workers
    )
    assert len(unique_ips_03) == 0


def test_104_8_unique_ips():
    excluded_ips = [128]
    subnet_a = "192.168.2"
    subnet_b = "192.168.3"
    start = 120
    end = 136
    ping_count = 2
    max_workers = 96
    unique_ips_04 = ping_subnets(
        subnet_a, subnet_b, start, end, excluded_ips, ping_count, max_workers
    )

    a = set(unique_ips_04)
    b = {
        "192.168.2.129",
        "192.168.2.130",
        "192.168.2.131",
        "192.168.2.132",
        "192.168.2.133",
        "192.168.2.134",
        "192.168.2.135",
        "192.168.2.136",
    }
    assert a == b
