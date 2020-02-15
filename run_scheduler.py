import omicron_server

if __name__ == '__main__':
    omicron_server.logger.info("Scheduler start")
    omicron_server.scheduler.run()
