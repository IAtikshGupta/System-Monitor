import psutil
import tkinter as tk
from tkinter import ttk
import time

update_ms = 1000


class SystemMonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sytsem Monitor")
        self.root.geometry("420x650")
        self.root.resizable(False, False)

        self.old = psutil.net_io_counters()
        self.last_time = time.time()
        self.boot_time = psutil.boot_time()
        

        self.buildLayout()
        self.update()


    def buildLayout(self):
        cont = ttk.Frame(self.root, padding=20)
        cont.pack(fill="both", expand = True,)

        title=ttk.Label(cont, text="System Monitor", font=("Arial", 18, "bold"))
        title.pack(pady=(0,10))

        self.cpu_label, self.cpu_bar = self.makeStatRow(cont, "CPU")
        self.ram_label, self.ram_bar = self.makeStatRow(cont, "RAM")
        self.disk_label, self.disk_bar = self.makeStatRow(cont, "Disk (C:/)")

        net_frame = ttk.LabelFrame(cont, text="Network", padding=10)
        net_frame.pack(fill="x", pady=(16, 0))
        self.netUpLabel = ttk.Label(net_frame, text="Upload:   0.0 Mbps")
        self.netUpLabel.pack(anchor="w")
        self.netDownLabel = ttk.Label(net_frame, text="Download:   0.0 Mbps")
        self.netDownLabel.pack(anchor="w")

        core_frame = ttk.LabelFrame(cont, text="Per-Core CPU", padding=10)
        core_frame.pack(fill="x", pady=(16, 0))
        self.core_label = ttk.Label(core_frame, text="", justify="left")
        self.core_label.pack(anchor="w")

        self.uptime_label = ttk.Label(cont, text="Uptime: --")
        self.uptime_label.pack(pady=(16, 0))


    def makeStatRow(self, parent, name):
        frame = ttk.Frame(parent)
        frame.pack(fill="x", pady=6)

        label=ttk.Label(frame, text=f"{name}: --%", width = 22, anchor="w")
        label.pack(side="left")

        bar = ttk.Progressbar(frame, orient="horizontal", length=200, mode="determinate", maximum=100)
        bar.pack(side="left", pady=(8, 0))

        return label, bar

    def update(self):
        cpuVal = psutil.cpu_percent(interval=None, percpu=True)
        core_text = "\n".join(
            f"Core {i}: {pct:5.1f}%" for i, pct in enumerate(cpuVal)
        )
        self.core_label.config(text=core_text)
        trueCPU = sum(cpuVal)/len(cpuVal)
        self.cpu_label.config(text=f"CPU: {trueCPU:.1f}%")
        self.cpu_bar.config(value=trueCPU)

        mem = psutil.virtual_memory()
        self.ram_label.config(text=f"RAM: {mem.percent:.1f}%")
        self.ram_bar.config(value=mem.percent)

        disk = psutil.disk_usage("C:/")
        self.disk_label.config(text=f"Disk (C:/): {disk.percent:.1f}%")
        self.disk_bar["value"] = disk.percent

        now = time.time()
        new = psutil.net_io_counters()
        elapsed = max(now - self.last_time, 1e-6)
        
        upload_speed = round((new.bytes_sent - self.old.bytes_sent) / elapsed * 8 / 1_000_000, 1)
        download_speed = round((new.bytes_recv - self.old.bytes_recv) / elapsed * 8 / 1_000_000, 1)
        self.netUpLabel.config(text=f"Upload:   {upload_speed:.1f} Mbps")
        self.netDownLabel.config(text=f"Download: {download_speed:.1f} Mbps")

        self.old = new
        self.last_time =  now

        boot_time = psutil.boot_time()
        uptime_sec = int(time.time() - boot_time)
        h, remainder = divmod(uptime_sec, 3600)
        mins, sec = divmod(remainder, 60)
        self.uptime_label.config(text=f"Uptime: {h}h {mins}m {sec}s")

        self.root.after(update_ms, self.update)


def main():
    root = tk.Tk()
    app = SystemMonitorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()

