"""Cody the Dog — SVG illustrations for all moods."""


def _dog(mouth, eye_l, eye_r, extras="", tongue=False, tail_path=None):
    tongue_svg = (
        '<ellipse cx="100" cy="119" rx="9" ry="7.5" fill="#FF6B8A"/>'
        '<line x1="100" y1="114" x2="100" y2="125" stroke="#E04070" stroke-width="1.8" stroke-linecap="round"/>'
    ) if tongue else ""

    default_tail = (
        'M 148 157 C 178 138 186 112 170 101 C 157 92 147 106 153 120 C 157 132 148 147 145 152'
    )
    tail = f'<path d="{ tail_path or default_tail }" fill="#8B4513" stroke="none"/>'

    return f"""<svg viewBox="0 0 200 235" xmlns="http://www.w3.org/2000/svg">
  <!-- ground shadow -->
  <ellipse cx="100" cy="228" rx="56" ry="7" fill="rgba(0,0,0,0.10)"/>

  <!-- body -->
  <ellipse cx="100" cy="180" rx="53" ry="46" fill="#A0522D"/>

  <!-- tail -->
  {tail}

  <!-- left ear (floppy — behind head) -->
  <ellipse cx="43" cy="79" rx="24" ry="34" fill="#5C2E0A" transform="rotate(-14,43,79)"/>
  <!-- right ear (floppy — behind head) -->
  <ellipse cx="157" cy="79" rx="24" ry="34" fill="#5C2E0A" transform="rotate(14,157,79)"/>

  <!-- head -->
  <circle cx="100" cy="83" r="51" fill="#A0522D"/>

  <!-- ear inner tone -->
  <ellipse cx="43" cy="81" rx="14" ry="24" fill="#7A3D18" transform="rotate(-14,43,81)"/>
  <ellipse cx="157" cy="81" rx="14" ry="24" fill="#7A3D18" transform="rotate(14,157,81)"/>

  <!-- snout -->
  <ellipse cx="100" cy="102" rx="28" ry="21" fill="#C07840"/>

  <!-- nose -->
  <ellipse cx="100" cy="92" rx="12" ry="8.5" fill="#180800"/>
  <!-- nose gloss -->
  <ellipse cx="96" cy="89" rx="3.5" ry="2.5" fill="rgba(255,255,255,0.28)"/>

  <!-- left eye white -->
  <circle cx="74" cy="73" r="13.5" fill="white"/>
  <!-- right eye white -->
  <circle cx="126" cy="73" r="13.5" fill="white"/>

  <!-- pupils / expressions -->
  {eye_l}
  {eye_r}

  <!-- mouth -->
  {mouth}

  <!-- tongue -->
  {tongue_svg}

  <!-- red collar -->
  <path d="M 60 129 Q 100 142 140 129" stroke="#C0392B" stroke-width="11" fill="none" stroke-linecap="round"/>
  <!-- collar highlight -->
  <path d="M 62 125 Q 100 137 138 125" stroke="#E74C3C" stroke-width="4" fill="none" stroke-linecap="round" opacity="0.5"/>
  <!-- dog tag -->
  <circle cx="100" cy="136" r="8" fill="#F5A623" stroke="#E67E22" stroke-width="1.8"/>
  <text x="100" y="139.5" text-anchor="middle" fill="white" font-size="8"
        font-weight="bold" font-family="Arial, sans-serif">C</text>

  <!-- left paw -->
  <ellipse cx="67" cy="213" rx="21" ry="14" fill="#9B4A28"/>
  <path d="M 56 210 Q 67 203 78 210" stroke="#7A3519" stroke-width="1.8" fill="none" stroke-linecap="round"/>
  <!-- right paw -->
  <ellipse cx="133" cy="213" rx="21" ry="14" fill="#9B4A28"/>
  <path d="M 122 210 Q 133 203 144 210" stroke="#7A3519" stroke-width="1.8" fill="none" stroke-linecap="round"/>

  <!-- extras (mood-specific) -->
  {extras}
</svg>"""


# ── shared eye shapes ────────────────────────────────────────

