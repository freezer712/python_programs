# coding=utf-8
from enum import Enum


class PieceType(Enum):
    # 为序列值指定value值
    empty = 0
    white = 1
    black = 2


class SuperPiece:

    def __init__(self):
        self.type = PieceType.empty

    def is_empty(self) -> bool:
        """
        Determine whether the piece is empty.

        Returns:
            bool: True if the piece is empty
        """
        raise NotImplementedError

    def is_black(self) -> bool:
        """
        Determine whether the piece is black.

        Returns:
            bool: True if the piece is black
        """
        raise NotImplementedError

    def is_white(self) -> bool:
        """
        Determine whether the piece is white.

        Returns:
            bool: True if the piece is white
        """
        raise NotImplementedError

    def set_piece_type(self, p):
        self.type = p


class SuperChessboard:

    def __init__(self, size: int):
        """
        Initialization.

        Args:
            size (int): the length and width of the chessboard
        """
        self.size = size
        self.board = []
        a = []
        for i in range(self.size):
            a = []
            for j in range(self.size):
                p = Piece()
                a.append(p)
            self.board.append(a)

    def get_board_size(self) -> int:
        """
        Get the chessboard size.

        Returns:
            int: the size of the chessboard
        """
        return self.size

    def set_piece(self, piece: SuperPiece, position: tuple) -> bool:
        """
        Set a given piece in a given position only if the position in the chessboard
        is empty.
        
        Args:
            piece (SuperPiece): the piece to be set
            position (tuple): the position to set the piece, with the form of (x,y), 
            x is the row index and y is the column index, which should large than 0,
            i.e. x,y is in [1, size]

        Returns:
            bool: True if the piece is set successfully; False is there is not empty
            in the given position.
        """
        raise NotImplementedError

    def set_black_piece(self, position: tuple) -> bool:
        """
        Set a black piece in a given position only if the position in the chessboard
        is empty.
        
        Args:
            position (tuple): the position to set the piece, with the form of (x,y), 
            x is the row index and y is the column index, which should large than 0,
            i.e. x,y is in [1, size]

        Returns:
            bool: True if the piece is set successfully; False is there is not empty
            in the given position.
        """
        raise NotImplementedError

    def set_white_piece(self, position: tuple) -> bool:
        """
        Set a white piece in a given position only if the position in the chessboard
        is empty.
        
        Args:
            position (tuple): the position to set the piece, with the form of (x,y), 
            x is the row index and y is the column index, which should large than 0,
            i.e. x,y is in [1, size]

        Returns:
            bool: True if the piece is set successfully; False is there is not empty
            in the given position.
        """
        raise NotImplementedError

    def set_empty_piece(self, position: tuple):
        """
        Set a empty piece in a given position.
        
        Args:
            position (tuple): the position to set the piece, with the form of (x,y), 
            x is the row index and y is the column index, which should large than 0,
            i.e. x,y is in [1, size]
        """
        raise NotImplementedError

    def get_piece(self, position: tuple) -> SuperPiece:
        """
        Get the piece in the given position.

        Args:
            position (tuple): querying position, with the form of (x,y), 
            x is the row index and y is the column index, which should large than 0,
            i.e. x,y is in [1, size]

        Returns:
            SuperPiece: the piece in the given position
        """
        raise NotImplementedError

    def isEmpty(self, position: tuple) -> bool:
        """
        Determine whether the position in the chessboard is empty.

        Args:
            position (tuple): querying position, with the form of (x,y), 
            x is the row index and y is the column index, which should large than 0,
            i.e. x,y is in [1, size]

        Returns:
            bool: True if the piece in the given position is empty
        """
        raise NotImplementedError


class SuperGame:
    def __init__(self):
        """
        Initialization. We have initialized the `display` and `round_num`, but left the
        `board_size` and `board` uninitialized.
        """
        self.display = Display()
        self.round_num = 0

        # 以下参数需要初始化
        self.board_size = 0
        self.board = None

    def set_size(self, size):
        self.board_size = size
        self.board = Chessboard(size)

    def start(self):
        """
        Start the game.
        """
        self.game_loop()

    def show_board(self):
        """
        Show current chessboard to the user.
        """
        self.display.display_board(self.board)

    def game_loop(self):
        """
        Start the game main loop.
        In this function, you should first call the `self.display.display_help_info()`,
        then enter a for/while loop, in which you should do things bellow:
            1. update `self.round_num`.
            2. diaplsy current round info by calling `self.display.display_round`.
            3. display chessboard by calling `super().show_board()`.
            4. get position input by calling `self.display.input_position()`.
                4.1. call `self.display.display_position_empty_error()` if there
                is not empty in the position.
                4.2. call `self.display.display_position_boundary_error()` if the
                position exceeds the boundary.
                4.3. call `self.display.display_position_info(position, self.black_turn)` if
                the position is valid.
            5. set a black/white piece in the input position.
            6. break loop if black/white wins the game.
        """
        raise NotImplementedError

    def win_judging(self,position:tuple) -> bool:
        """
        Determine whether black/white wins the game.

        Returns:
            bool: True if black/white wins the game
        """
        raise NotImplementedError


