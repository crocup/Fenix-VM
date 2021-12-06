from app.services.hostdiscovery import HostDiscovery


def test_del_misc_data():
    data = {
        "test": "test",
        "stats": "stats",
        "runtime": "runtime"
    }
    assert HostDiscovery(host="192.168.1.1", name="name", uuid="uuid",
                         db="db", table="table").del_misc_data(data=data) == {"test": "test"}


def test_del_misc_data_no_stats():
    data = {
        "test": "test",
        "runtime": "runtime"
    }
    assert HostDiscovery(host="192.168.1.1", name="name", uuid="uuid",
                         db="db", table="table").del_misc_data(data=data) == {"test": "test"}


def test_del_misc_data_no_stats_and_runtime():
    data = {
        "test": "test",
        "runtimes": "runtimes"
    }
    assert HostDiscovery(host="192.168.1.1", name="name", uuid="uuid",
                         db="db", table="table").del_misc_data(data=data) == {"test": "test", "runtimes": "runtimes"}


