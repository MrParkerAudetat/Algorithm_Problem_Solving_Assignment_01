"""Console styling and ANSI color utilities for readable terminal output.

This module provides ANSI escape sequences and convenience formatting functions
to highlight report titles, table headers, columns, rows, and validation warnings
without requiring any external third-party dependencies.
"""

import sys
import os

# ANSI escape codes for basic styling
RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"

# Standard foreground colors
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"
WHITE = "\033[97m"
GRAY = "\033[90m"


def supports_color():
    """Detect if the current environment supports ANSI color sequences."""
    if os.getenv("NO_COLOR"):
        return False
    if not hasattr(sys.stdout, "isatty") or not sys.stdout.isatty():
        return False
    return True


_USE_COLOR = supports_color()


def colorize(text, color_code, bold=False):
    """Wrap text in ANSI formatting if colors are supported."""
    if not _USE_COLOR:
        return text
    prefix = (BOLD if bold else "") + color_code
    return f"{prefix}{text}{RESET}"


def style_header(text):
    """Format major report header banner."""
    return colorize(text, CYAN, bold=True)


def style_sub_header(text):
    """Format section sub-headers and counts."""
    return colorize(text, BLUE, bold=True)


def style_policy(text):
    """Format policy descriptions."""
    return colorize(text, WHITE, bold=False)


def style_column_label(text):
    """Format column headers/field labels in dimmed cyan/white."""
    return colorize(text, CYAN, bold=True)


def style_table_header():
    """Format a distinct header line for the ticket table columns."""
    hdr = f"  {'ID':<6} {'STATUS':<9} {'PRIORITY':<10} {'CATEGORY':<11} {'AGE':<10}"
    sep = f"  {'-'*5}  {'-'*7}  {'-'*8}  {'-'*9}  {'-'*8}"
    return colorize(hdr, CYAN, bold=True) + "\n" + colorize(sep, GRAY)


def style_id(ticket_id):
    """Format ticket IDs with bold white."""
    return colorize(ticket_id, WHITE, bold=True)


def style_status(status):
    """Color-code ticket status: open (green), closed (gray)."""
    if status == "open":
        return colorize(status, GREEN, bold=True)
    elif status == "closed":
        return colorize(status, GRAY)
    return colorize(status, YELLOW)


def style_priority(priority):
    """Color-code ticket priority: high (bold red), normal (yellow), low (blue)."""
    if priority == "high":
        return colorize(f"{priority:<8}", RED, bold=True)
    elif priority == "normal":
        return colorize(f"{priority:<8}", YELLOW)
    elif priority == "low":
        return colorize(f"{priority:<8}", BLUE)
    return colorize(f"{priority:<8}", WHITE)


def style_category(category):
    """Format category labels with distinct colors."""
    if category == "access":
        return colorize(f"{category:<9}", MAGENTA)
    elif category == "software":
        return colorize(f"{category:<9}", CYAN)
    elif category == "network":
        return colorize(f"{category:<9}", BLUE)
    return colorize(f"{category:<9}", WHITE)


def style_age(age_days):
    """Color-code age to draw attention to older tickets."""
    age_str = f"{age_days:>2} days"
    if age_days >= 3:
        return colorize(age_str, YELLOW, bold=True)
    elif age_days == 2:
        return colorize(age_str, WHITE)
    return colorize(age_str, GRAY)


def style_pipe():
    """Format table vertical dividers in subtle gray."""
    return colorize("|", GRAY)


def style_review_record(text):
    """Format records needing review completely in bold bright red."""
    return colorize(text, RED, bold=True)


def style_badge():
    """Format attention badge for invalid/review records."""
    return colorize("[NEEDS REVIEW]", RED, bold=True)