class Display:
    def __init__(self, gbk_console=False, ascii_piece=False):
        """
        Initialization.

        Args:
            gbk_console (bool): use gbk encoding, if your program outputs messy code, you
            can try it.
        """
        import sys
        import io

        sys.stdout = io.TextIOWrapper(
            sys.stdout.buffer, encoding="gbk" if gbk_console else "utf-8"
        )

        # self.balck_unit = "●"  if not ascii_piece else "x"
        # self.white_unit = "○"  if not ascii_piece else "o"
        # self.empty_unit = "+"

        self.balck_unit = "x"
        self.white_unit = "o"
        self.empty_unit = "+"

    def input_board_size(self) -> int:
        """
        Get chessboard size from user.

        Returns:
            int: the size of the chessboard
        """
        self.info("请输入棋盘大小:")
        size = int(input())
        return size

    def input_position(self) -> tuple:
        """
        Get next position from user to set a piece.

        Returns:
            tuple: the position tuple, with the form of (x,y), x is the row index
            and y is the column index, which should large than 0, i.e. x,y is in [1, size]
        """
        self.info("请输入坐标:")
        position = tuple(map(int, input().split()))
        while True:
            if len(position) == 2:
                break
            self.info("输入坐标格式错误", True)
            self.info("请输入坐标:")
            position = tuple(map(int, input().split()))
        return position

    def info(self, message: str, space_line=False):
        """
        Print a message to user.

        Args:
            message (str): the message string to print
            space_line (bool): whether to print another '\n' after the message
        """
        print(message)
        if space_line:
            print("")

    def display_winner(self, black_win: bool):
        """
        Print game winner info.

        Args:
            black_win (bool): wether the winner is black
        """
        win_message = "{}棋获胜".format("黑" if black_win else "白")
        self.info(win_message, True)

    def display_round(self, round_num, black_turn: bool):
        """
        Print round info.

        Args:
            round_num (int): current round
            black_turn (bool): wether the round is black's round
        """
        self.split_line(20)
        round_message = "回合{} {}棋回合:".format(round_num, "黑" if black_turn else "白")
        self.info(round_message, True)

    def display_position_info(self, position: tuple, black_turn: bool):
        """
        Print the input position info of this round.

        Args:
            position (tuple): the input position of this round, with the form of (x,y),
            x is the row index and y is the column index, which should large than 0,
            i.e. x,y is in [1, size]
            black_turn (bool): wether the round is black's round
        """
        position_info = "{}棋落子位置为 ({} {})".format(
            "黑" if black_turn else "白", position[0], position[1]
        )
        self.info(position_info, True)

    def display_help_info(self):
        """
        Print help message.
        """
        title = "帮助信息:"
        position_info = '坐标的形式如"3 5"，表示第3行第5列。坐标从1开始，最大不超过棋盘大小。'
        self.info(title)
        self.info(position_info, True)

    def display_position_boundary_error(self):
        """
        Print position boundary error message.
        """
        self.info("输入的坐标范围有误", True)

    def display_position_empty_error(self):
        """
        Print position empty error message.
        """
        self.info("该位置已经有棋子了", True)

    def split_line(self, width):
        """
        Print `--` for width times.
        """
        print("--" * width)

    def display_board(self, chessboard: SuperChessboard):
        """
        Display chessboard.

        Args:
            chessboard (SuperChessboard): the chessboard to display
        """
        board_size = chessboard.get_board_size()
        self.split_line(board_size + 1)
        # print coordinate
        row_str = "{:<2}" * board_size
        print("  " + row_str.format(*list(range(1, board_size + 1))))

        for i in range(1, board_size + 1):
            board_row = []
            for j in range(1, board_size + 1):
                piece = chessboard.get_piece((i, j))
                if piece.is_empty():
                    board_row.append(self.empty_unit)
                elif piece.is_white():
                    board_row.append(self.white_unit)
                else:
                    board_row.append(self.balck_unit)
            row_str = "{:<2d}".format(i) + " ".join(board_row)
            print(row_str)
        self.split_line(board_size + 1)


# your code here
# class Piece(SuperPiece) ...
# class Chessboard(SuperChessboard) ...
# class Game(SuperGame) ...


class Piece(SuperPiece):

    def is_empty(self) -> bool:
        return self.type == PieceType.empty

    def is_black(self) -> bool:
        return self.type == PieceType.black

    def is_white(self) -> bool:
        return self.type == PieceType.white


