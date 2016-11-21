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
SLEEP = 1
# 타임아웃
TIME_OUT = 30
DEFAULT_CLIENT = 'omok_client.py'


class Player():
	index = 0
	args = None
	client = None

	def __init__(self, index, args):
		self.index = index
		self.args = args


	def getname(self):
		if self.index == BLACK:
			return 'Player1'
		elif self.index == WHITE:
			return 'Player2' 



class OmokException(Exception):
	def __init__(self, player, reason):
		self.player = player
		self.reason = reason


class PipeClient:
	def __init__(self, player):
		self.proc = Popen(player.args, shell=False, bufsize=2048, stdin=PIPE, stdout=PIPE, stderr=PIPE)
		return
	

	def send_msg(self, player, obj):
		try:
			self.proc.stdin.write(str(obj) + '\n')
			self.proc.stdin.flush()
		except:
			raise OmokException(player, '')


	def get_msg(self, player):		
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
				raise OmokException(player, 'timeout')


	def quit(self):
		if self.proc.returncode is None:
			self.proc.stdin.write('quit\n')



class ManualClient:
	def __init__(self, game, screen):
		self.game = game
		self.screen = screen
		return
	

	def send_msg(self, player, obj):
		return

	
	def get_msg(self, player):
		return self.screen.get_player_input(self.game.map, self.game.turn)


	def quit(self):
		return
	


def send_msg(player, obj):
	player.client.send_msg(player, obj)


def get_msg(player):
	return player.client.get_msg(player)


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


def set_client(player, game, screen):
	if player.args[0] is 'manual':
		player.client = ManualClient(game, screen)
	else:
		player.client = PipeClient(player)


def do_game(players, turn=BLACK, screen=None):

	game = core.omok.Omok()
	game.turn = BLACK

	# init
	x, y = -1, -1

	# invoke player
	set_client(players[BLACK], game, screen)
	set_client(players[WHITE], game, screen)

	# 플레이어에게 자신의 턴을 알려준다
	send_msg(players[BLACK], BLACK)
	send_msg(players[WHITE], WHITE)

	# draw
	game.draw(screen)

	while True:
		turn = game.turn
		player = players[game.turn]

		# 플레이어에게 전 플레이어의 수를 알려준다
		send_msg(player, '{} {}'.format(x, y))

		# 플레이어의 수를 가져온다
		x, y = get_msg(player)

		# 게임 진행
		ret = game.step(x, y)
		screen.play_sound('sound/tock.wav')

		# print log
		game.draw(screen)
		print set_color(turn, '{} put {}, {}'.format(player.getname(), x, y))
		
		# 게임 진행중 체크, -1은 진행 중
		if ret != -1:
			break

		# wait
		time.sleep(SLEEP)

	# quit process
	players[BLACK].client.quit()
	players[WHITE].client.quit()
	
	return players[ret]


def do(args1, args2):
	screen = core.omok_screen.OmokScreen()
	wins = {BLACK:0, WHITE:0}
	winner = None

	p1 = Player(1, args1)
	p2 = Player(2, args2)
	players = None

	# print vs
	print set_color('g', '{} vs {}'.format('-'.join(args1), '-'.join(args2)))
	time.sleep(1)

	for _round in xrange(TOTAL_ROUND):

		# print round
		print set_color('g', 'ROUND{}'.format(_round))
		time.sleep(1)

		try:
			# 라운드 마다 순서 교체
			if _round % 2 == 0:
				players = [None, p1, p2]
			else:
				players = [None, p2, p1]

			# print first player
			print set_color('g', '{} is First'.format(players[BLACK].getname()))
			time.sleep(1)

			# do omok
			res = do_game(players, BLACK, screen)
			winner = res

			# sound
			screen.play_sound('sound/win.wav')

		except OmokException as e:
			# 플레이어가 예외상황(타임아웃)이라면, 상대 플레이어 승으로 간주한다
			winner = players[EYE_OFFSET - e.index]
			print set_color('r', '{} IS TIMEOUT'.format(e.getname()))

		except:
			import traceback
			traceback.print_exc()
			sys.exit("Fatal Error")

		# 승리자
		wins[winner.index] += 1

		print set_color('g', 'WINNER IS {}'.format(winner.getname()))
		print ''

		time.sleep(3)

	# 결과 출력
	who_win = max(enumerate(wins), key=lambda x: x[1])[0]
	print set_color('g', 'Player1 {} : Player2 {}'.format(wins[1], wins[2]))
	print set_color('g', 'Finnaly Winner is {}'.format(players[who_win].getname()))



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
