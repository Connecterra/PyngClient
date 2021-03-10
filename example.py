from pyngclient import GenericPingClient

client = GenericPingClient()

result = client.send_ping("TestMonitor", "PT1H")
print(result)