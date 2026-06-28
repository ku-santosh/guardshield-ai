import sys
import json
import logging
from datetime import datetime
from typing import Any, Dict, Optional


class StructuredJsonFormatter(logging.Formatter):    
    """
    Standardizes log generation structures into clean, machine-readable JSON strings.
    """

    def format(self, record: logging.LogRecord) -> str:
        log_record: Dict[str, Any] = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "message": record.getMessage(),
            "logger": record.name,
            "module": record.module,
            "function": record.funcName,
            "line_no": record.lineno,
        }

        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)
        
        # Merge custom contextual metrics injected during runtime
        if hasattr(record, "extra_context"):
            log_record.update(record.extra_context)

        return json.dumps(log_record)
    
    def setup_logging() -> logging.Logger:
        """
        Configures the logging system to use the StructuredJsonFormatter for all log messages.
        """
        logger = logging.getLogger("GuardShieldLogger")
        logger.setLevel(logging.INFO)

        if not logger.handlers:
            # Create console handler with structured JSON formatter
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(StructuredJsonFormatter())
            logger.addHandler(console_handler)        

        return logger
    
    system_logger = setup_logging()
