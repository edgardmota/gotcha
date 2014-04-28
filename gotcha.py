#!/usr/bin/env python
# -*- coding: utf-8 -*-
import subprocess as sp
import time 

LAST_ONE_MINUTE = 0
LAST_FIVE_MINUTES = 1
LAST_FIFTEEN_MINUTES = 2
LOAD_AVG_THRESHOULD = 2.4
WAIT_ON_IDLE = 1
WAIT_ON_BUSY = 10
LOG_DIRECTORY = '/tmp/gotcha'
LOG_FILENAME_BASE = 'processes'
LOG_TIMESTAMP_FORMAT = '%Y-%m-%d-%H%M'
PROCESSES_LIST_COMMAND = 'ps aux'

def get_output(raw_command):
	command_in_list = raw_command.split()
	command = command_in_list[0]
	args = command_in_list[1:]
	return sp.Popen([command] + args, stdout=sp.PIPE).communicate()[0]

def get_load_avg(metric):
	uptime_output = get_output('uptime')
	values = uptime_output.split(':')[-1].strip()
	return float(values.split(',')[metric])

def wait(busy):
	if busy:
		time_to_wait = WAIT_ON_BUSY
	else:
		time_to_wait = WAIT_ON_IDLE
	time.sleep(time_to_wait * 60)

def log(load_avg_fifteen,process_list):
	log_filename = '_'.join([
							LOG_FILENAME_BASE,
							time.strftime(LOG_TIMESTAMP_FORMAT),
							str(load_avg_fifteen),
							])
	file = open('/'.join([LOG_DIRECTORY,log_filename]),'w')
	file.write(process_list)
	file.close()

def snapshot_processes(load_avg_fifteen):
	process_list = get_output(PROCESSES_LIST_COMMAND)
	log(load_avg_fifteen,process_list)

def main():
	busy = False
	while(True):
		load_avg_fifteen = get_load_avg(LAST_FIFTEEN_MINUTES)
		print 'Checando...'
		if load_avg_fifteen > LOAD_AVG_THRESHOULD:
			print 'NOK: Logando... (%s)' % str(load_avg_fifteen)
			busy = True
			snapshot_processes(load_avg_fifteen)
			print 'Logado!'
		else:
			print 'OK!'
			busy = False
		print 'Aguardando próxima checagem...'
		wait(busy)

main()