_EL_NORMAL = (
    '<circle cx="76" cy="74" r="9.5" fill="#180800"/>'
    '<circle cx="73" cy="71" r="3.8" fill="white"/>'
    '<circle cx="75" cy="70" r="1.6" fill="white"/>'
)
_ER_NORMAL = (
    '<circle cx="124" cy="74" r="9.5" fill="#180800"/>'
    '<circle cx="121" cy="71" r="3.8" fill="white"/>'
    '<circle cx="123" cy="70" r="1.6" fill="white"/>'
)

# wide (celebrate)
_EL_WIDE = (
    '<circle cx="74" cy="73" r="11" fill="#180800"/>'
    '<circle cx="70" cy="69" r="4.5" fill="white"/>'
    '<circle cx="73" cy="68" r="1.8" fill="white"/>'
)
_ER_WIDE = (
    '<circle cx="126" cy="73" r="11" fill="#180800"/>'
    '<circle cx="122" cy="69" r="4.5" fill="white"/>'
    '<circle cx="125" cy="68" r="1.8" fill="white"/>'
)

# droopy (sad) — pupils shifted down
_EL_SAD = (
    '<circle cx="74" cy="76" r="9.5" fill="#180800"/>'
    '<circle cx="71" cy="74" r="3" fill="white"/>'
)
_ER_SAD = (
    '<circle cx="126" cy="76" r="9.5" fill="#180800"/>'
    '<circle cx="123" cy="74" r="3" fill="white"/>'
)

# side-glance (thinking)
_EL_THINK = (
    '<circle cx="76" cy="73" r="9.5" fill="#180800"/>'
    '<circle cx="79" cy="70" r="3.8" fill="white"/>'
    '<circle cx="81" cy="69" r="1.6" fill="white"/>'
)
_ER_THINK = (
    '<circle cx="124" cy="73" r="9.5" fill="#180800"/>'
    '<circle cx="127" cy="70" r="3.8" fill="white"/>'
    '<circle cx="129" cy="69" r="1.6" fill="white"/>'
)

# ── mouth shapes ─────────────────────────────────────────────

_MOUTH_HAPPY = '<path d="M 85 112 Q 100 126 115 112" stroke="#180800" stroke-width="3.2" fill="none" stroke-linecap="round"/>'
_MOUTH_BIG   = '<path d="M 81 110 Q 100 128 119 110" stroke="#180800" stroke-width="3.8" fill="none" stroke-linecap="round"/>'
_MOUTH_FLAT  = '<path d="M 90 112 Q 100 116 110 112" stroke="#180800" stroke-width="2.8" fill="none" stroke-linecap="round"/>'
_MOUTH_SAD   = '<path d="M 85 116 Q 100 106 115 116" stroke="#180800" stroke-width="3" fill="none" stroke-linecap="round"/>'

# ── extras ───────────────────────────────────────────────────

_CELEBRATE_EXTRAS = (
    '<text x="12"  y="38"  font-size="22">⭐</text>'
    '<text x="158" y="28"  font-size="18">✨</text>'
    '<text x="8"   y="72"  font-size="18">🎉</text>'
    '<text x="162" y="68"  font-size="20">⭐</text>'
    '<text x="80"  y="20"  font-size="14">✨</text>'
)

_THINKING_EXTRAS = (
    '<text x="148" y="42" font-size="26">💭</text>'
    # raised eyebrow lines
    '<path d="M 63 58 Q 72 53 81 57" stroke="#5C2E0A" stroke-width="2.2" fill="none" stroke-linecap="round"/>'
    '<path d="M 119 57 Q 128 53 137 58" stroke="#5C2E0A" stroke-width="2.2" fill="none" stroke-linecap="round"/>'
)

_SAD_EXTRAS = (
    # droopy eyebrow lines
    '<path d="M 62 60 Q 71 65 81 62" stroke="#5C2E0A" stroke-width="2.2" fill="none" stroke-linecap="round"/>'
    '<path d="M 119 62 Q 129 65 138 60" stroke="#5C2E0A" stroke-width="2.2" fill="none" stroke-linecap="round"/>'
)

