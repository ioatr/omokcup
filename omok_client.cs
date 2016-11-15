using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace OmokClientExample
{
    public class OmokClient
    {
        const int EYE_OFFSET = 3;

        public int boardSize;
        public int[,] board;

        public int myId;

        public OmokClient(int boardSize)
        {
            this.boardSize = boardSize;
            this.board = new int[boardSize, boardSize];
        }

        string _get()
        {
            // 호스트와 통신
            return Console.ReadLine().Trim();
        }

        void _put(string text)
        {
            // 호스트와 통신
            Console.WriteLine(text);
            Console.Out.Flush();
        }

        public Tuple<int, int, int> get()
        {
            // 호스트에게 상태와 상대의 좌표를 가져온다.
            var tmp = _get();
            if (tmp == "quit")
                return Tuple.Create(-1, -1, -1);

            var xy = tmp.Split();
            var x = int.Parse(xy[0]);
            var y = int.Parse(xy[1]);
            if (x != -1 || y != -1)
                board[y, x] = EYE_OFFSET - myId;

            return Tuple.Create(1, x, y);
        }

        public void put(int x, int y)
        {
            board[y, x] = myId;
            // 나의 수(좌표)를 호스트에게 알려준다.
            _put(string.Format("{0} {1}", x, y));
        }

        public void ready()
        {
            // 호스트로부터 아이디를 가져옵니다.
            myId = int.Parse(_get());
        }
    }
}
