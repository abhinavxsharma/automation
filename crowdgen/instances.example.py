"""Example configuration of CrowdGen Maven worker instances."""

from crowdgen_automation.instances import InstanceConfig

INSTANCES: list[InstanceConfig] = [
    InstanceConfig(
        email="your_email@example.com",
        password="your_password",
        task_url="https://dq0uw9vf3nt8l.cloudfront.net",
        headless=False,
        max_tasks=250,
        auto_submit=True,
        aht_min_wait_sec=30,
        target_remaining_sec=130,
    ),
]