_READING_EXTRAS = (
    # glasses
    '<circle cx="74" cy="74" r="16" fill="none" stroke="#4A3728" stroke-width="2.2" opacity="0.7"/>'
    '<circle cx="126" cy="74" r="16" fill="none" stroke="#4A3728" stroke-width="2.2" opacity="0.7"/>'
    '<line x1="90" y1="74" x2="110" y2="74" stroke="#4A3728" stroke-width="2" opacity="0.7"/>'
    # book in paw
    '<rect x="38" y="198" width="30" height="22" rx="3" fill="#E8C560" stroke="#C8A030" stroke-width="1.5"/>'
    '<line x1="53" y1="198" x2="53" y2="220" stroke="#C8A030" stroke-width="1.2"/>'
    '<line x1="42" y1="205" x2="51" y2="205" stroke="#A07020" stroke-width="1"/>'
    '<line x1="42" y1="210" x2="51" y2="210" stroke="#A07020" stroke-width="1"/>'
    '<line x1="42" y1="215" x2="51" y2="215" stroke="#A07020" stroke-width="1"/>'
)

# ── wagging tail for happy ────────────────────────────────────
_TAIL_WAGGING = "M 148 155 C 182 132 190 105 172 97 C 158 89 147 104 154 119 C 159 132 150 146 146 152"
_TAIL_UP      = "M 148 155 C 175 128 180 100 162 94 C 149 88 142 105 150 118 C 156 130 148 146 145 152"

# ── public SVG strings ───────────────────────────────────────

CODY = {
    "happy": _dog(
        mouth=_MOUTH_HAPPY, eye_l=_EL_NORMAL, eye_r=_ER_NORMAL,
        tongue=True, tail_path=_TAIL_WAGGING,
    ),
    "celebrate": _dog(
        mouth=_MOUTH_BIG, eye_l=_EL_WIDE, eye_r=_ER_WIDE,
        extras=_CELEBRATE_EXTRAS, tongue=True, tail_path=_TAIL_UP,
    ),
    "thinking": _dog(
        mouth=_MOUTH_FLAT, eye_l=_EL_THINK, eye_r=_ER_THINK,
        extras=_THINKING_EXTRAS,
    ),
    "sad": _dog(
        mouth=_MOUTH_SAD, eye_l=_EL_SAD, eye_r=_ER_SAD,
        extras=_SAD_EXTRAS,
    ),
    "reading": _dog(
        mouth=_MOUTH_FLAT, eye_l=_EL_THINK, eye_r=_ER_THINK,
        extras=_READING_EXTRAS,
    ),
}


def cody_html(mood: str = "happy", size: int = 180) -> str:
    """Return an <img>-style inline SVG wrapped in a sized div."""
    svg = CODY.get(mood, CODY["happy"])
    return (
        f'<div style="width:{size}px;height:{size}px;display:flex;'
        f'align-items:center;justify-content:center;">'
        f'{svg}'
        f'</div>'
    )


def speech_bubble(text: str, mood: str = "happy") -> str:
    """Return HTML for Cody + a speech bubble side by side."""
    svg = CODY.get(mood, CODY["happy"])
    color_map = {
        "happy":     ("#FFF8F0", "#D2691E"),
        "celebrate": ("#FFFBEA", "#E6A817"),
        "thinking":  ("#F0F4FF", "#5B7FD4"),
        "sad":       ("#FFF0F0", "#C0392B"),
        "reading":   ("#F0FFF4", "#27AE60"),
    }
    bg, border = color_map.get(mood, ("#FFF8F0", "#D2691E"))
    return f"""
<div style="display:flex;align-items:flex-start;gap:16px;margin:8px 0;">
  <div style="flex-shrink:0;width:110px;height:110px;">{svg}</div>
  <div style="
      background:{bg};
      border:2px solid {border};
      border-radius:20px 20px 20px 4px;
      padding:14px 18px;
      font-size:1rem;
      line-height:1.6;
      color:#2C1810;
      flex:1;
      box-shadow:0 2px 12px rgba(0,0,0,0.06);
  ">{text}</div>
</div>"""
