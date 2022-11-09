FROM ubuntu

# Update package manager and download required tools for troubleshooting
RUN apt-get update && apt-get install -y sudo syslog-ng iputils-ping strace vim nmap lsof net-tools;

# Create sstem group and account to run following commands with given privileges
RUN groupadd -r -g 1000 syslog && useradd -r -g syslog -u 999 syslog

# Change version configuration of syslog 
RUN chown syslog:syslog /etc/syslog-ng/ /var/lib/syslog-ng/ /dev/ && sed -i "1s/.*/@version: 3.35/" /etc/syslog-ng/syslog-ng.conf

# Add syslog configuration to working directory
ADD ./client.conf /client.conf

RUN mv client.conf /etc/syslog-ng/conf.d/

HEALTHCHECK --interval=2m --timeout=3s --start-period=30s --retries=3 CMD /usr/sbin/syslog-ng-ctl stats || exit 1

# Commented for now because of the /dev/log accessibility issues
# USER syslog

# set entrypoint to execute syslog-ng
ENTRYPOINT [ "/usr/sbin/syslog-ng", "-F", "--no-caps" ]