class Chessboard(SuperChessboard):

    def set_piece(self, black_turn:bool, position: tuple) -> bool:
        if position[0] > self.size or position[0] <= 0 or position[1] > self.size or position[1] <= 0:
            return False
        elif not self.isEmpty(position):
            return False
        elif black_turn:
            return self.set_black_piece(position)
        else:
            return self.set_white_piece(position)

    def set_black_piece(self, position: tuple) -> bool:
        if self.isEmpty(position):
            self.board[position[0] - 1][position[1] - 1].set_piece_type(PieceType.black)
            return True
        else:
            return False

    def set_white_piece(self, position: tuple) -> bool:
        if self.isEmpty(position):
            self.board[position[0] - 1][position[1] - 1].set_piece_type(PieceType.white)
            return True
        else:
            return False

    def set_empty_piece(self, position: tuple):
        self.board[position[0]-1][position[1]-1].set_piece_type(PieceType.empty)

    def get_piece(self, position: tuple) -> SuperPiece:
        return self.board[position[0]-1][position[1]-1]

    def isEmpty(self, position: tuple) -> bool:
        return self.board[position[0]-1][position[1]-1].is_empty()


class Game(SuperGame):

    def start(self):
        """
        Start the game.
        """
        self.game_loop()

    def show_board(self):
        """
        Show current chessboard to the user.
        """
        self.display.display_board(self.board)

    def game_loop(self):
        #todo
        """
        Start the game main loop.
        In this function, you should first call the `self.display.display_help_info()`,
        then enter a for/while loop, in which you should do things bellow:
            1. update `self.round_num`.
            2. diaplsy current round info by calling `self.display.display_round`.
            3. display chessboard by calling `super().show_board()`.
            4. get position input by calling `self.display.input_position()`.
                4.1. call `self.display.display_position_empty_error()` if there
                is not empty in the position.
                4.2. call `self.display.display_position_boundary_error()` if the
                position exceeds the boundary.
                4.3. call `self.display.display_position_info(position, self.black_turn)` if
                the position is valid.
            5. set a black/white piece in the input position.
            6. break loop if black/white wins the game.
        """
        size = self.display.input_board_size()
        self.display.display_help_info()
        self.set_size(size)
        someone_win = False
        black_turn = True
        position = (0,0)
        while not someone_win:
            self.round_num += 1
            black_turn = self.round_num % 2 == 1
            self.display.display_round(self.round_num, black_turn)
            self.show_board()
            not_set = True
            while not_set:
                position = self.display.input_position()
                if self.board.set_piece(black_turn, position):
                    self.display.display_position_info(position, black_turn)
                    not_set = False
                else:
                    if position[0] > size or position[0] <= 0 or position[1] > size or position[1] <= 0:
                        self.display.display_position_boundary_error()
                    elif not self.board.isEmpty(position):
                        self.display.display_position_empty_error()
            someone_win = self.win_judging(position)
        self.show_board()
        self.display.display_winner(black_turn)

    def win_judging(self,position:tuple) -> bool:
        if self.round_num < 9:
            return False
        """
        Determine whether black/white wins the game.

        Returns:
            bool: True if black/white wins the game
        """

        transverse = 0
        vertical = 0
        ltrslash = 0
        rtlslash = 0
        #竖直方向
        x,y = position[0],position[1]
        while x > 0:
            if self.board.board[x-1][y-1].type == self.board.board[position[0]-1][position[1]-1].type:
                vertical += 1
                x -= 1
            else:
                break

        x, y = position[0]+1, position[1]
        while x <= self.board_size:
            if self.board.board[x-1][y-1].type == self.board.board[position[0]-1][position[1]-1].type:
                vertical += 1
                x += 1
            else:
                break

        #水平方向
        x, y = position[0], position[1]
        while y > 0:
            if self.board.board[x-1][y-1].type == self.board.board[position[0]-1][position[1]-1].type:
                transverse += 1
                y -= 1
            else:
                break

        x, y = position[0], position[1] + 1
        while y <= self.board_size:
            if self.board.board[x-1][y-1].type == self.board.board[position[0]-1][position[1]-1].type:
                transverse += 1
                y += 1
            else:
                break

        #左上右下方向
        x, y = position[0], position[1]
        while x>0 and y >0:
            if self.board.board[x-1][y-1].type == self.board.board[position[0]-1][position[1]-1].type:
                ltrslash += 1
                x -= 1
                y -= 1
            else:
                break

        x, y = position[0]+1, position[1]+1
        while x <= self.board_size and y <= self.board_size:
            if self.board.board[x-1][y-1].type == self.board.board[position[0]-1][position[1]-1].type:
                ltrslash += 1
                x += 1
                y += 1
            else:
                break

        #左下右上方向
        x, y = position[0], position[1]
        while x > 0 and y <= self.board_size:
            if self.board.board[x-1][y-1].type == self.board.board[position[0]-1][position[1]-1].type:
                rtlslash += 1
                x -= 1
                y += 1
            else:
                break

        x, y = position[0] + 1, position[1] - 1
        while x <= self.board_size and y > 0:
            if self.board.board[x-1][y-1].type == self.board.board[position[0]-1][position[1]-1].type:
                rtlslash += 1
                x += 1
                y -= 1
            else:
                break

        return max(vertical,transverse,ltrslash,rtlslash) >= 5



if __name__ == "__main__":
    g = Game()
    g.start()

