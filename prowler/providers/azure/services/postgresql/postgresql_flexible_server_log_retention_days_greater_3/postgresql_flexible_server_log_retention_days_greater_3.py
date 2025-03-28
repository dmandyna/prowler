from prowler.lib.check.models import Check, Check_Report_Azure
from prowler.providers.azure.services.postgresql.postgresql_client import (
    postgresql_client,
)


class postgresql_flexible_server_log_retention_days_greater_3(Check):
    def execute(self) -> Check_Report_Azure:
        findings = []
        for (
            subscription,
            flexible_servers,
        ) in postgresql_client.flexible_servers.items():
            for server in flexible_servers:
                report = Check_Report_Azure(metadata=self.metadata(), resource=server)
                report.subscription = subscription
                report.status = "FAIL"
                report.status_extended = f"Flexible Postgresql server {server.name} from subscription {subscription} has log_retention disabled"
                if server.log_retention_days:
                    report.status_extended = f"Flexible Postgresql server {server.name} from subscription {subscription} has log_retention set to {server.log_retention_days}"
                    if (
                        int(server.log_retention_days) > 3
                        and int(server.log_retention_days) < 8
                    ):
                        report.status = "PASS"
                findings.append(report)

        return findings
