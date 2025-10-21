import sys
import os
import subprocess
import uuid
import hashlib
import re
from typing import List, Dict

def run_cmd(cmd: List[str]) -> str:
    try:
        out = subprocess.check_output(cmd, stderr=subprocess.DEVNULL, universal_newlines=True)
        return out.strip()
    except Exception:
        return ""

def get_macs() -> List[str]:
    """Return list of MAC-like strings found on the system."""
    results = []
    plat = sys.platform
    if plat.startswith("win"):
        # Use ipconfig /all or wmic
        out = run_cmd(["wmic", "nic", "where", "MACAddress IS NOT NULL", "get", "MACAddress", "/FORMAT:VALUE"])
        # parse MACAddress=00:11:22...
        for m in re.findall(r"MACAddress=(.+)", out):
            mac = m.strip()
            if mac:
                results.append(mac)
    elif plat == "darwin":
        out = run_cmd(["ifconfig", "-a"])
        # find hex pairs like xx:xx:xx:...
        results += re.findall(r"([0-9a-fA-F]{2}(?::[0-9a-fA-F]{2}){5})", out)
    else:
        # Assume Linux / BSD
        # Try ip link
        out = run_cmd(["ip", "link"])
        results += re.findall(r"link/[a-z0-9]+ ([0-9a-fA-F:]{17})", out)
        if not results:
            out = run_cmd(["ifconfig", "-a"])
            results += re.findall(r"([0-9a-fA-F]{2}(?::[0-9a-fA-F]{2}){5})", out)
    # uniq and normalized (uppercase)
    results = list(dict.fromkeys([r.upper() for r in results]))
    # fallback to uuid.getnode() if empty
    if not results:
        node = uuid.getnode()
        if (node >> 40) % 2 == 0:  # if it's a real MAC, low-order bit of first octet is 0
            mac = ":".join(f"{(node >> ele) & 0xff:02x}" for ele in range(40, -1, -8))
            results.append(mac.upper())
    return results

def get_machine_uuid() -> str:
    """Try platform-specific machine UUID / machine-id / hardware UUID."""
    plat = sys.platform
    if plat.startswith("win"):
        # Windows: use registry or wmic
        out = run_cmd(["wmic", "csproduct", "get", "UUID", "/FORMAT:VALUE"])
        m = re.search(r"UUID=(.+)", out)
        if m:
            return m.group(1).strip()
        # fallback: machine guid from registry (requires permissions)
        out = run_cmd(["reg", "query", r"HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Cryptography", "/v", "MachineGuid"])
        m = re.search(r"MachineGuid\s+REG_SZ\s+([0-9A-Fa-f-]+)", out)
        if m:
            return m.group(1).strip()
    elif plat == "darwin":
        # macOS: IOPlatformUUID
        out = run_cmd(["ioreg", "-rd1", "-c", "IOPlatformExpertDevice"])
        m = re.search(r'"IOPlatformUUID"\s*=\s*"(.+?)"', out)
        if m:
            return m.group(1)
    else:
        # linux: /etc/machine-id or /var/lib/dbus/machine-id
        for path in ("/etc/machine-id", "/var/lib/dbus/machine-id"):
            try:
                with open(path, "r") as f:
                    data = f.read().strip()
                    if data:
                        return data
            except Exception:
                pass
        # fallback: try hostname-based uuid via /sys/class/dmi/id/product_uuid (may need root)
        try:
            with open("/sys/class/dmi/id/product_uuid", "r") as f:
                pu = f.read().strip()
                if pu:
                    return pu
        except Exception:
            pass
    return ""

def get_disk_serials() -> Dict[str, str]:
    """
    Return mapping device -> serial (best-effort).
    On Windows uses wmic diskdrive get SerialNumber.
    On Linux uses lsblk/udevadm or hdparm (may need sudo).
    On macOS tries ioreg/system_profiler.
    """
    plat = sys.platform
    disks = {}
    if plat.startswith("win"):
        out = run_cmd(["wmic", "diskdrive", "get", "SerialNumber,DeviceID", "/FORMAT:LIST"])
        # parse lines like SerialNumber=XYZ and DeviceID=\\.\PHYSICALDRIVE0
        dev = None
        serial = None
        for line in out.splitlines():
            line = line.strip()
            if not line:
                continue
            if line.startswith("DeviceID="):
                dev = line.split("=", 1)[1].strip()
            elif line.startswith("SerialNumber="):
                serial = line.split("=", 1)[1].strip()
            if dev is not None and serial is not None:
                disks[dev] = serial
                dev = serial = None
    elif plat == "darwin":
        # Use system_profiler SPStorageDataType or ioreg; parsing text output
        out = run_cmd(["system_profiler", "SPStorageDataType"])
        # crude capture: "Serial Number: XXXXXXXXX"
        entries = re.findall(r"Device:.*?Serial Number: (.+)", out, flags=re.S)
        if entries:
            # map by index (since mapping device names is complex)
            for i, s in enumerate(entries):
                disks[f"disk_{i}"] = s.strip()
        else:
            # fallback: ioreg search
            out = run_cmd(["ioreg", "-r", "-c", "IOBlockStorageDevice"])
            mlist = re.findall(r'"Serial Number"\s=\s"(.+?)"', out)
            for i, s in enumerate(mlist):
                disks[f"disk_{i}"] = s.strip()
    else:
        # Linux: try lsblk -o NAME,SERIAL
        out = run_cmd(["lsblk", "-o", "NAME,SERIAL", "-P"])
        # example line: NAME="sda" SERIAL="123456789"
        for line in out.splitlines():
            name_m = re.search(r'NAME="([^"]+)"', line)
            ser_m = re.search(r'SERIAL="([^"]*)"', line)
            if name_m:
                name = "/dev/" + name_m.group(1)
                serial = ser_m.group(1) if ser_m else ""
                if serial:
                    disks[name] = serial
        # if none found, try udevadm for common devices:
        if not disks:
            # check common devices
            for dev in ["/dev/sda", "/dev/nvme0n1", "/dev/vda"]:
                if os.path.exists(dev):
                    out = run_cmd(["udevadm", "info", "--query=property", "--name", dev])
                    m = re.search(r"ID_SERIAL=(.+)", out)
                    if m:
                        disks[dev] = m.group(1).strip()
                    else:
                        # try hdparm (needs sudo)
                        out = run_cmd(["hdparm", "-I", dev])
                        m = re.search(r"Serial Number:\s*(\S+)", out)
                        if m:
                            disks[dev] = m.group(1).strip()
    return disks

def make_composite_id() -> str:
    """Create a hashed composite ID from machine UUID + first MAC + first disk serial (best-effort)."""
    parts = []
    mu = get_machine_uuid()
    if mu:
        parts.append(mu)
    macs = get_macs()
    if macs:
        parts.append(macs[0])
    disks = get_disk_serials()
    if disks:
        # take first serial value
        first_serial = next(iter(disks.values()))
        parts.append(first_serial)
    if not parts:
        # ultimate fallback: hostname + uuid.getnode()
        parts.append(str(uuid.getnode()))
        parts.append(os.uname().nodename if hasattr(os, "uname") else os.environ.get("COMPUTERNAME", "unknown"))
    combined = "|".join(parts)
    # return a stable SHA-256 hex
    return hashlib.sha256(combined.encode("utf-8")).hexdigest()

if __name__ == "__main__":
    print("MACs:", get_macs())
    print("Machine UUID:", get_machine_uuid())
    print("Disk Serials:", get_disk_serials())
    print("Composite hashed machine ID:", make_composite_id())
