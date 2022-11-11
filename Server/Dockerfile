FROM ubuntu

# Update package manager and download required tools for troubleshooting
RUN apt-get update && apt-get install -y sudo syslog-ng iputils-ping strace vim nmap lsof net-tools;

# Create sstem group and account to run following commands with given privileges
RUN groupadd -r -g 1000 syslog && useradd -r -g syslog -u 999 syslog

# Create directory for collected logs
RUN sudo mkdir /var/log/syslog-ng && sudo chown syslog:syslog /var/log/syslog-ng

# Change version configuration of syslog 
RUN chown syslog:syslog /etc/syslog-ng/ /var/lib/syslog-ng/ /dev/ && sed -i "1s/.*/@version: 3.35/" /etc/syslog-ng/syslog-ng.conf

# Consider adding the log directly to the database
RUN apt-get install -y libdbd-pgsql

# Add syslog configuration to working directory
ADD ./server.conf /server.conf

# Move configuration into the right place
RUN sudo mv server.conf /etc/syslog-ng/conf.d/


# Change user to syslog
HEALTHCHECK --interval=2m --timeout=3s --start-period=30s --retries=3 CMD /usr/sbin/syslog-ng-ctl stats || exit 1

# Commented for now because of the /dev/log accessibility issues
# USER syslog

# set entrypoint to execute syslog-ng
ENTRYPOINT [ "/usr/sbin/syslog-ng", "-F", "--no-caps" ]


