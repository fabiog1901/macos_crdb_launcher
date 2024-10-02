from configparser import ConfigParser
import rumps
import shlex
import subprocess
import webbrowser


class App:
    def __init__(self):
        # 🟢 🔴

        # rumps app
        self.app = rumps.App(
            "macos_crdb_launcher", icon="cockroachdb_logo.png", quit_button=None
        )

        self.config = ConfigParser()
        self.read_config()
        self.pid = ""

        # set Timer callback at 5s
        # the timer checks that CRDB is still alive
        self.timer = rumps.Timer(self.on_tick, 5)
        self.timer.stop()

        # menu items
        self.status_button = rumps.MenuItem(title="🔴 CockroachDB")
        self.start_stop_button = rumps.MenuItem(
            title="Start CockroachDB", callback=self.start_stop_crdb, key="S"
        )
        self.open_dbconsole_button = rumps.MenuItem(
            title="Open DBConsole", callback=self.open_dbconsole, key="W"
        )
        self.configure_start_button = rumps.MenuItem(
            title="Configure Start Command...",
            callback=self.configure_start_command,
            key="C",
        )
        self.configure_dbconsole_button = rumps.MenuItem(
            title="Configure DBConsole URL...",
            callback=self.configure_dbconsole_url,
            key="D",
        )
        self.configure_autostart_button = rumps.MenuItem(
            title="Start CockroachDB when app starts",
            callback=self.configure_autostart,
            key="A",
        )

        # need a custom quit button to make sure crdb shuts down before quitting
        self.quit_button = rumps.MenuItem(
            title="Quit",
            callback=self.graceful_shutdown,
            key="Q",
        )

        self.app.menu = [
            self.status_button,
            None,
            self.start_stop_button,
            None,
            self.open_dbconsole_button,
            self.configure_start_button,
            self.configure_dbconsole_button,
            self.configure_autostart_button,
            None,
            self.quit_button,
        ]

        if self.config.getboolean("DEFAULT", "autostart"):
            self.configure_autostart_button.state = True
            self.start_stop_crdb(self.start_stop_button)

    def read_config(self):
        # try reading the default ini file
        try:
            with self.app.open("macos_crdb_launcher.ini", "r") as f:
                self.config.read_file(f)

        except:
            # if the file doesn't exist, create a stub with default values
            self.config.set(
                "DEFAULT",
                "start",
                "/usr/local/bin/cockroach start-single-node --insecure --store=/tmp/cockroach-data",
            )
            self.config.set("DEFAULT", "autostart", "no")
            self.config.set("DEFAULT", "dbconsole_url", "http://localhost:8080")
            self.config.set("DEFAULT", "autostart", "no")

            self.write_config()

    def write_config(self):
        with self.app.open("macos_crdb_launcher.ini", "w") as f:
            self.config.write(f)

    def on_tick(self, sender):
        # check the pid is still valid
        p = subprocess.run(
            shlex.split("ps -o pid -p %s" % self.pid), capture_output=True, text=True
        )

        if str.find(p.stdout, self.pid) == -1:
            self.timer.stop()
            self.status_button.title = "🔴 CockroachDB"
            self.start_stop_button.title = "Start CockroachDB"

            rumps.notification(
                title="CockroachDB",
                subtitle="Unexpected failure",
                message="CockroachDB process has crashed unexpectedly.",
            )

    def start_stop_crdb(self, sender):
        if sender.title == "Start CockroachDB":
            p = subprocess.Popen(shlex.split(self.config.get("DEFAULT", "start")))
            self.pid = str(p.pid)

            self.status_button.title = "🟢 CockroachDB"
            sender.title = "Stop CockroachDB"
            self.timer.start()
        else:
            self.crdb_shutdown()

            self.status_button.title = "🔴 CockroachDB"
            sender.title = "Start CockroachDB"
            self.timer.stop()

    def open_dbconsole(self, sender):
        webbrowser.open_new_tab(self.config.get("DEFAULT", "dbconsole_url"))

    def crdb_shutdown(self):
        p = subprocess.run(["kill", self.pid])

        if p.returncode != 0:
            rumps.notification(
                title="CockroachDB",
                subtitle="Shutdown failed",
                message="Couldn't gracefully shutdown server, forced to kill the process",
            )
            subprocess.run(["kill", "-9", self.pid])

    def configure_start_command(self, sender):
        resp = rumps.Window(
            "Enter the command to run CockroachDB",
            "Start Up Command",
            self.config.get("DEFAULT", "start"),
            cancel="Cancel",
            dimensions=(320, 80),
        ).run()

        if resp.clicked:
            self.config.set("DEFAULT", "start", resp.text)
            self.write_config()

    def configure_dbconsole_url(self, sender):
        resp = rumps.Window(
            "Enter the DBConsole URL",
            "DBConsole URL",
            self.config.get("DEFAULT", "dbconsole_url"),
            cancel="Cancel",
            dimensions=(320, 60),
        ).run()

        if resp.clicked:
            self.config.set("DEFAULT", "dbconsole_url", resp.text)
            self.write_config()

    def configure_autostart(self, sender):
        if sender.state:
            self.config.set("DEFAULT", "autostart", "no")
        else:
            self.config.set("DEFAULT", "autostart", "yes")

        sender.state = not sender.state
        self.write_config()

    def graceful_shutdown(self, sender):
        self.crdb_shutdown()
        rumps.quit_application()

    def run(self):
        self.app.run()


App().run()
