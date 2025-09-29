class VideoText:
    def __init__(
            self,
    ):
        self.opening_animation_text()
        self.head_file_text()
        self.insert_animation_text()

    def opening_animation_text(self):
        self.START_TEX = r"""
            \begin{tabular}{p{8cm}}
            \hspace{1em}
            “形而上者谓之道，形而下者谓之器。”
            \end{tabular}
        """

        self.AUTHER_TEX = r"""
            \begin{tabular}{p{8cm}}
            \hspace{1em}
            ————《易经$\bullet$系辞》
            \end{tabular}
        """

        self.EXPLAIN_TEX = r"""
            \begin{tabular}{p{8cm}}
            \hspace{1em}
            详见课本19页，中华传统文化中的抽象思维。
            \end{tabular}
        """
    def head_file_text(self):
        self.TOTAL_TEX = [
            r"InitList(\&L)",
            r"DestroyList(\&L)",
            r"ListInsert(\&L, i, e)",
            r"ListErase(\&L, i, \&e)",
            r"ListClear(\&L)",
            r"ListAssign(L, i, value)",
            r"ListEmpty(L)",
            r"ListSize(L)",
            r"ListGetElem(L, i \&e)",
            r"ListFind(L, e)",
            r"ListTraverse(L, visit())"
        ]

        self.TITLE = r"线性表\\基本操作方法"

        self.CAPTION1 = r"""
            可暂停了解,\\
            详情见课本14页
        """

        self.CAPTION2 = r"""
            \&
        """
        self.CAPTION3 = r"""
            Sequential
        """
    def insert_animation_text(self):
        self.CAPTION4 = r"i = 1"
        self.CAPTION5 = r"i = 0"