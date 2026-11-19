"""png.py — stdlib-only canvas + PNG writer.

Integer-only drawing on a 1024x1024 RGB canvas, and a deterministic
indexed-free PNG encoder (filter 0 on every scanline, fixed zlib level,
no ancillary chunks, no time/text chunks): the same program always
writes the same bytes.
"""
import binascii
import struct
import zlib


def _chunk(typ, data):
    out = struct.pack(">I", len(data)) + typ + data
    return out + struct.pack(">I", binascii.crc32(typ + data) & 0xFFFFFFFF)


class Canvas:
    def __init__(self, w, h, bg):
        self.w = w
        self.h = h
        r, g, b = bg
        self.buf = bytearray(bytes((r, g, b)) * (w * h))

    def _off(self, x, y):
        return (y * self.w + x) * 3

    def set(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h:
            o = self._off(x, y)
            self.buf[o] = c[0]
            self.buf[o + 1] = c[1]
            self.buf[o + 2] = c[2]

    def fill_rect(self, x, y, w, h, c):
        x0 = max(0, x)
        y0 = max(0, y)
        x1 = min(self.w, x + w)
        y1 = min(self.h, y + h)
        if x1 <= x0 or y1 <= y0:
            return
        row = bytes(c) * (x1 - x0)
        for yy in range(y0, y1):
            o = self._off(x0, yy)
            self.buf[o:o + len(row)] = row

    def rect(self, x, y, w, h, c, t=1):
        self.fill_rect(x, y, w, t, c)
        self.fill_rect(x, y + h - t, w, t, c)
        self.fill_rect(x, y, t, h, c)
        self.fill_rect(x + w - t, y, t, h, c)

    def hline(self, x0, x1, y, c):
        if y < 0 or y >= self.h:
            return
        a = max(0, min(x0, x1))
        b = min(self.w - 1, max(x0, x1))
        if b < a:
            return
        row = bytes(c) * (b - a + 1)
        o = self._off(a, y)
        self.buf[o:o + len(row)] = row

    def vline(self, x, y0, y1, c):
        if x < 0 or x >= self.w:
            return
        a = max(0, min(y0, y1))
        b = min(self.h - 1, max(y0, y1))
        for yy in range(a, b + 1):
            o = self._off(x, yy)
            self.buf[o] = c[0]
            self.buf[o + 1] = c[1]
            self.buf[o + 2] = c[2]

    def line(self, x0, y0, x1, y1, c):
        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        x, y = x0, y0
        while True:
            self.set(x, y, c)
            if x == x1 and y == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x += sx
            if e2 <= dx:
                err += dx
                y += sy

    def disc(self, cx, cy, r, c):
        # Filled circle via horizontal spans (integer math only).
        for dy in range(-r, r + 1):
            dx = int((r * r - dy * dy) ** 0.5)
            self.hline(cx - dx, cx + dx, cy + dy, c)

    def ring(self, cx, cy, r, c):
        # Circle outline, 1px.
        x = 0
        y = r
        d = 1 - r
        while x <= y:
            for px, py in ((cx + x, cy + y), (cx + y, cy + x),
                           (cx - x, cy + y), (cx - y, cy + x),
                           (cx + x, cy - y), (cx + y, cy - x),
                           (cx - x, cy - y), (cx - y, cy - x)):
                self.set(px, py, c)
            if d < 0:
                d += 2 * x + 3
            else:
                d += 2 * (x - y) + 5
                y -= 1
            x += 1

    def poly(self, pts, c):
        # Scanline polygon fill. pts: list of (x, y), integer only.
        if len(pts) < 3:
            return
        ys = [p[1] for p in pts]
        ymin, ymax = min(ys), max(ys)
        n = len(pts)
        for y in range(ymin, ymax + 1):
            xs = []
            for i in range(n):
                x0, y0 = pts[i]
                x1, y1 = pts[(i + 1) % n]
                if y0 == y1:
                    continue
                if (y0 <= y < y1) or (y1 <= y < y0):
                    x = x0 + (y - y0) * (x1 - x0) // (y1 - y0)
                    xs.append(x)
            xs.sort()
            for i in range(0, len(xs) - 1, 2):
                self.hline(xs[i], xs[i + 1], y, c)

    # ---- text (embedded bitmap font) ----

    def text_w(self, s, fnt, scale=1):
        w = 0
        for ch in s:
            g = fnt.get(ch)
            if g is None:
                g = fnt["?"]
            w += g[0] * scale
        return w

    def text(self, x, y, s, fnt, scale, color):
        """Draw text; (x, y) is the top-left of the em box (20px tall
        at scale 1, baseline at row 15). Returns the width drawn."""
        cx = x
        for ch in s:
            g = fnt.get(ch)
            if g is None:
                g = fnt["?"]
            adv, w, h, top, rows = g
            if isinstance(rows, int):
                rows = (rows,)  # single-row glyphs stored bare
            if w and h:
                for ri, bits in enumerate(rows):
                    py = y + (top + ri) * scale
                    for bx in range(w):
                        if bits >> (w - 1 - bx) & 1:
                            px = cx + bx * scale
                            self.fill_rect(px, py, scale, scale, color)
            cx += adv * scale
        return cx - x

    def wrap(self, s, fnt, scale, maxw):
        """Greedy word wrap; returns a list of lines that fit maxw."""
        words = s.split(" ")
        lines = []
        cur = ""
        for wd in words:
            trial = wd if not cur else cur + " " + wd
            if self.text_w(trial, fnt, scale) <= maxw or not cur:
                cur = trial
            else:
                lines.append(cur)
                cur = wd
        if cur:
            lines.append(cur)
        return lines

    # ---- PNG output ----

    def png_bytes(self):
        raw = bytearray()
        stride = self.w * 3
        for y in range(self.h):
            raw.append(0)  # filter: None
            o = y * stride
            raw += self.buf[o:o + stride]
        ihdr = struct.pack(">IIBBBBB", self.w, self.h, 8, 2, 0, 0, 0)
        out = b"\x89PNG\r\n\x1a\n"
        out += _chunk(b"IHDR", ihdr)
        out += _chunk(b"IDAT", zlib.compress(bytes(raw), 9))
        out += _chunk(b"IEND", b"")
        return out
