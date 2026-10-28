"""Asynchronous process manager with real-time stream capture and timeout controls."""

import asyncio
import os
import signal
import time
from typing import Dict, List, Optional, Tuple

class ManagedProcess:
    def __init__(self, pid: int, command: str, target: str = ""):
        self.pid = pid
        self.command = command
        self.target = target
        self.start_time = time.time()
        self.end_time: Optional[float] = None
        self.status = "RUNNING"
        self.exit_code: Optional[int] = None
        self.stdout_buffer: List[str] = []
        self.stderr_buffer: List[str] = []

    @property
    def duration(self) -> float:
        if self.end_time:
            return round(self.end_time - self.start_time, 2)
        return round(time.time() - self.start_time, 2)

    def to_dict(self) -> dict:
        return {
            "pid": self.pid,
            "command": self.command,
            "target": self.target,
            "status": self.status,
            "duration_seconds": self.duration,
            "exit_code": self.exit_code,
            "stdout_preview": "".join(self.stdout_buffer[-20:]) if self.stdout_buffer else ""
        }

class ProcessManager:
    """Manages concurrent tool executions with asynchronous event loops."""

    def __init__(self):
        self.active_processes: Dict[int, ManagedProcess] = {}
        self.completed_processes: Dict[int, ManagedProcess] = {}

    async def execute_command(
        self,
        command: str,
        timeout: int = 300,
        target: str = ""
    ) -> Tuple[int, str, str]:
        """Execute a shell command asynchronously with strict timeout and buffer capture."""
        proc = await asyncio.create_subprocess_shell(
            command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        managed = ManagedProcess(pid=proc.pid, command=command, target=target)
        self.active_processes[proc.pid] = managed

        try:
            stdout_data, stderr_data = await asyncio.wait_for(
                proc.communicate(),
                timeout=float(timeout)
            )
            managed.exit_code = proc.returncode
            managed.status = "COMPLETED" if proc.returncode == 0 else "FAILED"
            stdout_str = stdout_data.decode("utf-8", errors="replace")
            stderr_str = stderr_data.decode("utf-8", errors="replace")
            managed.stdout_buffer = stdout_str.splitlines(keepends=True)
            managed.stderr_buffer = stderr_str.splitlines(keepends=True)
        except asyncio.TimeoutError:
            try:
                proc.kill()
            except ProcessLookupError:
                pass
            managed.status = "TIMED_OUT"
            managed.exit_code = -1
            stdout_str = ""
            stderr_str = f"Execution timed out after {timeout} seconds."
        finally:
            managed.end_time = time.time()
            if proc.pid in self.active_processes:
                del self.active_processes[proc.pid]
            self.completed_processes[proc.pid] = managed

        return managed.exit_code or 0, stdout_str, stderr_str

    def terminate_process(self, pid: int) -> bool:
        if pid in self.active_processes:
            try:
                os.kill(pid, signal.SIGTERM)
                self.active_processes[pid].status = "TERMINATED"
                return True
            except OSError:
                return False
        return False

    def list_active(self) -> List[dict]:
        return [p.to_dict() for p in self.active_processes.values()]

    def list_completed(self, limit: int = 50) -> List[dict]:
        items = list(self.completed_processes.values())[-limit:]
        return [p.to_dict() for p in reversed(items)]

global_process_manager = ProcessManager()
