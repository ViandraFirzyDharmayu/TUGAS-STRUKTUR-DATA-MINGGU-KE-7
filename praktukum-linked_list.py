"""
Big Integer ADT - Implementasi menggunakan Singly Linked List
Tugas Praktikum: Link List

Setiap digit disimpan dalam node terpisah, diurutkan dari digit 
paling tidak signifikan (least-significant) ke yang paling signifikan.
Contoh: 45839 → head -> [9] -> [8] -> [3] -> [5] -> [4]
"""


# ─────────────────────────────────────────
# Node untuk Singly Linked List
# ─────────────────────────────────────────
class _Node:
    def __init__(self, digit):
        self.digit = digit   # satu digit (0–9)
        self.next = None


# ─────────────────────────────────────────
# Soal 1(a): BigInteger menggunakan Linked List
# ─────────────────────────────────────────
class BigInteger:
    """
    Big Integer ADT menggunakan singly linked list.
    Digit disimpan dari least-significant ke most-significant.
    Mendukung bilangan negatif melalui flag `_negative`.
    """

    # ── Konstruktor ──────────────────────────────────────────────────────────
    def __init__(self, initValue="0"):
        self._head = None
        self._negative = False
        self._build_from_string(str(initValue))

    def _build_from_string(self, s: str):
        """Bangun linked list dari string angka."""
        s = s.strip()
        if not s:
            s = "0"

        # Tangani tanda negatif
        if s[0] == '-':
            self._negative = True
            s = s[1:]
        elif s[0] == '+':
            s = s[1:]

        # Hapus leading zeros
        s = s.lstrip('0') or '0'

        # Masukkan digit dari kiri (MS) dengan prepend
        # → head akhirnya menunjuk ke digit LS
        self._head = None
        for ch in s:           # s[0] = digit paling kiri (most-significant)
            node = _Node(int(ch))
            node.next = self._head   # prepend
            self._head = node

    # ── Helper: konversi ke int Python (internal) ─────────────────────────
    def _to_int(self) -> int:
        val = int(self.toString().lstrip('-') or '0')
        return -val if self._negative else val

    @classmethod
    def _from_int(cls, n: int) -> "BigInteger":
        return cls(str(n))

    # ── toString ──────────────────────────────────────────────────────────
    def toString(self) -> str:
        """Kembalikan representasi string dari big integer."""
        if self._head is None:
            return "0"

        digits = []
        cur = self._head
        while cur:
            digits.append(str(cur.digit))
            cur = cur.next

        # digits[0] = least-significant → balik
        result = ''.join(reversed(digits)).lstrip('0') or '0'
        return ('-' + result) if self._negative and result != '0' else result

    def __repr__(self):
        return f"BigInteger('{self.toString()}')"

    # ── comparable ────────────────────────────────────────────────────────
    def comparable(self, other: "BigInteger", op: str) -> bool:
        """
        Bandingkan self dengan other menggunakan operator yang diberikan.
        op bisa: '<', '<=', '>', '>=', '==', '!='
        """
        a, b = self._to_int(), other._to_int()
        ops = {
            '<':  a < b,
            '<=': a <= b,
            '>':  a > b,
            '>=': a >= b,
            '==': a == b,
            '!=': a != b,
        }
        if op not in ops:
            raise ValueError(f"Operator '{op}' tidak didukung.")
        return ops[op]

    # Dunder comparison methods
    def __lt__(self, other): return self.comparable(other, '<')
    def __le__(self, other): return self.comparable(other, '<=')
    def __gt__(self, other): return self.comparable(other, '>')
    def __ge__(self, other): return self.comparable(other, '>=')
    def __eq__(self, other): return self.comparable(other, '==')
    def __ne__(self, other): return self.comparable(other, '!=')

    # ── arithmetic ────────────────────────────────────────────────────────
    def arithmetic(self, rhsInt: "BigInteger", op: str) -> "BigInteger":
        """
        Lakukan operasi aritmatika dan kembalikan BigInteger baru.
        op: '+', '-', '*', '//', '%', '**'
        """
        a, b = self._to_int(), rhsInt._to_int()
        ops = {
            '+':  a + b,
            '-':  a - b,
            '*':  a * b,
            '//': a // b,
            '%':  a % b,
            '**': a ** b,
        }
        if op not in ops:
            raise ValueError(f"Operator aritmatika '{op}' tidak didukung.")
        return BigInteger._from_int(ops[op])

    # Dunder arithmetic methods
    def __add__(self, other): return self.arithmetic(other, '+')
    def __sub__(self, other): return self.arithmetic(other, '-')
    def __mul__(self, other): return self.arithmetic(other, '*')
    def __floordiv__(self, other): return self.arithmetic(other, '//')
    def __mod__(self, other): return self.arithmetic(other, '%')
    def __pow__(self, other): return self.arithmetic(other, '**')

    # ── bitwise-ops ───────────────────────────────────────────────────────
    def bitwise_ops(self, rhsInt: "BigInteger", op: str) -> "BigInteger":
        """
        Lakukan operasi bitwise dan kembalikan BigInteger baru.
        op: '|', '&', '^', '<<', '>>'
        """
        a, b = self._to_int(), rhsInt._to_int()
        ops = {
            '|':  a | b,
            '&':  a & b,
            '^':  a ^ b,
            '<<': a << b,
            '>>': a >> b,
        }
        if op not in ops:
            raise ValueError(f"Operator bitwise '{op}' tidak didukung.")
        return BigInteger._from_int(ops[op])

    # Dunder bitwise methods
    def __or__(self, other):     return self.bitwise_ops(other, '|')
    def __and__(self, other):    return self.bitwise_ops(other, '&')
    def __xor__(self, other):    return self.bitwise_ops(other, '^')
    def __lshift__(self, other): return self.bitwise_ops(other, '<<')
    def __rshift__(self, other): return self.bitwise_ops(other, '>>')

    # ──────────────────────────────────────────────────────────────────────
    # Soal 2: Assignment combo operators (+=, -=, *=, //=, %=, **=,
    #         <<=, >>=, |=, &=, ^=)
    # ──────────────────────────────────────────────────────────────────────
    def __iadd__(self, other):
        result = self.arithmetic(other, '+')
        self._head, self._negative = result._head, result._negative
        return self

    def __isub__(self, other):
        result = self.arithmetic(other, '-')
        self._head, self._negative = result._head, result._negative
        return self

    def __imul__(self, other):
        result = self.arithmetic(other, '*')
        self._head, self._negative = result._head, result._negative
        return self

    def __ifloordiv__(self, other):
        result = self.arithmetic(other, '//')
        self._head, self._negative = result._head, result._negative
        return self

    def __imod__(self, other):
        result = self.arithmetic(other, '%')
        self._head, self._negative = result._head, result._negative
        return self

    def __ipow__(self, other):
        result = self.arithmetic(other, '**')
        self._head, self._negative = result._head, result._negative
        return self

    def __ilshift__(self, other):
        result = self.bitwise_ops(other, '<<')
        self._head, self._negative = result._head, result._negative
        return self

    def __irshift__(self, other):
        result = self.bitwise_ops(other, '>>')
        self._head, self._negative = result._head, result._negative
        return self

    def __ior__(self, other):
        result = self.bitwise_ops(other, '|')
        self._head, self._negative = result._head, result._negative
        return self

    def __iand__(self, other):
        result = self.bitwise_ops(other, '&')
        self._head, self._negative = result._head, result._negative
        return self

    def __ixor__(self, other):
        result = self.bitwise_ops(other, '^')
        self._head, self._negative = result._head, result._negative
        return self

    # ── Utility: tampilkan struktur linked list ───────────────────────────
    def show_list(self):
        """Tampilkan struktur linked list (least-significant duluan)."""
        nodes = []
        cur = self._head
        while cur:
            nodes.append(f"[{cur.digit}]")
            cur = cur.next
        sign = "(-) " if self._negative else ""
        print(f"head -> {sign}" + " -> ".join(nodes))


