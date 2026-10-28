"""ScopeGuard: Enterprise authorization and scope verification engine.

Ensures that all scanning, penetration testing, and analysis strictly adhere to
authorized targets, eliminating illegal out-of-scope probes and collateral hazards.
"""

import fnmatch
import ipaddress
import re
from typing import List, Tuple
from cyberkill.config import settings

class ScopeGuard:
    """Verifies targets against white-lists, CIDR ranges, and black-lists."""

    def __init__(
        self,
        allowed_domains: List[str] = None,
        allowed_cidrs: List[str] = None,
        disallowed_domains: List[str] = None,
        strict: bool = True
    ):
        self.allowed_domains = allowed_domains or settings.scope.allowed_domains
        self.allowed_cidrs = allowed_cidrs or settings.scope.allowed_cidrs
        self.disallowed_domains = disallowed_domains or settings.scope.disallowed_domains
        self.strict = strict

    def is_ip(self, target: str) -> bool:
        try:
            ipaddress.ip_address(target)
            return True
        except ValueError:
            return False

    def validate_target(self, target: str) -> Tuple[bool, str]:
        """Validate whether a target is permitted for security operations.
        
        Returns:
            Tuple[bool, str]: (is_allowed, reason)
        """
        clean = re.sub(r"^https?://", "", target.strip()).split("/")[0].split(":")[0]

        # 1. Check disallowed blacklists first
        for pattern in self.disallowed_domains:
            if fnmatch.fnmatch(clean.lower(), pattern.lower()):
                return False, f"Target '{clean}' matches forbidden domain pattern '{pattern}'."

        # 2. Check if IP address
        if self.is_ip(clean):
            target_ip = ipaddress.ip_address(clean)
            for cidr in self.allowed_cidrs:
                try:
                    if target_ip in ipaddress.ip_network(cidr, strict=False):
                        return True, f"Target IP '{clean}' authorized under CIDR block '{cidr}'."
                except ValueError:
                    continue
            
            if not self.strict:
                return True, f"Target IP '{clean}' allowed (non-strict mode)."
            return False, f"Target IP '{clean}' is outside all authorized CIDR ranges."

        # 3. Check domain whitelist
        for pattern in self.allowed_domains:
            if pattern == "*" or pattern == clean or fnmatch.fnmatch(clean.lower(), pattern.lower()):
                return True, f"Target '{clean}' explicitly authorized by scope pattern '{pattern}'."

        if not self.strict:
            return True, f"Target '{clean}' allowed (non-strict mode)."

        return False, f"Target '{clean}' is not in authorized domain scope whitelist."

default_scope_guard = ScopeGuard()
