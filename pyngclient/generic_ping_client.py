import os
from typing import Union
import requests
import json
import logging
from time import time
import isodate
import asyncio


class GenericPingClient:
    def __init__(
        self,
        username: str = None,
        password: str = None,
        token=None,
        odata_url: str = None,
        auth_url: str = None,
    ):

        self.odataUrl = odata_url if odata_url else os.environ.get("oDataUrl", None)
        self.authUrl = auth_url if auth_url else os.environ.get("authUrl", None)
        self.username = username if username else os.environ.get("authUsername", None)
        self.password = password if password else os.environ.get("authPassword", None)

        if self.username and self.password:
            self.authenticate()

        self.access_token = token
        self.headers = {"Authorization": f"Bearer {self.access_token}"}

    def authenticate(self) -> bool:
        auth = {
            "username": self.username,
            "password": self.password,
            "grant_type": "password",
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        r = requests.post(f"{self.authUrl}/token", data=auth, headers=headers)

        response_body = json.loads(r.text)

        self.expiration_epoch = int(time()) + parse_duration("PT24H")
        self.access_token = response_body.get("access_token")
        self.headers["Authorization"] = f"Bearer {self.access_token}"

        return True if self.access_token else False

    async def authenticate_async(self) -> bool:
        return self.authenticate()

    async def send_ping(
        self,
        name,
        ping_timeout: Union[int, str] = None,
        run_duration: int = None,
        override_timeout: bool = False,
    ) -> bool:
        monitor = self.__get_generic_ping_monitor(name)

        """ Ping the monitoring service. Create a new monitor if it does not exist yet. """

        ping_timeout_seconds = self.__parse_ping_timeout(ping_timeout)

        if int(time) > self.expiration_epoch:
            await self.authenticate_async()

        if not monitor:
            # Create a new monitor and get it returned.
            monitor = self.__create_ping_monitor(name, ping_timeout_seconds)

        monitor_id = monitor.get("MonitorID")
        patch_body = {
            "monitorName": monitor.get("monitorName"),
            "lastRunFinishEpoch": int(time()),
            "lastRunDuration": int(run_duration) if run_duration else 0,
        }

        if (
            override_timeout
            and ping_timeout != None
            and int(monitor.get("runFrequencySeconds")) != ping_timeout_seconds
        ):
            # Monitor should be updated to new ping timeout if our definition is not in line with the definition on the generic ping service.
            logging.info(
                f"Update {name} ping timeout interval to ({ping_timeout}) : { monitor.get('runFrequencySeconds') } => {ping_timeout_seconds}"
            )
            patch_body["runFrequencySeconds"] = ping_timeout_seconds

        r = requests.patch(
            f"{self.odataUrl}/GenericMonitorDefinitions({monitor_id})",
            json=patch_body,
            headers=self.headers,
        )

        logging.info(f"Sent ping for GenericPingMonitor '{name}'")
        return r.ok

    async def run_async(
        self,
        name: str,
        ping_interval: Union[str, int],
        ping_timeout: Union[str, int],
        override_timeout: bool = False,
    ):

        """ Run the ping client in an async application and send a ping every inverval """

        interval = parse_duration(ping_interval)
        ping_timeout = parse_duration(ping_timeout)
        start_time = int(time())

        if not interval:
            logging.error(f"Cannot run async with interval {interval}")

        while True:
            run_duration = int(time()) - start_time
            await self.send_ping(name, ping_timeout, run_duration, override_timeout=override_timeout)
            await asyncio.sleep(interval)

    def __get_generic_ping_monitor(self, name: str = None) -> dict:

        r = requests.get(f"{self.odataUrl}/GenericMonitorDefinitions", headers=self.headers)

        monitors_response = json.loads(r.text)
        monitors = monitors_response.get("value")

        monitor = [x for x in monitors if x.get("monitorName") == name]
        return monitor[0] if len(monitor) > 0 else None

    def __create_ping_monitor(self, name: str, ping_timeout_seconds: int = 3600) -> dict:

        logging.info(f"Creating a new monitor {name}")

        # Ping timeouts should not be shorter than 5 minutes
        ping_timeout_seconds = max(ping_timeout_seconds, 300)

        monitor_definition = {
            "monitorName": name,
            "runFrequencySeconds": ping_timeout_seconds,
            "alertEnabled": True,
            "slackUsers": None,
        }

        r = requests.post(
            f"{self.odataUrl}/GenericMonitorDefinitions",
            json=monitor_definition,
            headers=self.headers,
        )

        if not r.ok:
            logging.error(f"Could not create new monitor {monitor_definition.get('monitorName')}")

        response = r.json()
        return response


def parse_duration(interval: Union[str, int]) -> int:

    try:
        duration_seconds = int(interval)
    except ValueError:
        duration_seconds = isodate.parse_duration(interval).total_seconds()
    except Exception:
        return None
    return duration_seconds