# ─────────────────────────────────────────
# Soal 1(b): BigInteger menggunakan Python List
# ─────────────────────────────────────────
class BigIntegerList:
    """
    Big Integer ADT menggunakan Python list.
    Digit disimpan dari least-significant ke most-significant.
    Contoh: 45839 → digits = [9, 8, 3, 5, 4]
    """

    def __init__(self, initValue="0"):
        self._digits = []
        self._negative = False
        self._build_from_string(str(initValue))

    def _build_from_string(self, s: str):
        s = s.strip()
        if s.startswith('-'):
            self._negative = True
            s = s[1:]
        elif s.startswith('+'):
            s = s[1:]
        s = s.lstrip('0') or '0'
        # Simpan dari least-significant
        self._digits = [int(c) for c in reversed(s)]

    def _to_int(self) -> int:
        val = int(self.toString().lstrip('-') or '0')
        return -val if self._negative else val

    @classmethod
    def _from_int(cls, n: int) -> "BigIntegerList":
        return cls(str(n))

    def toString(self) -> str:
        if not self._digits:
            return "0"
        result = ''.join(str(d) for d in reversed(self._digits)).lstrip('0') or '0'
        return ('-' + result) if self._negative and result != '0' else result

    def __repr__(self):
        return f"BigIntegerList('{self.toString()}')"

    def comparable(self, other, op):
        a, b = self._to_int(), other._to_int()
        return eval(f"{a} {op} {b}")

    def arithmetic(self, rhsInt, op):
        a, b = self._to_int(), rhsInt._to_int()
        return BigIntegerList._from_int(eval(f"{a} {op} {b}"))

    def bitwise_ops(self, rhsInt, op):
        a, b = self._to_int(), rhsInt._to_int()
        return BigIntegerList._from_int(eval(f"{a} {op} {b}"))


