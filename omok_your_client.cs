using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace OmokClientExample
{
    class Program
    {
        const int BOARD_SIZE = 15;

        static Tuple<int, int> Choose(int myId, int px, int py, int[,] board)
        {
            // my_id: 나의 식별자 (흑:1, 백: 2)
            // px, py: 방금전 상대편이 둔 수 (주의!맨 처음 수는 - 1, -1로 주어진다)
            // board: 현재 상태 수

            var boardSize = board.Length;
            for (var y = 0; y < boardSize; ++y)
                for (var x = 0; y < boardSize; ++x)
                    if (board[y, x] == 0)
                        return Tuple.Create(x, y);

            return Tuple.Create(-1, -1);
        }

        static void Main(string[] args)
        {
            var game = new OmokClient(BOARD_SIZE);
            game.ready();

            while (true)
            {
                // sync
                var tmp = game.get();
                if (tmp.Item1 == -1)
                    break;

                var x = tmp.Item2;
                var y = tmp.Item3;

                // 자신의 수 선택
                var choose = Choose(game.myId, x, y, game.board);
                x = choose.Item1;
                y = choose.Item2;

                // sync
                game.put(x, y);
            }
        }
    }
}
