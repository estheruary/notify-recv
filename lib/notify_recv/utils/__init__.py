import dbus
import json

# Because this is 99% of what you ever want to do with dbus.
def dbus_get_interface(bus, bus_name, object_path, interface):
    proxy = bus.get_object(bus_name, object_path)
    return dbus.Interface(proxy, dbus_interface=interface)
