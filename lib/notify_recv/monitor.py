from gi.repository import GLib
import dbus
from dbus.mainloop.glib import DBusGMainLoop

from notify_recv.utils import dbus_get_interface
from notify_recv.notification import Notification

class NotifyMonitor(object):
    NOTIFY_DBUS_NAME = "org.freedesktop.Notifications"
    NOTIFY_DBUS_CORE_OBJECT = "/org/freedesktop/Notifications"
    NOTIFY_DBUS_CORE_INTERFACE = "org.freedesktop.Notifications"

    DBUS_NAME = "org.freedesktop.DBus"
    DBUS_CORE_OBJECT = "/org/freedesktop/DBus"
    DBUS_MONITOR_INTERFACE = "org.freedesktop.DBus.Monitoring"
    DBUS_NAMEOWNER_INTERFACE = 'org.freedesktop.DBus.NameOwnerChanged'

    def __init__(self, formatter):
        GLib.threads_init()
        DBusGMainLoop(set_as_default=True)

        self._bus = dbus.SessionBus()
        self._formatter = formatter

        # We have to do this little dance of monitoring the application that
        # owns this name because message filtering appears to be broken and you
        # can't actually use the destination= filter.
        self._update_notifications_owner()

        self._bus.add_message_filter(self._get_message_handle())

        iface = dbus_get_interface(
                self._bus,
                self.DBUS_NAME,
                self.DBUS_CORE_OBJECT,
                self.DBUS_MONITOR_INTERFACE)
        iface.BecomeMonitor([
            f"type='method_call',interface='{self.NOTIFY_DBUS_CORE_INTERFACE}',member='Notify'",
            f"type='signal',interface='{self.DBUS_NAMEOWNER_INTERFACE}',member='NameOwnerChanged'"
        ], 0)

    # This method exists for no other reason than to have the callback close over self.
    def _get_message_handle(self):
        def h(bus, message):
            destination = message.get_destination()

            # We have to filter the destination ourselves because the match rule
            # doesn't work in all versions.
            if message.is_method_call(self.NOTIFY_DBUS_CORE_INTERFACE, 'Notify') and \
               self._notifications_owner == destination:
                self._formatter.send(Notification.frommessage(message))

            if message.is_method_call(self.DBUS_NAMEOWNER_INTERFACE, 'NameOwnerChanged'):
                # TODO: We could do better and check if the name that changed
                # was the one we care about but w/e.
                self._update_notifications_owner()

        return h

    def _update_notifications_owner(self):
        self._notifications_owner = self._bus.activate_name_owner(self.NOTIFY_DBUS_NAME)

    def start(self):
        self._mainloop = GLib.MainLoop()

        if not self._mainloop:
            return

        self._mainloop.run()
