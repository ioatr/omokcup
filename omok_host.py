# -*- encoding: utf8 -*-

import os
import sys
import time
from select import select
from subprocess import *

import util
import core.config
import core.omok
import core.omok_screen

BOARD_SIZE = core.config.BOARD_SIZE
EYE_OFFSET = 3
BLACK = 1
WHITE = 2

TOTAL_ROUND = 5

# 흑/백간의 쉬는 시간
SLEEP = 0.2
# 타임아웃
TIME_OUT = 30
DEFAULT_CLIENT = 'omok_client.py'


class OmokException(Exception):
	def __init__(self, turn, reason):
		self.turn = turn
		self.reason = reason


class PipeClient:
	def __init__(self, args):
		self.proc = Popen(args, shell=False, bufsize=2048, stdin=PIPE, stdout=PIPE, stderr=PIPE)
		return
	

	def send_msg(self, turn, obj):
		try:
			self.proc.stdin.write(str(obj) + '\n')
			self.proc.stdin.flush()
		except:
			raise OmokException(turn, '')


	def get_msg(self, turn):		
		if os.name == 'nt':
			# nt is window
			# select, window is not support
			msg =  self.proc.stdout.readline().rstrip()
			return map(int, msg.split())
		else:
			has_msg, _, _ = select([self.proc.stdout], [], [], TIME_OUT)
			if has_msg:
				msg = self.proc.stdout.readline().rstrip('\n')
				return map(int, msg.split())
			else:
				self.proc.kill()
				raise OmokException(turn, 'timeout')


	def quit(self):
		if self.proc.returncode is None:
			self.proc.stdin.write('quit\n')



class ManualClient:
	def __init__(self, game, screen):
		self.game = game
		self.screen = screen
		return
	

	def send_msg(self, turn, obj):
		return

	
	def get_msg(self, turn):
		return self.screen.get_player_input(self.game.map, self.game.turn)


	def quit(self):
		return
	


def send_msg(client, turn, obj):
	client.send_msg(turn, obj)


def get_msg(client, turn):
	return client.get_msg(turn)


def set_color(code, text):
	if not util.supports_color():
		return text

	if code == BLACK:
		return '\x1b[6;37;40m{}\x1b[0m'.format(text)
	elif code == WHITE:
		return '\x1b[6;30;47m{}\x1b[0m'.format(text)
	elif code == 'g':
		return '\x1b[6;30;42m{}\x1b[0m'.format(text)
	elif code == 'r':
		return '\x1b[6;37;41m{}\x1b[0m'.format(text)
	else:
		return text


def _get_username(user):
	if user == BLACK:
		return 'BLACK'
	elif user == WHITE:
		return 'WHITE' 


def get_client(args, game, screen):
	if args[0] is 'manual':
		return ManualClient(game, screen)
	else:
		return PipeClient(args)


def do_game(args1, args2, turn=BLACK, screen=None):

	game = core.omok.Omok()
	game.turn = turn

	# invoke first player
	p1 = get_client(args1, game, screen) 

	# invoke another player
	p2 = get_client(args2, game, screen)

	x, y = -1, -1
	players = [None, p1, p2]

	# 플레이어에게 자신의 턴을 알려준다
	send_msg(p1, BLACK, BLACK)
	send_msg(p2, WHITE, WHITE)

	# draw
	game.draw(screen)

	while True:
		turn = game.turn
		player = players[game.turn]

		# 플레이어에게 전 플레이어의 수를 알려준다
		send_msg(player, turn, '{} {}'.format(x, y))

		# 플레이어의 수를 가져온다
		x, y = get_msg(player, turn)

		# 게임 진행
		ret = game.step(x, y)

		# print log
		game.draw(screen)
		print set_color(turn, '{}({}) put {}, {}'.format(_get_username(turn), turn, x, y))
		
		# 게임 진행중 체크, -1은 진행 중
		if ret != -1:
			break

		# wait
		time.sleep(SLEEP)

	# quit process
	p1.quit()
	p2.quit()
	
	return ret


def do(args1, args2):
	screen = core.omok_screen.OmokScreen()
	turn = BLACK
	wins = {BLACK:0, WHITE:0}
	winner = None

	# print vs
	print set_color('g', '{} vs {}'.format('-'.join(args1), '-'.join(args2)))
	time.sleep(1)

	for _round in xrange(TOTAL_ROUND):

		# print round
		print set_color('g', 'ROUND{}'.format(_round))
		time.sleep(1)

		try:
			res = do_game(args1, args2, turn, screen)
			winner = res

		except OmokException as e:
			# 플레이어가 예외상황(타임아웃)이라면, 상대 플레이어 승으로 간주한다
			winner = EYE_OFFSET - e.turn
			print set_color('r', '{} IS TIMEOUT'.format(_get_username(e.turn)))

		except:
			import traceback
			traceback.print_exc()
			sys.exit("Fatal Error")

		# 승리자
		wins[winner] += 1
		turn = EYE_OFFSET - turn

		print set_color('g', 'WINNER IS {}'.format(_get_username(winner)))
		print ''

		time.sleep(3)

	# 결과 출력
	who_win = max(enumerate(wins), key=lambda x: x[1])[0]
	print set_color('g', 'Black {} : White {}'.format(wins[BLACK], wins[WHITE]))
	print set_color('g', 'Finnaly Winner is {}'.format(_get_username(who_win)))



if __name__ == '__main__':
	import optparse
	import os

	parser = optparse.OptionParser(usage='%prog ai_1 ai_2')
	options, args = parser.parse_args()

	def make_args(args, i):
		if len(args) > i:
			filename = args[i]
		else:
			filename = DEFAULT_CLIENT
		
		ext = os.path.splitext(filename)[1]
		if filename in {'m', 'manual'}:
			return ['manual']
		elif ext in {'.py'}:
			return ['python', filename]
		elif ext in {'.exe'}:
			return [filename]
		else:
			raise Exception('{} is not supported'.format(filename))

	args1 = make_args(args, 0)
	args2 = make_args(args, 1)

	# omok
	do(args1, args2)
