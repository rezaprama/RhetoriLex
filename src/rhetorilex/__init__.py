"""RhetoriLex: offline, evidence-aware academic rhetoric templates."""

from .catalog import Catalog, Entry, SearchResult
from .contracts import ContractIssue, check_entry_contract

__all__ = [
    "Catalog",
    "ContractIssue",
    "Entry",
    "SearchResult",
    "check_entry_contract",
]
__version__ = "0.2.0"