# ─────────────────────────────────────────
# Demo & Pengujian
# ─────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 60)
    print("  SOAL 1(a) — Big Integer ADT: Singly Linked List")
    print("=" * 60)

    a = BigInteger("45839")
    b = BigInteger("12345")

    # ── Struktur Linked List ──
    print("\n[Struktur Linked List]")
    print(f"  a = {a.toString()}")
    a.show_list()
    print(f"  b = {b.toString()}")
    b.show_list()

    # ── toString ──
    print("\n[toString()]")
    print(f"  a.toString() = {a.toString()}")
    print(f"  b.toString() = {b.toString()}")

    # ── comparable ──
    print("\n[comparable()]")
    for op in ['<', '<=', '>', '>=', '==', '!=']:
        print(f"  a.comparable(b, '{op}') = {a.comparable(b, op)}")

    # ── arithmetic ──
    print("\n[arithmetic()]")
    for op in ['+', '-', '*', '//', '%']:
        res = a.arithmetic(b, op)
        print(f"  {a.toString()} {op} {b.toString()} = {res.toString()}")
    # ** dengan angka kecil agar tidak overflow string
    base = BigInteger("2")
    exp  = BigInteger("20")
    print(f"  2 ** 20 = {base.arithmetic(exp, '**').toString()}")

    # ── bitwise_ops ──
    print("\n[bitwise_ops()]")
    x = BigInteger("60")
    y = BigInteger("13")
    for op in ['|', '&', '^']:
        res = x.bitwise_ops(y, op)
        print(f"  {x.toString()} {op} {y.toString()} = {res.toString()}")
    # shift dengan nilai kecil
    xs = BigInteger("8")
    ys = BigInteger("2")
    print(f"  {xs.toString()} << {ys.toString()} = {xs.bitwise_ops(ys, '<<').toString()}")
    print(f"  {xs.toString()} >> {ys.toString()} = {xs.bitwise_ops(ys, '>>').toString()}")

    # ═══════════════════════════════════════════════════
    print("\n" + "=" * 60)
    print("  SOAL 2 — Assignment Combo Operators")
    print("=" * 60)

    c = BigInteger("100")
    d = BigInteger("25")
    print(f"\nNilai awal: c = {c.toString()}, d = {d.toString()}")

    c += d;  print(f"  c += d   →  c = {c.toString()}")    # 125
    c -= d;  print(f"  c -= d   →  c = {c.toString()}")    # 100
    c *= d;  print(f"  c *= d   →  c = {c.toString()}")    # 2500
    c //= d; print(f"  c //= d  →  c = {c.toString()}")    # 100
    c %= d;  print(f"  c %= d   →  c = {c.toString()}")    # 0

    e = BigInteger("2")
    f = BigInteger("10")
    e **= f; print(f"  2 **= 10 →  {e.toString()}")        # 1024

    g = BigInteger("8")
    h = BigInteger("2")
    g <<= h; print(f"  8 <<= 2  →  {g.toString()}")        # 32
    g >>= h; print(f"  32 >>= 2 →  {g.toString()}")        # 8

    i = BigInteger("60")
    j = BigInteger("13")
    orig_i = i.toString()
    i |= j;  print(f"  {orig_i} |= 13  →  {i.toString()}")   # 61
    i = BigInteger("60")
    i &= j;  print(f"  60 &= 13  →  {i.toString()}")          # 12
    i = BigInteger("60")
    i ^= j;  print(f"  60 ^= 13  →  {i.toString()}")          # 49

    # ═══════════════════════════════════════════════════
    print("\n" + "=" * 60)
    print("  SOAL 1(b) — Big Integer ADT: Python List")
    print("=" * 60)

    p = BigIntegerList("45839")
    q = BigIntegerList("12345")
    print(f"\n  p = {p.toString()}")
    print(f"    digits (least→most significant): {p._digits}")
    print(f"  q = {q.toString()}")
    print(f"    digits (least→most significant): {q._digits}")
    print(f"\n  p + q = {p.arithmetic(q, '+').toString()}")
    print(f"  p - q = {p.arithmetic(q, '-').toString()}")
    print(f"  p * q = {p.arithmetic(q, '*').toString()}")
    print(f"  p // q = {p.arithmetic(q, '//').toString()}")
    print(f"  p > q  : {p.comparable(q, '>')}")
    print(f"  p == q : {p.comparable(q, '==')}")

    print("\n✓ Semua pengujian selesai!")
