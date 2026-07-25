import re

# 1. Define sets outside the function (fixed missing commas & lowercased)
ENV_KEYWORDS = {
    "development": {
        "compile", "compiler", "compilation", "source", "repository", "branch",
        "debug", "debugging", "localhost", "patch", "commit", "implementation",
        "build", "build failure", "merge", "developer", "sdk", "framework",
        "command line", "cli", "library", "refactor", "trace", "config", "plugin",
        "coding", "svn", "git", "local machine", "dev environment", "workspace",
        "api", "configuration", "dependency", "eclipse", "intellij", "visual studio",
        "vscode", "netbeans"
    },
    "staging": {
        "qa", "testing", "test", "uat", "staging", "regression", "nightly", "ci",
        "pipeline", "preproduction", "pre-production", "verification", "test case",
        "unit test", "integration test", "test suite", "test plan", "validation",
        "integration", "automation", "continuous integration", "continuous delivery",
        "reproduce", "reproduced", "reproduction", "expected result", "actual result",
        "sandbox", "preview"
    },
    "production": {
        "production", "prod", "customer", "customers", "client", "clients",
        "deployment", "deployed", "deploy", "release", "rollout", "released",
        "release version", "crash", "fatal error", "data corruption", "incident",
        "security vulnerability", "live", "live system", "live server", "outage",
        "downtime", "service unavailable", "service disruption", "end user",
        "end users", "data loss", "authentification", "authentification failure",
        "network", "frontend", "monitoring", "logging", "aws", "azure", "gcp",
        "payment", "cloud", "authorization", "authorization failure", "server",
        "billing", "database", "cannot login", "users cannot", "affects customers",
        "customer impact", "user reported", "reported by customer", "in production",
        "production issue", "cannot access", "multiple users", "emergency",
        "severe", "invoice", "subscription", "revenue", "cluster", "access",
        "public release", "rollback"
    }
}

# 1. Define explicit priority lookup matrix
PRIORITY_MAP = {
    # Severity 3 (High)
    (3, "production"): "critical",
    (3, "staging"):    "critical",
    (3, "development"): "high",
    
    # Severity 2 (Medium)
    (2, "production"): "medium",
    (2, "staging"):    "medium",
    (2, "development"): "low",
    
    # Severity 1 (Low)
    (1, "production"): "medium",
    (1, "staging"):    "low",
    (1, "development"): "low",
}

#Role assignment mapping for severity and environment
FRONTEND_TERMS = {
    "ui", "layout", "frontend", "dom", "html", "css", "javascript", "browser",
    "writer", "spreadsheet", "mailer", "swt", "display", "interface", "rendering", "xul"
}

BACKEND_TERMS = {
    "server", "backend", "api", "core", "service", "network", "authentication",
    "authorization", "java", "logic", "javascript engine"
}

SYSTEMS_TERMS = {
    "c++", "libstdc++", "c", "fortran", "compiler", "optimization",
    "tree-optimization", "rtl-optimization", "middle-end", "bootstrap",
    "target", "driver", "drivers", "drm", "directx", "mesa", "kernel",
    "memory", "concurrency"
}

DATABASE_TERMS = {
    "database", "sql", "storage", "query", "schema", "transaction", "postgres", "mysql"
}

DEVOPS_TERMS = {
    "server operations", "deployment", "build", "ci/cd", "pipeline", "cloud",
    "docker", "kubernetes", "infrastructure", "release", "configuration"
}

PRODUCT_TERMS = {
    "documentation", "feature request", "enhancement", "requirements"
}

GENERIC_COMPONENTS = {"other", "general", "-unknown", "unknown", "", "nan"}
